#!/usr/bin/env python3
"""
Pay Invoice Script for Payment Splitter DApp
Pay your share of a payment split
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
    
    print(f"💸 PAYMENT SPLITTER - PAY YOUR SHARE 💸")
    print(f"=" * 50)
    print(f"Your address: {account}")
    print(f"Network: {network.show_active()}")
    print(f"Balance: {account.balance() / 1e18:.4f} CELO")
    
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
    
    # Get payment ID
    try:
        payment_id = int(input("\nEnter Payment ID: "))
    except ValueError:
        print("❌ Payment ID must be a number")
        return
    
    # Get payment details
    try:
        payment_details = contract.getPayment(payment_id)
        description = payment_details[0]
        recipients = payment_details[1]
        percentages = payment_details[2]
        total_amount = payment_details[3]
        collected_amount = payment_details[4]
        is_active = payment_details[5]
        creator = payment_details[6]
    except Exception as e:
        print(f"❌ Payment ID {payment_id} not found: {str(e)}")
        return
    
    if not is_active:
        print(f"❌ Payment {payment_id} is no longer active")
        return
    
    # Check if already paid
    has_paid = contract.hasPaid(payment_id, account)
    if has_paid:
        contribution = contract.getContribution(payment_id, account)
        print(f"✅ You already paid {contribution / 1e18:.4f} CELO for this bill")
        show_payment_status(contract, payment_id)
        return
    
    # Display payment details
    print(f"\n📋 PAYMENT DETAILS 📋")
    print(f"Description: {description}")
    print(f"Total Amount: {total_amount / 1e18:.4f} CELO")
    print(f"Collected: {collected_amount / 1e18:.4f} CELO")
    print(f"Remaining: {(total_amount - collected_amount) / 1e18:.4f} CELO")
    print(f"Created by: {creator}")
    
    print(f"\n💰 RECIPIENTS:")
    for i, recipient in enumerate(recipients):
        celo_amount = total_amount * percentages[i] / (100 * 1e18)
        print(f"  {recipient}: {percentages[i]}% ({celo_amount:.4f} CELO)")
    
    # Get payment amount
    while True:
        try:
            pay_celo = float(input(f"\nHow much CELO do you want to contribute? "))
            if pay_celo <= 0:
                print("❌ Amount must be greater than 0")
                continue
            pay_amount = Wei(f"{pay_celo} ether")
            break
        except ValueError:
            print("❌ Please enter a valid number")
    
    # Check balance
    if account.balance() < pay_amount:
        print(f"❌ Insufficient balance. You have {account.balance() / 1e18:.4f} CELO")
        print(f"Get more CELO from: https://faucet.celo.org/")
        return
    
    # Confirm payment
    print(f"\n💳 PAYMENT CONFIRMATION 💳")
    print(f"You will pay: {pay_celo} CELO")
    print(f"For: {description}")
    print(f"Your balance after: {(account.balance() - pay_amount) / 1e18:.4f} CELO")
    
    confirm = input("Confirm payment? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Payment cancelled")
        return
    
    # Make payment
    print(f"\n💸 Processing payment...")
    try:
        tx = contract.payInvoice(payment_id, {"from": account, "value": pay_amount})
        
        print(f"\n✅ SUCCESS! Payment sent!")
        print(f"Transaction: {tx.txid}")
        
        if network.show_active() != "development":
            explorer_url = f"https://alfajores.celoscan.io/tx/{tx.txid}"
            print(f"Explorer: {explorer_url}")
        
        # Check if payment completed
        if 'PaymentCompleted' in tx.events:
            print(f"🎉 PAYMENT SPLIT COMPLETED! All recipients have been paid.")
        
        # Show updated status
        show_payment_status(contract, payment_id)
        
    except Exception as e:
        print(f"❌ Payment failed: {str(e)}")
        return

def show_payment_status(contract, payment_id):
    """Display current payment status"""
    try:
        payment_details = contract.getPayment(payment_id)
        total_amount = payment_details[3]
        collected_amount = payment_details[4]
        is_active = payment_details[5]
        
        print(f"\n📊 PAYMENT STATUS 📊")
        percentage_collected = (collected_amount / total_amount * 100) if total_amount > 0 else 0
        print(f"Progress: {collected_amount / 1e18:.4f} / {total_amount / 1e18:.4f} CELO ({percentage_collected:.1f}%)")
        print(f"Status: {'Active' if is_active else 'Completed'}")
        
        if is_active:
            remaining = total_amount - collected_amount
            print(f"Remaining: {remaining / 1e18:.4f} CELO")
        else:
            print(f"✅ Payment completed and distributed!")
            
    except Exception as e:
        print(f"❌ Could not get payment status: {str(e)}")

if __name__ == "__main__":
    main()
