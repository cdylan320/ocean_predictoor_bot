# Ocean Predictoor Bot - Quick Start Guide

## 🚀 One-Command Bot Launcher

Instead of manually exporting environment variables every time, use the **launcher script**:

### Simple Commands

```bash
# Run simulation mode (no blockchain, uses Kraken data)
./run_bot.sh sim

# Run on testnet
./run_bot.sh testnet

# Run on mainnet (requires VPN for Binance)
./run_bot.sh mainnet

# Claim OCEAN rewards (from mainnet)
./run_bot.sh claim

# Claim ROSE rewards (from mainnet)
./run_bot.sh claim-rose
```

### What It Does Automatically

The `run_bot.sh` script:
1. ✅ Activates your virtual environment
2. ✅ Loads `PRIVATE_KEY` from `pdr_config.env`
3. ✅ Sets up PATH and all environment variables
4. ✅ Runs your bot
5. ✅ Shows colored status messages

---

## 📋 Your Bot Configuration

**Wallet:**
- Address: `0xYOUR_WALLET_ADDRESS`
- Balance: Check with explorer or web3 commands

**Settings:**
- Stake: 1 OCEAN per prediction
- Feed: BTC/USDT 5m
- Network: Mainnet

**Deployed Contracts:**
- Testnet: `0x73129dFaf1b29Ca024f2b92db7776316f10dC5D1`
- Mainnet: `0xd1F3FE129D7feC87d4370CeE87C9B8f41ddF291f`

---

## ⚠️ Important: Binance API Blocked

Your location is blocked by Binance. **Solutions:**

### Option 1: Use VPN (Recommended for Mainnet)
1. Install a VPN (ProtonVPN, NordVPN, ExpressVPN)
2. Connect to allowed region (EU, US, most of Asia)
3. Run: `./run_bot.sh mainnet`

### Option 2: Use Simulation Mode (No VPN Needed)
```bash
./run_bot.sh sim
```
- Uses Kraken (works in your location)
- No blockchain transactions
- Perfect for testing

---

## 🎯 Why You Need to Source the Env File

**Environment variables are session-specific:**
- They only exist in the current terminal
- They're cleared when you close the terminal
- They don't persist between sessions

**The `pdr_config.env` file is just a text file** - it doesn't automatically apply its contents. You must **source** it (load it into the current session) using:
```bash
source pdr_config.env
```

**The launcher script (`run_bot.sh`) does this automatically for you!**

---

## 📝 Manual Method (If You Prefer)

If you want to run commands manually instead of using the launcher:

```bash
# Every new terminal session, run these:
cd D:/Mine/Projects/rewards/ocean/pdr-backend
source venv/Scripts/activate
source pdr_config.env

# Then run your bot:
pdr predictoor my_ppss.yaml sapphire-mainnet
```

---

## 🔍 Check Your Setup

```bash
# Check if environment is loaded
echo $PRIVATE_KEY  # Should show your key

# Check wallet balance (Testnet)
python -c "from web3 import Web3; w3=Web3(Web3.HTTPProvider('https://testnet.sapphire.oasis.dev')); print(f'{w3.from_wei(w3.eth.get_balance(\"0xYOUR_WALLET_ADDRESS\"), \"ether\")} ROSE')"

# Check wallet balance (Mainnet)
python -c "from web3 import Web3; w3=Web3(Web3.HTTPProvider('https://sapphire.oasis.io')); print(f'{w3.from_wei(w3.eth.get_balance(\"0xYOUR_WALLET_ADDRESS\"), \"ether\")} ROSE')"

# List available feeds
python list_feeds.py mainnet
```

---

## 🐛 Troubleshooting

### Error: "Web3Config object has no attribute 'owner'"
**Cause:** `PRIVATE_KEY` not set
**Fix:** Use `./run_bot.sh` or manually `source pdr_config.env`

### Error: "Service unavailable from restricted location" (Binance)
**Cause:** Binance blocks your region
**Fix:** Use VPN or run simulation mode

### Error: "pdr: command not found"
**Cause:** `PATH` not set or not in project directory
**Fix:** Use `./run_bot.sh` which handles this automatically

### Error: "No feeds found"
**Cause:** Looking for wrong exchange (Kraken vs Binance)
**Fix:** Already fixed in your config (changed to Binance for mainnet)

### Error: "ValueError: when sending a str, it must be a hex string. Got: 'DeployNewMgr'"
**Cause:** Config file has placeholder instead of real contract address
**Fix:** Already fixed in `ppss.yaml` (set to your deployed contract)

---

## 📊 Monitor Your Bot

### View Predictions on Blockchain Explorer
**Mainnet:** https://explorer.oasis.io/mainnet/sapphire/address/0xYOUR_WALLET_ADDRESS

### Query Your Predictions Programmatically
Create your own script to query the Ocean Protocol subgraph for your prediction history.

### Check Bot Logs
```bash
# Latest log
ls -lt logs/ | head -2

# View log
cat logs/out_<timestamp>.txt
```

### Claim Your Rewards

After your bot has made predictions and they've been verified, you can claim rewards:

```bash
# Claim OCEAN tokens
./run_bot.sh claim

# Claim ROSE tokens (gas refunds)
./run_bot.sh claim-rose
```

**When to claim:**
- After your predictions are verified (takes a few epochs)
- Check for pending payouts periodically
- If output shows "No payouts available", you either haven't made predictions yet or already claimed them

---

## 🎓 What You've Learned

1. **Environment variables** need to be loaded each terminal session
2. **The launcher script** (`run_bot.sh`) automates this
3. **Binance is blocked** in your region - need VPN for mainnet
4. **Simulation mode** works without VPN using Kraken
5. **Your bot is fully configured** and ready to run!

---

## 🚀 Next Steps

1. **Test with simulation:**
   ```bash
   ./run_bot.sh sim
   ```

2. **Get VPN and run on mainnet:**
   ```bash
   ./run_bot.sh mainnet
   ```

3. **Monitor and optimize:**
   - Check prediction accuracy
   - Adjust stake amounts
   - Add more feeds
   - Improve AI model

---

## 🔐 Security Reminder

- **Never share your `PRIVATE_KEY`**
- **Never commit `pdr_config.env` to git** (already in .gitignore)
- **If compromised:** Transfer funds immediately and use new wallet
- **Backup your key** securely offline

---

**Need help? Check `SETUP_GUIDE.md` for detailed documentation.**


