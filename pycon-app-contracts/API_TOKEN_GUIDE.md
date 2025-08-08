# CeloScan API Token Guide 🔑
## For Automatic Contract Verification

## Why You Need an API Token

Automatic contract verification requires an API token from CeloScan. This allows Brownie to:
- **Verify contracts automatically** after deployment
- **Upload source code** to the blockchain explorer
- **Create verified contract pages** on CeloScan

## How to Get a CeloScan API Token

### Step 1: Visit CeloScan
1. Go to: https://celoscan.io/apis
2. Click **"Sign Up"** or **"Login"**

### Step 2: Create Account
1. **Sign up** with your email
2. **Verify your email** address
3. **Login** to your account

### Step 3: Generate API Key
1. Go to **"API Keys"** section
2. Click **"Add"** or **"Create API Key"**
3. Give it a name (e.g., "Brownie Verification")
4. Copy the generated API key

### Step 4: Add to Your Project
```bash
# Run the setup script
python scripts/setup_verification.py

# Enter your API token when prompted
```

Or manually add to `.env`:
```bash
echo "CELOSCAN_TOKEN=your_api_token_here" >> .env
```

## Verification Options

### Option 1: Automatic (Recommended)
```bash
# Setup API token
python scripts/setup_verification.py

# Deploy with auto-verification
brownie run deploy --network alfajores
```

### Option 2: Manual Verification Script
```bash
# Deploy without auto-verification
brownie run deploy --network alfajores

# Verify manually
brownie run verify_contract --network alfajores
```

### Option 3: Manual on CeloScan
1. Deploy your contract
2. Visit: https://alfajores.celoscan.io/verifyContract
3. Enter contract address
4. Upload source code
5. Submit for verification

## API Token Security

### ✅ Safe to Share
- **Public API keys** are designed to be shared
- **No private keys** or sensitive data
- **Read-only access** to verification features

### ⚠️ Best Practices
- **Use different keys** for different projects
- **Monitor usage** in your CeloScan account
- **Rotate keys** periodically if needed

## Troubleshooting

### "API token not found"
```bash
# Check if token is set
echo $CELOSCAN_TOKEN

# Re-run setup
python scripts/setup_verification.py
```

### "Invalid API token"
- **Check spelling** of your API token
- **Regenerate** a new token on CeloScan
- **Update** your `.env` file

### "Rate limit exceeded"
- **Free tier** has rate limits
- **Wait** a few minutes and try again
- **Upgrade** to paid plan if needed

## Free vs Paid Plans

### Free Plan
- **100 API calls/day**
- **Basic verification**
- **Perfect for learning**

### Paid Plans
- **Higher rate limits**
- **Advanced features**
- **Priority support**

## Example Workflow

```bash
# 1. Setup environment
./setup.sh

# 2. Create account
python scripts/create_account.py

# 3. Setup verification (optional)
python scripts/setup_verification.py

# 4. Get test CELO
# Visit: https://faucet.celo.org/

# 5. Deploy with verification
brownie run deploy --network alfajores

# 6. View verified contract
# Visit the explorer link shown after deployment
```

## Benefits of Verification

### For Developers
- **Professional appearance**
- **Easier debugging**
- **Better documentation**

### For Users
- **Transparency** - see exactly what the contract does
- **Trust** - verified contracts are more trustworthy
- **Interaction** - use explorer to interact with contract

### For Community
- **Open source** - code is available for learning
- **Auditing** - security researchers can review
- **Collaboration** - others can build on your work

---

*API tokens make contract verification seamless and professional! 🔑✅*
