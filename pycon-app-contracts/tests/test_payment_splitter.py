#!/usr/bin/env python3
"""
Test Payment Splitter Contract
Unit tests for the PaymentSplitter smart contract
"""

import pytest
from brownie import PaymentSplitter, accounts, Wei

@pytest.fixture
def payment_splitter():
    """Deploy PaymentSplitter contract for testing"""
    return PaymentSplitter.deploy({"from": accounts[0]})

@pytest.fixture
def alice():
    """Test account Alice"""
    return accounts[0]

@pytest.fixture
def bob():
    """Test account Bob"""
    return accounts[1]

@pytest.fixture
def carol():
    """Test account Carol"""
    return accounts[2]

def test_create_payment(payment_splitter, alice, bob, carol):
    """Test creating a payment split"""
    description = "Dinner at Cafe Javas"
    recipients = [alice, bob, carol]
    percentages = [40, 30, 30]  # Must add up to 100
    total_amount = Wei("0.1 ether")
    
    # Create payment
    tx = payment_splitter.createPayment(
        description,
        recipients,
        percentages,
        total_amount,
        {"from": alice}
    )
    
    # Check payment was created
    payment_id = tx.events['PaymentCreated']['paymentId']
    assert payment_id == 0
    
    # Get payment details
    payment = payment_splitter.getPayment(payment_id)
    assert payment[0] == description  # description
    assert payment[1] == recipients   # recipients
    assert payment[2] == percentages  # percentages
    assert payment[3] == total_amount # totalAmount
    assert payment[4] == 0           # collectedAmount
    assert payment[5] == True        # isActive
    assert payment[6] == alice       # creator

def test_pay_invoice(payment_splitter, alice, bob, carol):
    """Test paying an invoice"""
    # Create payment first
    description = "Group lunch"
    recipients = [alice, bob]
    percentages = [60, 40]
    total_amount = Wei("0.05 ether")
    
    tx = payment_splitter.createPayment(
        description,
        recipients,
        percentages,
        total_amount,
        {"from": alice}
    )
    payment_id = tx.events['PaymentCreated']['paymentId']
    
    # Carol pays her share
    contribution = Wei("0.02 ether")
    tx = payment_splitter.payInvoice(
        payment_id,
        {"from": carol, "value": contribution}
    )
    
    # Check contribution was recorded
    recorded_contribution = payment_splitter.getContribution(payment_id, carol)
    assert recorded_contribution == contribution
    
    # Check payment status
    payment = payment_splitter.getPayment(payment_id)
    assert payment[4] == contribution  # collectedAmount
    assert payment[5] == True         # still active

def test_payment_completion(payment_splitter, alice, bob, carol):
    """Test payment completion and distribution"""
    # Create payment
    description = "Small bill"
    recipients = [alice, bob]
    percentages = [50, 50]
    total_amount = Wei("0.02 ether")
    
    tx = payment_splitter.createPayment(
        description,
        recipients,
        percentages,
        total_amount,
        {"from": alice}
    )
    payment_id = tx.events['PaymentCreated']['paymentId']
    
    # Get initial balances
    alice_initial = alice.balance()
    bob_initial = bob.balance()
    
    # Carol pays the full amount
    tx = payment_splitter.payInvoice(
        payment_id,
        {"from": carol, "value": total_amount}
    )
    
    # Check payment completed event
    assert 'PaymentCompleted' in tx.events
    
    # Check payment is no longer active
    payment = payment_splitter.getPayment(payment_id)
    assert payment[5] == False  # isActive = False
    
    # Check balances increased (distribution happened)
    assert alice.balance() > alice_initial
    assert bob.balance() > bob_initial

def test_invalid_percentages(payment_splitter, alice, bob):
    """Test that percentages must add up to 100"""
    description = "Invalid payment"
    recipients = [alice, bob]
    percentages = [60, 30]  # Only 90%, should fail
    total_amount = Wei("0.1 ether")
    
    with pytest.raises(Exception):
        payment_splitter.createPayment(
            description,
            recipients,
            percentages,
            total_amount,
            {"from": alice}
        )

def test_double_payment_prevention(payment_splitter, alice, bob, carol):
    """Test that same person cannot pay twice"""
    # Create payment
    description = "Test payment"
    recipients = [alice, bob]
    percentages = [50, 50]
    total_amount = Wei("0.1 ether")
    
    tx = payment_splitter.createPayment(
        description,
        recipients,
        percentages,
        total_amount,
        {"from": alice}
    )
    payment_id = tx.events['PaymentCreated']['paymentId']
    
    # Carol pays first time
    payment_splitter.payInvoice(
        payment_id,
        {"from": carol, "value": Wei("0.05 ether")}
    )
    
    # Carol tries to pay again - should fail
    with pytest.raises(Exception):
        payment_splitter.payInvoice(
            payment_id,
            {"from": carol, "value": Wei("0.05 ether")}
        )

def test_payment_id_increment(payment_splitter, alice, bob):
    """Test that payment IDs increment correctly"""
    # Create first payment
    tx1 = payment_splitter.createPayment(
        "First payment",
        [alice],
        [100],
        Wei("0.01 ether"),
        {"from": alice}
    )
    payment_id_1 = tx1.events['PaymentCreated']['paymentId']
    assert payment_id_1 == 0
    
    # Create second payment
    tx2 = payment_splitter.createPayment(
        "Second payment",
        [bob],
        [100],
        Wei("0.01 ether"),
        {"from": alice}
    )
    payment_id_2 = tx2.events['PaymentCreated']['paymentId']
    assert payment_id_2 == 1
    
    # Check nextPaymentId
    assert payment_splitter.nextPaymentId() == 2
