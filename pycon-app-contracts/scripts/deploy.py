#!/usr/bin/env python3
"""
Deploy Script for Payment Splitter DApp
Deploys the PaymentSplitter contract to the network
"""

import os
from brownie import PaymentSplitter, accounts, network, config
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    
    # Get account from .env file
    if os.getenv("PRIVATE_KEY"):
        account = accounts.add(os.getenv("PRIVATE_KEY"))
    else:
        print("❌ No PRIVATE_KEY found in .env file")
        print("Run: python scripts/create_account.py first")
        return
    
    print(f"🚀 PAYMENT SPLITTER - DEPLOY CONTRACT 🚀")
    print(f"=" * 50)
    print(f"Network: {network.show_active()}")
    print(f"Account: {account}")
    print(f"Balance: {account.balance() / 1e18:.4f} CELO")
    
    if account.balance() == 0:
        print(f"\n⚠️  WARNING: Account has no CELO!")
        print(f"Get test CELO from: https://faucet.celo.org/")
        print(f"Enter address: {account}")
        return
    
    # Deploy contract
    print(f"\n📦 Deploying PaymentSplitter contract...")
    try:
        payment_splitter = PaymentSplitter.deploy({"from": account})
        
        print(f"\n✅ SUCCESS! Contract deployed!")
        print(f"Contract Address: {payment_splitter.address}")
        print(f"Transaction Hash: {payment_splitter.tx.txid}")
        
        # Show contract info
        print(f"\n📋 CONTRACT INFO:")
        print(f"Next Payment ID: {payment_splitter.nextPaymentId()}")
        print(f"Network: {network.show_active()}")
        
        if network.show_active() != "development":
            explorer_url = f"https://alfajores.celoscan.io/address/{payment_splitter.address}"
            print(f"Explorer: {explorer_url}")
        
        print(f"\n🎉 Contract ready to create payment splits!")
        print(f"💡 Next: Run 'brownie run create_payment --network {network.show_active()}'")
        
        # Manual verification instructions for testnet
        if network.show_active() != "development":
            print(f"\n🔍 CONTRACT VERIFICATION")
            print(f"To verify your contract on CeloScan:")
            print(f"")
            print(f"1. Visit: https://alfajores.celoscan.io/address/{payment_splitter.address}")
            print(f"2. Click 'Contract' tab")
            print(f"3. Click 'Verify and Publish'")
            print(f"4. Select 'Solidity (Single file)'")
            print(f"5. Enter compiler version: 0.8.19")
            print(f"6. Upload the content of contracts/PaymentSplitter.sol")
            print(f"7. Click 'Verify and Publish'")
            print(f"")
            print(f"📋 Alternative verification methods:")
            print(f"   • brownie run verify_contract --network {network.show_active()}")
            print(f"   • https://alfajores.celoscan.io/verifyContract")
            print(f"   • Contract address: {payment_splitter.address}")
        
        return payment_splitter
        
    except Exception as e:
        print(f"\n❌ Deployment failed: {str(e)}")
        print(f"Check your balance and try again")
        return None

if __name__ == "__main__":
    main()
