#!/usr/bin/env python3
"""
Setup Contract Verification
Helps users set up API tokens for contract verification
"""

import os
from dotenv import load_dotenv, set_key

def main():
    """Setup verification API tokens"""
    
    print("🔧 PAYMENT SPLITTER - VERIFICATION SETUP 🔧")
    print("=" * 50)
    
    # Load existing environment
    load_dotenv()
    
    print("To enable automatic contract verification, you need API tokens.")
    print("This allows Brownie to verify your contracts on CeloScan automatically.")
    
    # Check for existing tokens
    celoscan_token = os.getenv("CELOSCAN_TOKEN")
    
    if celoscan_token:
        print(f"\n✅ CeloScan API token already configured")
        print(f"Token: {celoscan_token[:10]}...{celoscan_token[-10:]}")
    else:
        print(f"\n❌ CeloScan API token not found")
        print(f"Follow these steps to get one:")
        print(f"1. Visit: https://celoscan.io/apis")
        print(f"2. Create a free account")
        print(f"3. Generate an API key")
        print(f"4. Copy the API key")
        
        # Get token from user
        token = input(f"\nEnter your CeloScan API token (or press Enter to skip): ").strip()
        
        if token:
            # Save to .env
            set_key(".env", "CELOSCAN_TOKEN", token)
            print(f"✅ CeloScan API token saved to .env")
        else:
            print(f"⚠️  Skipping API token setup")
            print(f"You can still verify contracts manually")
    
    # Show verification options
    print(f"\n📋 VERIFICATION OPTIONS:")
    print(f"1. Automatic (requires API token): brownie run deploy --network alfajores")
    print(f"2. Manual verification: brownie run verify_contract --network alfajores")
    print(f"3. Manual on CeloScan: https://alfajores.celoscan.io/verifyContract")
    
    # Show current status
    print(f"\n📊 CURRENT STATUS:")
    if os.getenv("CELOSCAN_TOKEN"):
        print(f"✅ Auto-verification: Enabled")
    else:
        print(f"⚠️  Auto-verification: Disabled (no API token)")
    
    print(f"✅ Manual verification: Available")
    print(f"✅ Network configured: alfajores")
    
    print(f"\n🎉 Setup complete!")
    print(f"Ready to deploy and verify your contracts!")

if __name__ == "__main__":
    main()
