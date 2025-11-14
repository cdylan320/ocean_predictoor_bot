# Ocean Predictoor Bot - Setup Guide

This guide covers the complete setup and usage of your predictoor bot on Windows.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Configuration](#environment-configuration)
3. [Available Commands](#available-commands)
4. [Running Your Bot](#running-your-bot)
5. [Monitoring](#monitoring)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

✅ **You've already completed:**
- Python 3.12 installed
- Virtual environment created and activated
- Dependencies installed
- PredSubmitterMgr contract deployed on testnet

---

## Environment Configuration

### 1. Load Environment Variables

Every time you start a new terminal session, run:

```bash
# Navigate to project directory
cd D:/Mine/Projects/rewards/ocean/pdr-backend

# Activate virtual environment
source venv/Scripts/activate

# Load your environment configuration
source pdr_config.env
```

**Or manually:**

```bash
export PRIVATE_KEY=0xYOUR_PRIVATE_KEY_HERE
export PATH=$PATH:.
```

### 2. Your Configuration Summary

**Wallet:**
- Address: `0xYOUR_WALLET_ADDRESS_HERE`
- Private Key: Stored in `pdr_config.env` (create this file with your own key)

**Deployed Contracts:**
- Testnet PredSubmitterMgr: `0x73129dFaf1b29Ca024f2b92db7776316f10dC5D1`

**Balances:**
- Testnet: 149.68 ROSE ✅
- Mainnet: 0 ROSE ❌ (need to fund for mainnet use)

---

## Available Commands

### Check Available Prediction Feeds

```bash
# Mainnet feeds (20 active feeds)
python list_feeds.py mainnet

# Testnet feeds (currently none available)
python list_feeds.py testnet
```

### Run Simulation (Works Offline)

```bash
pdr sim my_ppss.yaml
```

- Trains AI model on historical data
- Simulates predictions and trading
- Outputs results to console and `logs/`
- Creates state files in `sim_state/`

### View Simulation Dashboard

```bash
# In a separate terminal
pdr sim_plots
```

- Opens dashboard at http://127.0.0.1:8050/
- Shows charts and performance metrics
- Auto-detects latest simulation run

### Run Live Predictoor Bot

#### On Testnet (Currently No Feeds Available)

```bash
pdr predictoor my_ppss.yaml sapphire-testnet
```

⚠️ **Note:** Testnet currently has no active prediction feeds. Use simulation mode instead.

#### On Mainnet (20 Active Feeds)

```bash
# Make sure you have funds first!
pdr predictoor my_ppss.yaml sapphire-mainnet
```

**Requirements:**
- ROSE tokens for gas fees (buy on exchanges)
- OCEAN tokens for staking predictions (get from DEX)

### Check Your Predictions

```bash
python query_my_predictions.py
```

Shows your recent predictions, stakes, and payouts from the blockchain.

### Check Wallet Balances

```bash
# Testnet balance
python -c "from web3 import Web3; w3=Web3(Web3.HTTPProvider('https://testnet.sapphire.oasis.dev')); addr='0xYOUR_WALLET_ADDRESS'; print(f'{w3.from_wei(w3.eth.get_balance(addr), \"ether\")} ROSE')"

# Mainnet balance
python -c "from web3 import Web3; w3=Web3(Web3.HTTPProvider('https://sapphire.oasis.io')); addr='0xYOUR_WALLET_ADDRESS'; print(f'{w3.from_wei(w3.eth.get_balance(addr), \"ether\")} ROSE')"
```

---

## Running Your Bot

### Option 1: Simulation Mode (Recommended for Testing)

This works completely offline with no blockchain transactions:

```bash
# Load environment
source pdr_config.env

# Run simulation
pdr sim my_ppss.yaml

# View results in dashboard (separate terminal)
pdr sim_plots
```

**Results:**
- Console output with accuracy metrics
- Log files in `logs/out_<timestamp>.txt`
- State files in `sim_state/<run_id>/`
- Dashboard at http://127.0.0.1:8050/

### Option 2: Live on Mainnet

**Before you start:**

1. **Fund Your Wallet with ROSE** (for gas fees)
   - Buy ROSE on: Binance, KuCoin, Gate.io, Kraken
   - Send to: `0xYOUR_WALLET_ADDRESS`
   - Network: Oasis Sapphire (NOT Ethereum!)
   - Amount needed: ~10-50 ROSE depending on activity

2. **Get OCEAN Tokens** (for staking)
   - Bridge from Ethereum or buy on Sapphire DEX
   - Amount: Based on your `stake_amount` setting (currently 5 OCEAN)

3. **Deploy PredSubmitterMgr on Mainnet** (one-time)
   ```bash
   source pdr_config.env
   pdr deploy_pred_submitter_mgr my_ppss.yaml sapphire-mainnet
   ```
   
   Save the contract address to `pdr_config.env`:
   ```bash
   export PRED_SUBMITTER_MGR_MAINNET=0xYOUR_CONTRACT_ADDRESS
   ```

4. **Run Your Bot**
   ```bash
   source pdr_config.env
   pdr predictoor my_ppss.yaml sapphire-mainnet
   ```

---

## Monitoring

### 1. Bot Console Output

The bot logs to console in real-time:
- Predictions being made
- Transactions being submitted
- Success/failure status
- Accuracy metrics

### 2. Log Files

Check `logs/` directory:
```bash
# View latest log
ls -lt logs/ | head -5
cat logs/out_<timestamp>.txt
```

### 3. Blockchain Explorer

**Testnet:**
- Explorer: https://explorer.oasis.io/testnet/sapphire
- Your Address: https://explorer.oasis.io/testnet/sapphire/address/0xYOUR_WALLET_ADDRESS

**Mainnet:**
- Explorer: https://explorer.oasis.io/mainnet/sapphire
- Your Address: https://explorer.oasis.io/mainnet/sapphire/address/0xYOUR_WALLET_ADDRESS

### 4. Query Predictions Programmatically

```bash
python query_my_predictions.py
```

This queries the Ocean Protocol subgraph for your prediction history.

### 5. Ocean Protocol Dashboard (Future)

The Ocean Protocol team may provide an official dashboard at:
- https://predictoor.ai (check if available)
- https://df.oceandao.org (Data Farming dashboard)

---

## Troubleshooting

### Command Not Found: `pdr`

```bash
export PATH=$PATH:.
# or
source pdr_config.env
```

### Module Not Found Errors

```bash
source venv/Scripts/activate
pip install -r requirements.txt
```

### Private Key Error

Make sure your private key is exported:
```bash
export PRIVATE_KEY=0xYOUR_PRIVATE_KEY_HERE
# or
source pdr_config.env
```

### Insufficient Balance Error

You need ROSE tokens for gas. Check balance:
```bash
python -c "from web3 import Web3; w3=Web3(Web3.HTTPProvider('https://sapphire.oasis.io')); print(f'{w3.from_wei(w3.eth.get_balance(\"0xYOUR_WALLET_ADDRESS\"), \"ether\")} ROSE')"
```

### No Feeds Found

This means there are no active prediction feeds on that network.
- **Testnet:** Currently no feeds available. Use simulation mode.
- **Mainnet:** Run `python list_feeds.py mainnet` to see 20 active feeds.

### Subgraph Down (503 Error)

The Ocean Protocol subgraph service is temporarily unavailable. Wait and try again later.

### Binance API Blocked

You're in a restricted location for Binance. Your config already uses Kraken instead.

### Simulation "Too Little Data" Error

Your config is already optimized for the available data (200 epochs training/testing).

### Dashboard Path Error (Windows)

This has been fixed in your installation. If you see path errors, make sure you're using the updated `sim_plotter.py`.

---

## Quick Reference

### Every Terminal Session

```bash
cd D:/Mine/Projects/rewards/ocean/pdr-backend
source venv/Scripts/activate
source pdr_config.env
```

### Simulation Workflow

```bash
pdr sim my_ppss.yaml          # Terminal 1: Run simulation
pdr sim_plots                 # Terminal 2: View dashboard
```

### Live Bot Workflow (Mainnet)

```bash
# Check feeds
python list_feeds.py mainnet

# Check balance
python -c "from web3 import Web3; w3=Web3(Web3.HTTPProvider('https://sapphire.oasis.io')); print(f'{w3.from_wei(w3.eth.get_balance(\"0xYOUR_WALLET_ADDRESS\"), \"ether\")} ROSE')"

# Run bot
pdr predictoor my_ppss.yaml sapphire-mainnet

# Monitor predictions (separate terminal)
python query_my_predictions.py
```

---

## Important Files

- **`my_ppss.yaml`** - Your bot configuration
- **`pdr_config.env`** - Environment variables (private key, etc.)
- **`list_feeds.py`** - Script to list available prediction feeds (if you create one)
- **`logs/`** - Bot execution logs
- **`sim_state/`** - Simulation state files for dashboard
- **`lake_data/`** - Cached historical price data

---

## Support & Resources

- **Ocean Protocol Docs:** https://docs.oceanprotocol.com/
- **Predictoor Docs:** https://docs.oceanprotocol.com/predictoor
- **Ocean Discord:** https://discord.gg/oceanprotocol
- **Oasis Explorer (Testnet):** https://explorer.oasis.io/testnet/sapphire
- **Oasis Explorer (Mainnet):** https://explorer.oasis.io/mainnet/sapphire

---

## Security Notes

⚠️ **CRITICAL:**
- Never share your `PRIVATE_KEY`
- Never commit `pdr_config.env` to git (already in `.gitignore`)
- Create `pdr_config.env` with your own private key
- If compromised, transfer funds immediately and use a new wallet

---

## What We Fixed Today

1. ✅ Python version (3.14 → 3.12)
2. ✅ Missing dependencies
3. ✅ Binance API blocked (switched to Kraken)
4. ✅ Simulation data requirements (reduced epochs)
5. ✅ Windows path handling bug (sim_plotter.py)
6. ✅ Network name mapping (oasis_sapphire_testnet)
7. ✅ Missing commands (created list_feeds.py)
8. ✅ Environment configuration (created pdr_config.env)

**Your bot is now fully operational on Windows! 🎉**

