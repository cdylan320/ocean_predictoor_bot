# VPN Setup for Binance Access

## Problem

Binance is blocking your location with error 451:
```
"Service unavailable from a restricted location according to 'b. Eligibility'"
```

## Solution: Use a VPN

You need a VPN to access Binance API from your location.

### Option 1: Free VPN Solutions

**ProtonVPN (Free)**
1. Download: https://protonvpn.com/download
2. Create free account
3. Connect to a server in Singapore, Japan, or Europe
4. Run simulation

**Windscribe (Free 10GB/month)**
1. Download: https://windscribe.com/download
2. Create account (10GB free monthly)
3. Connect to allowed region
4. Run simulation

### Option 2: Premium VPN (Recommended)

**NordVPN / ExpressVPN / Surfshark**
- More reliable
- Faster speeds
- Better for continuous bot operation
- ~$5-10/month

### Option 3: Set System Proxy

If you already have a proxy/VPN service:

**Windows (Git Bash):**
```bash
export HTTP_PROXY=http://your-proxy:port
export HTTPS_PROXY=http://your-proxy:port
./run_bot.sh sim
```

**Windows (PowerShell):**
```powershell
$env:HTTP_PROXY="http://your-proxy:port"
$env:HTTPS_PROXY="http://your-proxy:port"
./run_bot.sh sim
```

### Option 4: Use Kraken Instead (No VPN Needed)

If you don't want to use VPN, switch to Kraken:

1. Edit `my_ppss.yaml`
2. Comment out binance lines
3. Uncomment kraken lines

```yaml
lake_ss:
  feeds:
    # - binance BTC/USDT ETH/USDT 5m
    - kraken BTC/USDT ETH/USDT 5m
```

## Testing VPN Connection

After connecting to VPN, test Binance access:

```bash
curl https://api.binance.com/api/v3/exchangeInfo
```

If you see JSON response (not 451 error), VPN is working!

## Important for Mainnet

**For mainnet bot operation:**
- Binance is recommended (better liquidity)
- You'll need a reliable VPN running 24/7
- Or use a VPS/cloud server in an allowed region

## Allowed Regions for Binance

Binance generally works from:
- Europe (most countries)
- Asia (Singapore, Japan, Thailand, etc.)
- Some South American countries

Restricted regions:
- US
- Some middle eastern countries
- Check Binance terms for full list

## Next Steps

1. **Install VPN** (ProtonVPN free is good for testing)
2. **Connect to Singapore or Japan server**
3. **Run simulation:**
   ```bash
   ./run_bot.sh sim
   ```

The CNN-GRU model should then work with Binance data!

