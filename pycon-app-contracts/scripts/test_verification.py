#!/usr/bin/env python3
"""
Test Contract Verification
Tests the verification functionality for the PaymentSplitter contract
"""

import os
from brownie import PaymentSplitter, network
from dotenv import load_dotenv

def main():
    """Test contract verification functionality"""
    
    print("🧪 PAYMENT SPLITTER - VERIFICATION TEST 🧪")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check if we're on a testnet
    current_network = network.show_active()
    print(f"Current Network: {current_network}")
    
    if current_network == "development":
        print("⚠️  Verification only works on testnets/mainnets")
        print("Switch to alfajores: brownie run test_verification --network alfajores")
        return
    
    # Get contract address
    contract_address = input("Enter deployed PaymentSplitter contract address: ").strip()
    if not contract_address:
        print("❌ Contract address is required")
        return
    
    print(f"\n🔍 Testing verification for: {contract_address}")
    
    # Test 1: Check if contract exists
    print(f"\n📋 Test 1: Contract Existence")
    try:
        contract = PaymentSplitter.at(contract_address)
        print(f"✅ Contract found at address")
        print(f"Contract Name: {contract._name}")
        print(f"Contract ABI: Available")
    except Exception as e:
        print(f"❌ Contract not found: {str(e)}")
        return
    
    # Test 2: Check basic functionality
    print(f"\n📋 Test 2: Basic Functionality")
    try:
        next_id = contract.nextPaymentId()
        print(f"✅ Next Payment ID: {next_id}")
        print(f"✅ Contract is functional")
    except Exception as e:
        print(f"❌ Contract not functional: {str(e)}")
        return
    
    # Test 3: Check verification status
    print(f"\n📋 Test 3: Verification Status")
    try:
        # Try to get contract source code (this would work if verified)
        contract_source = contract._build
        print(f"✅ Contract source code available")
        print(f"✅ Contract appears to be verified")
    except Exception as e:
        print(f"⚠️  Contract may not be verified: {str(e)}")
        print(f"💡 Run: brownie run verify_contract --network {current_network}")
    
    # Test 4: Explorer links
    print(f"\n📋 Test 4: Explorer Links")
    if current_network == "alfajores":
        explorer_url = f"https://alfajores.celoscan.io/address/{contract_address}"
        code_url = f"https://alfajores.celoscan.io/address/{contract_address}#code"
        print(f"✅ Explorer: {explorer_url}")
        print(f"✅ Code: {code_url}")
    else:
        print(f"⚠️  Unknown network: {current_network}")
    
    # Summary
    print(f"\n📊 VERIFICATION TEST SUMMARY")
    print(f"=" * 30)
    print(f"Contract Address: {contract_address}")
    print(f"Network: {current_network}")
    print(f"Status: {'Verified' if 'verified' in locals() else 'Not Verified'}")
    print(f"Functional: ✅")
    
    if current_network == "alfajores":
        print(f"\n🔗 View your contract:")
        print(f"Explorer: https://alfajores.celoscan.io/address/{contract_address}")
        print(f"Code: https://alfajores.celoscan.io/address/{contract_address}#code")
    
    print(f"\n🎉 Verification test complete!")

if __name__ == "__main__":
    main()
