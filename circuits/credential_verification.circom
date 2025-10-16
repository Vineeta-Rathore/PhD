
pragma circom 2.0.0;

template CredentialVerification() {
    // Private inputs (not revealed during proof)
    signal private input credentialHash;
    signal private input userSecret;
    signal private input attributes[10]; // Up to 10 attributes
    signal private input attributeFlags[10]; // Which attributes to reveal

    // Public inputs (revealed during proof)
    signal input challenge;
    signal input issuerPublicKey;
    signal input schemaHash;

    // Outputs
    signal output validCredential;
    signal output attributeCommitments[10];

    // Components
    component hasher = Poseidon(12);
    component attributeHashers[10];

    // Initialize attribute hashers
    for (var i = 0; i < 10; i++) {
        attributeHashers[i] = Poseidon(3);
    }

    // Verify credential hash
    hasher.inputs[0] <== userSecret;
    hasher.inputs[1] <== issuerPublicKey;
    for (var i = 0; i < 10; i++) {
        hasher.inputs[i+2] <== attributes[i];
    }

    // Check if computed hash matches the provided credential hash
    validCredential <== (hasher.out === credentialHash) ? 1 : 0;

    // Generate selective attribute commitments
    for (var i = 0; i < 10; i++) {
        attributeHashers[i].inputs[0] <== attributes[i];
        attributeHashers[i].inputs[1] <== userSecret;
        attributeHashers[i].inputs[2] <== attributeFlags[i];

        // Only reveal attribute if flag is set
        attributeCommitments[i] <== attributeFlags[i] * attributeHashers[i].out;
    }
}

component main = CredentialVerification();
