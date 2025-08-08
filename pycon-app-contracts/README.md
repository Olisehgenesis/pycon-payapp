# Payment Splitter DApp Tutorial 🇺🇬💰
## From Web2 to Web3 in 30 Minutes

**Target Audience:** Ugandan web2 developers familiar with Python  
**Time:** 30 minutes  
**Framework:** Brownie (Python-based Ethereum development)  
**Network:** Celo Alfajores Testnet  

---

## What We're Building 🏗️

**Payment Splitter App** - Split bills, rent, and group expenses on blockchain:
- **Create Payment**: Set up who gets what percentage  
- **Pay Invoice**: Contributors send their share automatically  
- Perfect for **roommates, group dinners, boda rides, utility bills**  
- Transparent and automatic - no arguments about money!  

**Real Uganda Use Cases:**
- Split rent among roommates in Kampala  
- Group dinner at Cafe Javas  
- Shared boda boda rides  
- Office lunch orders  
- Group shopping at Nakumatt  

---

## Quick Start 🚀

### 1. Setup Environment (5 minutes)
```bash
# Navigate to project
cd pycon-app

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install eth-brownie python-dotenv

# Initialize Brownie
brownie init

# Add Celo Alfajores network
brownie networks add Celo alfajores host=https://alfajores-forno.celo-testnet.org chainid=44787 explorer=https://alfajores.celoscan.io
```

### 2. Create Account (2 minutes)
```bash
# Create and save account to .env
python scripts/create_account.py
```

### 2.5. Setup Verification (Optional - 2 minutes)
```bash
# Setup API tokens for automatic verification
python scripts/setup_verification.py
```

### 3. Deploy Contract (3 minutes)
```bash
# Deploy to local network first
brownie console
>>> run("deploy")
>>> # Copy the contract address
>>> exit()

# Deploy to Celo Alfajores (with auto-verification)
brownie run deploy --network alfajores
```

### 4. Create Payment Split (10 minutes)
```bash
brownie run create_payment --network alfajores
# Enter contract address and payment details
```

### 5. Pay Your Share (10 minutes)
```bash
brownie run pay_invoice --network alfajores
# Enter contract address and payment ID
```

---

## Project Structure 📁

```
pycon-app/
├── contracts/
│   └── PaymentSplitter.sol      # Smart contract
├── scripts/
│   ├── create_account.py        # Create and save account
│   ├── deploy.py               # Deploy contract
│   ├── create_payment.py       # Create payment split
│   └── pay_invoice.py          # Pay your share
├── tests/
│   └── test_payment_splitter.py # Unit tests
├── .env                        # Account private key
├── brownie-config.yaml         # Brownie configuration
└── README.md                   # This file
```

---

## Smart Contract Overview 🧠

**Key Concepts:**
- **Structs**: Like Python classes for organizing data
- **Mappings**: Like Python dictionaries but on blockchain
- **payable**: Functions that can receive CELO
- **Events**: For logging activities (permanent records)

**Two Main Functions:**
1. **`createPayment()`** - Set up payment split with recipients and percentages
2. **`payInvoice()`** - Contributors pay their share and trigger distribution

**Why Blockchain Beats Traditional:**
- **No cash handling** (common problem in Uganda)
- **No trust issues** ("Did John really pay?")
- **Automatic calculations** (no math errors)
- **Permanent records** (blockchain proof)
- **Cross-border payments** (works anywhere)

---

## Real Uganda Example 🇺🇬

**Scenario: Group Dinner at Cafe Javas**
```python
# Alice creates the split
Description: "Dinner at Cafe Javas - 4 people"
Total: 0.05 CELO
Recipients:
  - Alice: 30% (ordered extra dessert)
  - Bob: 25% 
  - Carol: 25%
  - David: 20% (just had appetizer)

# Everyone pays their share
# Automatic distribution when total reached
```

---

## Network Configuration 🌐

### Celo Alfajores Testnet
- **RPC URL**: `https://alfajores-forno.celo-testnet.org`
- **Chain ID**: 44787
- **Explorer**: `https://alfajores.celoscan.io`
- **Faucet**: `https://faucet.celo.org/`

### Get Test CELO
1. Visit `https://faucet.celo.org/`
2. Select "Alfajores" network
3. Enter your wallet address
4. Receive test CELO instantly

---

## Contract Verification 🔍

### Automatic Verification
Your contract is automatically verified when deployed (requires API token):
```bash
# Setup API token first (optional)
python scripts/setup_verification.py

# Deploy with auto-verification
brownie run deploy --network alfajores
```

### Manual Verification
If auto-verification fails:
```bash
brownie run verify_contract --network alfajores
```

### View Verified Contract
After deployment, visit:
```
https://alfajores.celoscan.io/address/YOUR_CONTRACT_ADDRESS#code
```

## Troubleshooting 🔧

**Common Issues:**
- **"Insufficient funds"**: Get CELO from faucet
- **"Percentages must add up to 100"**: Check your math!
- **"Invalid address format"**: Use proper 0x... format
- **"Payment not active"**: Payment already completed
- **"Contract already verified"**: No action needed

**Environment Issues:**
- **Not activated**: Should see `(.venv)` in terminal
- **Python version**: Use Python 3.9 or 3.10 (Brownie compatibility)
- **Network issues**: Try again with different RPC endpoint

**Resources:**
- Celo Faucet: `https://faucet.celo.org/`
- Brownie Docs: `https://eth-brownie.readthedocs.io/`
- Solidity Docs: `https://docs.soliditylang.org/`

---

## Next Steps 🚀

**Extend the DApp:**
- Add deadlines for payments
- Support ERC20 tokens (USDC, etc.)
- Email notifications
- Mobile app
- Integration with M-Pesa

**Learn More:**
- DeFi protocols
- Multi-signature wallets
- Payment streaming
- Cross-chain payments

---

## Why This Matters for Uganda 🇺🇬

**Traditional Bill Splitting Problems:**
- Manual calculations
- Trust issues ("Did John pay?")
- Cash handling problems
- No transparency

**Our Blockchain Solution:**
- Automatic calculations
- Transparent payments
- No cash needed
- Immutable records
- Automatic distribution

**Perfect for Uganda:**
- **Group Transport**: Split boda boda rides
- **Shared Meals**: Divide restaurant bills
- **Rent Splitting**: Roommate expenses
- **Office Lunches**: Team food orders
- **Event Planning**: Group event costs

---

*Welcome to Web3 Payments! You've just built a decentralized payment splitter! 🎉💰*
