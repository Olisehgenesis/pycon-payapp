#!/usr/bin/env python3
"""
Create Payment Script for Payment Splitter DApp
Creates a new payment split with recipients and percentages
"""

import os
from brownie import PaymentSplitter, accounts, network, Wei
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
    
    print(f"💰 PAYMENT SPLITTER - CREATE NEW SPLIT 💰")
    print(f"=" * 50)
    print(f"Creator: {account}")
    print(f"Network: {network.show_active()}")
    
    # Get contract address
    contract_address = input("\nEnter deployed PaymentSplitter contract address: ").strip()
    if not contract_address:
        print("❌ Contract address is required")
        return
    
    try:
        contract = PaymentSplitter.at(contract_address)
        print(f"✅ Connected to contract: {contract_address}")
    except Exception as e:
        print(f"❌ Failed to connect to contract: {str(e)}")
        return
    
    # Get payment details
    print(f"\n📝 PAYMENT DETAILS")
    description = input("Enter description (e.g., 'Dinner at Cafe Javas'): ").strip()
    if not description:
        print("❌ Description is required")
        return
    
    # Get total amount in CELO
    while True:
        try:
            total_celo = float(input("Enter total amount in CELO (e.g., 0.1): "))
            if total_celo <= 0:
                print("Amount must be greater than 0")
                continue
            total_amount = Wei(f"{total_celo} ether")
            break
        except ValueError:
            print("Please enter a valid number")
    
    # Get recipients and percentages
    recipients = []
    percentages = []
    
    print(f"\n👥 ADD RECIPIENTS")
    print(f"Enter recipient addresses and their share percentages")
    print(f"Type 'done' when finished")
    
    while True:
        recipient = input(f"\nEnter recipient address (or 'done' to finish): ").strip()
        if recipient.lower() == 'done':
            break
            
        try:
            # Validate address format (basic check)
            if not recipient.startswith('0x') or len(recipient) != 42:
                print("❌ Invalid address format. Should be 0x followed by 40 characters")
                continue
                
            percentage = int(input(f"Enter percentage for {recipient[:6]}... (0-100): "))
            if percentage <= 0 or percentage > 100:
                print("❌ Percentage must be between 1 and 100")
                continue
                
            recipients.append(recipient)
            percentages.append(percentage)
            
            current_total = sum(percentages)
            print(f"✅ Added: {recipient[:6]}... - {percentage}%")
            print(f"📊 Current total: {current_total}%")
            
            if current_total >= 100:
                print(f"🎯 Total reached 100% - stopping")
                break
                
        except ValueError:
            print("❌ Please enter a valid number for percentage")
    
    # Validate total percentage
    total_percentage = sum(percentages)
    if total_percentage != 100:
        print(f"❌ Total percentage is {total_percentage}%. Must equal 100%")
        return
    
    if len(recipients) == 0:
        print("❌ At least one recipient is required")
        return
    
    # Display summary
    print(f"\n📋 PAYMENT SUMMARY 📋")
    print(f"Description: {description}")
    print(f"Total Amount: {total_celo} CELO")
    print(f"Recipients:")
    for i, recipient in enumerate(recipients):
        celo_amount = total_celo * percentages[i] / 100
        print(f"  {recipient}: {percentages[i]}% ({celo_amount:.4f} CELO)")
    
    # Confirm creation
    confirm = input(f"\nCreate this payment split? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Payment creation cancelled")
        return
    
    # Create payment
    print(f"\n💳 Creating payment split...")
    try:
        tx = contract.createPayment(
            description,
            recipients,
            percentages,
            total_amount,
            {"from": account}
        )
        
        # Get payment ID from events
        payment_id = tx.events['PaymentCreated']['paymentId']
        
        print(f"\n✅ SUCCESS! Payment split created!")
        print(f"Payment ID: {payment_id}")
        print(f"Transaction: {tx.txid}")
        
        if network.show_active() != "development":
            explorer_url = f"https://alfajores.celoscan.io/tx/{tx.txid}"
            print(f"Explorer: {explorer_url}")
        
        print(f"\n📤 Share this Payment ID with contributors: {payment_id}")
        print(f"💡 Next: Run 'brownie run pay_invoice --network {network.show_active()}'")
        
    except Exception as e:
        print(f"❌ Failed to create payment: {str(e)}")
        return

if __name__ == "__main__":
    main()
