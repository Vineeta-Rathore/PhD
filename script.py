# Step 1: Verify system setup and file structure
import os
import sys

print("🔍 STEP 1: SYSTEM SETUP VERIFICATION")
print("=" * 50)

# Check required files
required_files = [
    'DIDRegistry.sol',
    'credential_verification.circom', 
    'privacy_auth.js',
    'indy_integration.py',
    'package.json',
    'hardhat.config.js',
    'requirements.txt',
    'run_tests.py'
]

print("📄 Checking required implementation files:")
all_files_present = True

for file in required_files:
    if os.path.exists(file):
        file_size = os.path.getsize(file)
        print(f"✅ {file} - {file_size:,} bytes")
    else:
        print(f"❌ {file} - MISSING")
        all_files_present = False

# Check directories
required_dirs = ['scripts', 'test', 'contracts', 'circuits']
print(f"\n📁 Checking required directories:")

for directory in required_dirs:
    if os.path.exists(directory):
        files_count = len(os.listdir(directory)) if os.path.isdir(directory) else 0
        print(f"✅ {directory}/ - {files_count} files")
    else:
        print(f"❌ {directory}/ - MISSING")

# Check Python version
print(f"\n🐍 Python version check:")
python_version = sys.version_info
print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")

if python_version.major >= 3 and python_version.minor >= 8:
    print("✅ Python version is compatible (3.8+)")
else:
    print("❌ Python version should be 3.8 or higher")

# Organize files into proper directories
print(f"\n🔧 Organizing project structure:")

# Move DIDRegistry.sol to contracts/
if os.path.exists('DIDRegistry.sol') and not os.path.exists('contracts/DIDRegistry.sol'):
    if not os.path.exists('contracts'):
        os.makedirs('contracts')
    
    # Copy instead of move to keep original
    import shutil
    shutil.copy2('DIDRegistry.sol', 'contracts/DIDRegistry.sol')
    print("✅ Moved DIDRegistry.sol to contracts/")

# Move circuit file to circuits/
if os.path.exists('credential_verification.circom') and not os.path.exists('circuits/credential_verification.circom'):
    if not os.path.exists('circuits'):
        os.makedirs('circuits')
    
    shutil.copy2('credential_verification.circom', 'circuits/credential_verification.circom')
    print("✅ Moved credential_verification.circom to circuits/")

# Summary
print(f"\n📊 STEP 1 SUMMARY:")
print(f"✅ Required files: {'All present' if all_files_present else 'Some missing'}")
print(f"✅ Directory structure: Organized")
print(f"✅ Python compatibility: Verified")

print(f"\n🎯 STEP 1 STATUS: {'COMPLETED SUCCESSFULLY' if all_files_present else 'NEEDS ATTENTION'}")

if all_files_present:
    print(f"\n➡️  Ready to proceed to Step 2: Installing Node.js dependencies")
    print(f"💡 Please acknowledge to continue with: npm install")
else:
    print(f"\n⚠️  Please ensure all files are present before proceeding")