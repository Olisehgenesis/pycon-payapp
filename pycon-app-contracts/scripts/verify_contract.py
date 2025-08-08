#!/usr/bin/env python3
"""
Contract Verification Script for Payment Splitter DApp
Verifies the deployed contract on Celo Alfajores explorer
"""

import os
from brownie import PaymentSplitter, network
from dotenv import load_dotenv

def main():
    """Verify the deployed contract on explorer"""
    
    print("🔍 PAYMENT SPLITTER - CONTRACT VERIFICATION 🔍")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Get contract address
    contract_address = input("Enter deployed PaymentSplitter contract address: ").strip()
    if not contract_address:
        print("❌ Contract address is required")
        return
    
    print(f"Contract Address: {contract_address}")
    print(f"Network: {network.show_active()}")
    
    # Provide manual verification instructions
    print(f"\n🔍 CONTRACT VERIFICATION")
    print(f"To verify your contract on CeloScan:")
    print(f"")
    print(f"1. Visit: https://alfajores.celoscan.io/address/{contract_address}")
    print(f"2. Click 'Contract' tab")
    print(f"3. Click 'Verify and Publish'")
    print(f"4. Select 'Solidity (Single file)'")
    print(f"5. Enter compiler version: 0.8.19")
    print(f"6. Upload the content of contracts/PaymentSplitter.sol")
    print(f"7. Click 'Verify and Publish'")
    print(f"")
    print(f"✅ Manual verification instructions provided!")
    print(f"Explorer: https://alfajores.celoscan.io/address/{contract_address}")
    print(f"Contract Code: https://alfajores.celoscan.io/address/{contract_address}#code")

if __name__ == "__main__":
    main()
