#!/usr/bin/env python3
"""
Create Account Script for Payment Splitter DApp
Creates a new account and saves private key to .env file
"""

import os
from eth_account import Account
from dotenv import load_dotenv, set_key

def main():
    print("🔐 PAYMENT SPLITTER - CREATE ACCOUNT 🔐")
    print("=" * 50)
    
    # Generate new account
    print("Generating new account...")
    account = Account.create()
    
    # Get account details
    private_key = account.key.hex()
    address = account.address
    
    print(f"\n✅ Account created successfully!")
    print(f"Address: {address}")
    print(f"Private Key: {private_key[:10]}...{private_key[-10:]}")
    
    # Save to .env file
    env_file = ".env"
    
    # Create .env file if it doesn't exist
    if not os.path.exists(env_file):
        with open(env_file, 'w') as f:
            f.write("# Payment Splitter DApp Environment Variables\n")
    
    # Save private key to .env
    set_key(env_file, "PRIVATE_KEY", private_key)
    
    print(f"\n💾 Private key saved to {env_file}")
    print(f"⚠️  Keep this file secure and never share it!")
    
    # Display next steps
    print(f"\n📋 NEXT STEPS:")
    print(f"1. Get test CELO from: https://faucet.celo.org/")
    print(f"2. Enter your address: {address}")
    print(f"3. Select 'Alfajores' network")
    print(f"4. Deploy contract: brownie run deploy --network alfajores")
    
    print(f"\n🔗 Useful Links:")
    print(f"• Celo Faucet: https://faucet.celo.org/")
    print(f"• Alfajores Explorer: https://alfajores.celoscan.io/")
    print(f"• Your Address: https://alfajores.celoscan.io/address/{address}")
    
    return account

if __name__ == "__main__":
    main()
