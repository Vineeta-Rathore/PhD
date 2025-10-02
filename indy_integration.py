
import asyncio
import json
from indy import did, wallet, pool, ledger, anoncreds
from indy.error import IndyError, ErrorCode

class HyperledgerIndyIntegration:
    def __init__(self, pool_name, wallet_config, wallet_credentials):
        self.pool_name = pool_name
        self.wallet_config = wallet_config
        self.wallet_credentials = wallet_credentials
        self.wallet_handle = None
        self.pool_handle = None

    async def initialize(self):
        """Initialize Indy wallet and pool connection"""
        try:
            # Create and open wallet
            await wallet.create_wallet(self.wallet_config, self.wallet_credentials)
            self.wallet_handle = await wallet.open_wallet(
                self.wallet_config, self.wallet_credentials
            )

            # Open pool connection
            self.pool_handle = await pool.open_pool_ledger(self.pool_name, None)

        except IndyError as e:
            if e.error_code == ErrorCode.WalletAlreadyExistsError:
                self.wallet_handle = await wallet.open_wallet(
                    self.wallet_config, self.wallet_credentials
                )
            else:
                raise e

    async def create_did(self, seed=None):
        """Create a new DID on the Indy network"""
        did_config = json.dumps({"seed": seed}) if seed else "{}"

        (did_value, verkey) = await did.create_and_store_my_did(
            self.wallet_handle, did_config
        )

        return {
            "did": did_value,
            "verkey": verkey
        }

    async def register_schema(self, issuer_did, schema_name, schema_version, attributes):
        """Register a credential schema on the ledger"""
        schema_id, schema_json = await anoncreds.issuer_create_schema(
            issuer_did, schema_name, schema_version, json.dumps(attributes)
        )

        # Submit schema to ledger
        schema_request = await ledger.build_schema_request(
            issuer_did, schema_json
        )
        await ledger.sign_and_submit_request(
            self.pool_handle, self.wallet_handle, issuer_did, schema_request
        )

        return schema_id

    async def create_credential_definition(self, issuer_did, schema_json):
        """Create a credential definition for issuing credentials"""
        cred_def_id, cred_def_json = await anoncreds.issuer_create_and_store_credential_def(
            self.wallet_handle, issuer_did, schema_json, 
            "default", "CL", json.dumps({"support_revocation": True})
        )

        # Submit credential definition to ledger
        cred_def_request = await ledger.build_cred_def_request(
            issuer_did, cred_def_json
        )
        await ledger.sign_and_submit_request(
            self.pool_handle, self.wallet_handle, issuer_did, cred_def_request
        )

        return cred_def_id

    async def issue_credential(self, issuer_did, cred_def_id, prover_did, credential_values):
        """Issue a credential to a prover"""
        # Create credential offer
        cred_offer_json = await anoncreds.issuer_create_credential_offer(
            self.wallet_handle, cred_def_id
        )

        # Issue credential
        cred_json, _, _ = await anoncreds.issuer_create_credential(
            self.wallet_handle, cred_offer_json, "{}", 
            json.dumps(credential_values), None, None
        )

        return json.loads(cred_json)

    async def create_proof_request(self, requested_attributes, requested_predicates):
        """Create a proof request for credential verification"""
        proof_request = {
            "nonce": "123432421212",
            "name": "Privacy-Preserving Credential Verification",
            "version": "1.0",
            "requested_attributes": requested_attributes,
            "requested_predicates": requested_predicates
        }

        return json.dumps(proof_request)

    async def verify_proof(self, proof_json, proof_request_json, schemas, cred_defs, rev_regs):
        """Verify a credential proof"""
        valid = await anoncreds.verifier_verify_proof(
            proof_request_json, proof_json, schemas, cred_defs, rev_regs, "{}"
        )

        return valid

    async def close(self):
        """Close wallet and pool connections"""
        if self.wallet_handle:
            await wallet.close_wallet(self.wallet_handle)
        if self.pool_handle:
            await pool.close_pool_ledger(self.pool_handle)
