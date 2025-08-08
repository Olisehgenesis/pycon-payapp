#!/bin/bash

# Payment Splitter DApp Setup Script
# This script sets up the development environment

set -e

echo "🚀 PAYMENT SPLITTER DAPP - SETUP SCRIPT 🚀"
echo "=========================================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or 3.10"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python version: $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Initialize Brownie if not already done
if [ ! -f "brownie-config.yaml" ]; then
    echo "🔧 Initializing Brownie..."
    brownie init
fi

# Add Celo Alfajores network
echo "🌐 Adding Celo Alfajores network..."
brownie networks add Celo alfajores host=https://alfajores-forno.celo-testnet.org chainid=44787 explorer=https://alfajores.celoscan.io 2>/dev/null || echo "Network already exists"

echo ""
echo "✅ SETUP COMPLETE!"
echo "=================="
echo ""
echo "📋 Next steps:"
echo "1. Create account: python scripts/create_account.py"
echo "2. Get test CELO: https://faucet.celo.org/"
echo "3. Deploy contract: brownie run deploy --network alfajores"
echo "4. Create payment: brownie run create_payment --network alfajores"
echo "5. Pay invoice: brownie run pay_invoice --network alfajores"
echo ""
echo "🔗 Useful links:"
echo "• Celo Faucet: https://faucet.celo.org/"
echo "• Alfajores Explorer: https://alfajores.celoscan.io/"
echo "• Brownie Docs: https://eth-brownie.readthedocs.io/"
echo ""
echo "🎉 Ready to build your Payment Splitter DApp!"
