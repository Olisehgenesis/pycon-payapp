#!/usr/bin/env python3
"""
Payment Splitter Flask App
A beautiful web interface for the PaymentSplitter DApp
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import os
from dotenv import load_dotenv
from web3 import Web3
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Contract configuration
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS', '0x074adfDF9e5330d4fB63A33C84217E338c47C03A')
CELO_RPC_URL = "https://alfajores-forno.celo-testnet.org"
EXPLORER_URL = "https://alfajores.celoscan.io"

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(CELO_RPC_URL))

# Contract ABI (simplified for the web interface)
CONTRACT_ABI = [
    {
        "inputs": [
            {"internalType": "string", "name": "_description", "type": "string"},
            {"internalType": "address[]", "name": "_recipients", "type": "address[]"},
            {"internalType": "uint256[]", "name": "_percentages", "type": "uint256[]"},
            {"internalType": "uint256", "name": "_totalAmount", "type": "uint256"}
        ],
        "name": "createPayment",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "_paymentId", "type": "uint256"}],
        "name": "payInvoice",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "_paymentId", "type": "uint256"}],
        "name": "getPayment",
        "outputs": [
            {"internalType": "string", "name": "description", "type": "string"},
            {"internalType": "address[]", "name": "recipients", "type": "address[]"},
            {"internalType": "uint256[]", "name": "percentages", "type": "uint256[]"},
            {"internalType": "uint256", "name": "totalAmount", "type": "uint256"},
            {"internalType": "uint256", "name": "collectedAmount", "type": "uint256"},
            {"internalType": "bool", "name": "isActive", "type": "bool"},
            {"internalType": "address", "name": "creator", "type": "address"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "nextPaymentId",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    }
]

# Initialize contract
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

@app.route('/')
def index():
    """Home page with payment splitter interface"""
    try:
        # Get total payments created
        total_payments = contract.functions.nextPaymentId().call()
        return render_template('index.html', 
                             total_payments=total_payments,
                             contract_address=CONTRACT_ADDRESS,
                             explorer_url=f"{EXPLORER_URL}/address/{CONTRACT_ADDRESS}")
    except Exception as e:
        flash(f"Error connecting to contract: {str(e)}", "error")
        return render_template('index.html', 
                             total_payments=0,
                             contract_address=CONTRACT_ADDRESS,
                             explorer_url=f"{EXPLORER_URL}/address/{CONTRACT_ADDRESS}")

@app.route('/create_payment', methods=['GET', 'POST'])
def create_payment():
    """Create a new payment split"""
    if request.method == 'POST':
        try:
            description = request.form['description']
            total_amount = float(request.form['total_amount'])
            recipients = request.form.getlist('recipients[]')
            percentages = [int(p) for p in request.form.getlist('percentages[]')]
            
            # Validate inputs
            if not description or total_amount <= 0:
                flash("Please provide valid description and amount", "error")
                return redirect(url_for('create_payment'))
            
            if len(recipients) == 0:
                flash("Please add at least one recipient", "error")
                return redirect(url_for('create_payment'))
            
            if sum(percentages) != 100:
                flash("Percentages must add up to 100%", "error")
                return redirect(url_for('create_payment'))
            
            # Convert to Wei
            total_amount_wei = w3.to_wei(total_amount, 'ether')
            
            # Prepare transaction data for MetaMask
            tx_data = contract.functions.createPayment(
                description,
                recipients,
                percentages,
                total_amount_wei
            ).build_transaction({
                'from': '0x0000000000000000000000000000000000000000',  # Will be replaced by MetaMask
                'gas': 2000000,
                'gasPrice': w3.eth.gas_price,
                'nonce': 0  # Will be replaced by MetaMask
            })
            
            # Return transaction data for frontend to sign with MetaMask
            return jsonify({
                'success': True,
                'tx_data': {
                    'to': CONTRACT_ADDRESS,
                    'data': tx_data['data'],
                    'gas': hex(2000000),
                    'gasPrice': hex(w3.eth.gas_price)
                }
            })
            
        except Exception as e:
            flash(f"Error creating payment: {str(e)}", "error")
            return redirect(url_for('create_payment'))
    
    return render_template('create_payment.html', contract_address=CONTRACT_ADDRESS)

@app.route('/pay_invoice', methods=['GET', 'POST'])
def pay_invoice():
    """Pay an invoice"""
    if request.method == 'POST':
        try:
            payment_id = int(request.form['payment_id'])
            amount = float(request.form['amount'])
            
            # Convert to Wei
            amount_wei = w3.to_wei(amount, 'ether')
            
            # Prepare transaction data for MetaMask
            tx_data = contract.functions.payInvoice(payment_id).build_transaction({
                'from': '0x0000000000000000000000000000000000000000',  # Will be replaced by MetaMask
                'value': amount_wei,
                'gas': 2000000,
                'gasPrice': w3.eth.gas_price,
                'nonce': 0  # Will be replaced by MetaMask
            })
            
            # Return transaction data for frontend to sign with MetaMask
            return jsonify({
                'success': True,
                'tx_data': {
                    'to': CONTRACT_ADDRESS,
                    'data': tx_data['data'],
                    'value': hex(amount_wei),
                    'gas': hex(2000000),
                    'gasPrice': hex(w3.eth.gas_price)
                }
            })
            
        except Exception as e:
            flash(f"Error processing payment: {str(e)}", "error")
            return redirect(url_for('pay_invoice'))
    
    return render_template('pay_invoice.html', contract_address=CONTRACT_ADDRESS)

@app.route('/view_payment/<int:payment_id>')
def view_payment(payment_id):
    """View payment details"""
    try:
        payment = contract.functions.getPayment(payment_id).call()
        
        # Convert from Wei to CELO
        total_amount_celo = w3.from_wei(payment[3], 'ether')
        collected_amount_celo = w3.from_wei(payment[4], 'ether')
        
        payment_data = {
            'id': payment_id,
            'description': payment[0],
            'recipients': payment[1],
            'percentages': payment[2],
            'total_amount': total_amount_celo,
            'collected_amount': collected_amount_celo,
            'is_active': payment[5],
            'creator': payment[6],
            'progress': (collected_amount_celo / total_amount_celo * 100) if total_amount_celo > 0 else 0
        }
        
        return render_template('view_payment.html', payment=payment_data, contract_address=CONTRACT_ADDRESS)
        
    except Exception as e:
        flash(f"Error loading payment: {str(e)}", "error")
        return redirect(url_for('index'))

@app.route('/api/payments')
def api_payments():
    """API endpoint to get all payments"""
    try:
        total_payments = contract.functions.nextPaymentId().call()
        payments = []
        
        for i in range(total_payments):
            try:
                payment = contract.functions.getPayment(i).call()
                total_amount_celo = w3.from_wei(payment[3], 'ether')
                collected_amount_celo = w3.from_wei(payment[4], 'ether')
                
                payments.append({
                    'id': i,
                    'description': payment[0],
                    'total_amount': total_amount_celo,
                    'collected_amount': collected_amount_celo,
                    'is_active': payment[5],
                    'progress': (collected_amount_celo / total_amount_celo * 100) if total_amount_celo > 0 else 0
                })
            except:
                continue
        
        return jsonify(payments)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
