#!/usr/bin/env python3
"""
Demo Script for Payment Splitter DApp
Shows a complete workflow example
"""

import os
from brownie import PaymentSplitter, accounts, network, Wei
from dotenv import load_dotenv

def main():
    """Demo the complete payment splitter workflow"""
    
    print("🎬 PAYMENT SPLITTER DAPP - DEMO 🎬")
    print("=" * 50)
    print("This demo shows a complete workflow:")
    print("1. Deploy contract")
    print("2. Create payment split")
    print("3. Pay invoices")
    print("4. Automatic distribution")
    print("=" * 50)
    
    # Load environment
    load_dotenv()
    
    # Get account
    if os.getenv("PRIVATE_KEY"):
        account = accounts.add(os.getenv("PRIVATE_KEY"))
    else:
        print("❌ No PRIVATE_KEY found in .env file")
        print("Run: python scripts/create_account.py first")
        return
    
    print(f"\n👤 Account: {account}")
    print(f"💰 Balance: {account.balance() / 1e18:.4f} CELO")
    
    if account.balance() == 0:
        print("❌ No CELO balance. Get test CELO from: https://faucet.celo.org/")
        return
    
    # Step 1: Deploy contract
    print(f"\n📦 STEP 1: Deploying contract...")
    payment_splitter = PaymentSplitter.deploy({"from": account})
    print(f"✅ Contract deployed at: {payment_splitter.address}")
    
    # Step 2: Create payment split
    print(f"\n💰 STEP 2: Creating payment split...")
    
    # Example: Dinner at Cafe Javas
    description = "Dinner at Cafe Javas - 4 people"
    recipients = [
        "0x70997970C51812dc3A010C7d01b50e0d17dc79C8",  # Alice
        "0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC",  # Bob
        "0x90F79bf6EB2c4f870365E785982E1f101E93b906",  # Carol
        "0x15d34AAf54267DB7D7c367839AAf71A00a2C6A65"   # David
    ]
    percentages = [30, 25, 25, 20]  # Must add up to 100
    total_amount = Wei("0.05 ether")  # 0.05 CELO
    
    tx = payment_splitter.createPayment(
        description,
        recipients,
        percentages,
        total_amount,
        {"from": account}
    )
    
    payment_id = tx.events['PaymentCreated']['paymentId']
    print(f"✅ Payment split created! ID: {payment_id}")
    
    # Step 3: Show payment details
    print(f"\n📋 PAYMENT DETAILS:")
    payment = payment_splitter.getPayment(payment_id)
    print(f"Description: {payment[0]}")
    print(f"Total Amount: {payment[3] / 1e18:.4f} CELO")
    print(f"Collected: {payment[4] / 1e18:.4f} CELO")
    print(f"Status: {'Active' if payment[5] else 'Completed'}")
    
    print(f"\n👥 Recipients:")
    for i, recipient in enumerate(payment[1]):
        celo_amount = payment[3] * payment[2][i] / (100 * 1e18)
        print(f"  {recipient[:6]}...: {payment[2][i]}% ({celo_amount:.4f} CELO)")
    
    # Step 4: Simulate payments
    print(f"\n💸 STEP 3: Simulating payments...")
    
    # Create additional accounts for demo
    demo_accounts = [
        accounts.add(),  # Contributor 1
        accounts.add(),  # Contributor 2
        accounts.add(),  # Contributor 3
    ]
    
    # Fund demo accounts (in real scenario, they'd have their own CELO)
    print(f"Note: In real scenario, contributors would have their own CELO")
    print(f"For demo, we'll simulate payments from the main account")
    
    # Simulate payments
    contributions = [0.015, 0.0125, 0.0125]  # Partial payments
    
    for i, contribution in enumerate(contributions):
        print(f"\n💰 Payment {i+1}: {contribution} CELO")
        
        try:
            tx = payment_splitter.payInvoice(
                payment_id,
                {"from": account, "value": Wei(f"{contribution} ether")}
            )
            print(f"✅ Payment successful! TX: {tx.txid}")
            
            # Check if payment completed
            if 'PaymentCompleted' in tx.events:
                print(f"🎉 PAYMENT COMPLETED! All recipients paid!")
                break
                
        except Exception as e:
            print(f"❌ Payment failed: {str(e)}")
    
    # Final status
    print(f"\n📊 FINAL STATUS:")
    payment = payment_splitter.getPayment(payment_id)
    percentage_collected = (payment[4] / payment[3] * 100) if payment[3] > 0 else 0
    print(f"Collected: {payment[4] / 1e18:.4f} / {payment[3] / 1e18:.4f} CELO")
    print(f"Progress: {percentage_collected:.1f}%")
    print(f"Status: {'Active' if payment[5] else 'Completed'}")
    
    print(f"\n🎉 DEMO COMPLETE!")
    print(f"Contract: {payment_splitter.address}")
    print(f"Payment ID: {payment_id}")
    
    if network.show_active() != "development":
        explorer_url = f"https://alfajores.celoscan.io/address/{payment_splitter.address}"
        print(f"Explorer: {explorer_url}")

if __name__ == "__main__":
    main()
