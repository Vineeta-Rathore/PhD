const { ethers } = require("hardhat");

async function main() {
  console.log("🚀 Deploying DID Registry contract...");

  const [deployer] = await ethers.getSigners();
  console.log("Deploying with account:", deployer.address);

  const DIDRegistry = await ethers.getContractFactory("DIDRegistry");
  const didRegistry = await DIDRegistry.deploy();
  await didRegistry.deployed();

  console.log("✅ DID Registry deployed to:", didRegistry.address);

  const deploymentInfo = {
    contractAddress: didRegistry.address,
    deployer: deployer.address,
    network: "localhost"
  };

  console.log("📄 Deployment completed successfully");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("❌ Deployment failed:", error);
    process.exit(1);
  });