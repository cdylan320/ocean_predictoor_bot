#!/usr/bin/env python3
"""
Test Binance API access from VPS
Checks if you can access Binance API without 451 errors
"""

import sys
import requests
from datetime import datetime

def test_binance_api():
    """Test Binance API access"""
    print("=" * 60)
    print("Testing Binance API Access")
    print("=" * 60)
    print(f"Time: {datetime.now()}\n")
    
    # Test 1: Exchange Info (most basic endpoint)
    print("Test 1: Exchange Info (GET /api/v3/exchangeInfo)")
    print("-" * 60)
    try:
        url = "https://api.binance.com/api/v3/exchangeInfo"
        response = requests.get(url, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 451:
            print("❌ ERROR: 451 - Service unavailable from restricted location")
            print("   Your VPS location is blocked by Binance")
            return False
        elif response.status_code == 200:
            print("✅ SUCCESS: Can access Binance API")
            data = response.json()
            print(f"   Found {len(data.get('symbols', []))} trading pairs")
        else:
            print(f"⚠️  Unexpected status code: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: Failed to connect - {e}")
        return False
    
    print()
    
    # Test 2: 24hr Ticker (data endpoint)
    print("Test 2: 24hr Ticker for BTC/USDT (GET /api/v3/ticker/24hr)")
    print("-" * 60)
    try:
        url = "https://api.binance.com/api/v3/ticker/24hr"
        params = {"symbol": "BTCUSDT"}
        response = requests.get(url, params=params, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 451:
            print("❌ ERROR: 451 - Service unavailable from restricted location")
            return False
        elif response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS: Can fetch market data")
            print(f"   BTC/USDT Price: ${float(data['lastPrice']):,.2f}")
            print(f"   24h Change: {float(data['priceChangePercent']):.2f}%")
        else:
            print(f"⚠️  Unexpected status code: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: Failed to fetch data - {e}")
        return False
    
    print()
    
    # Test 3: Klines/OHLCV (what the bot uses)
    print("Test 3: OHLCV/Klines for BTC/USDT 5m (GET /api/v3/klines)")
    print("-" * 60)
    try:
        url = "https://api.binance.com/api/v3/klines"
        params = {
            "symbol": "BTCUSDT",
            "interval": "5m",
            "limit": 5
        }
        response = requests.get(url, params=params, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 451:
            print("❌ ERROR: 451 - Service unavailable from restricted location")
            return False
        elif response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS: Can fetch OHLCV data (what bot needs)")
            print(f"   Fetched {len(data)} candles")
            if data:
                latest = data[-1]
                print(f"   Latest candle: Open=${float(latest[1]):,.2f}, Close=${float(latest[4]):,.2f}")
        else:
            print(f"⚠️  Unexpected status code: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: Failed to fetch OHLCV - {e}")
        return False
    
    print()
    print("=" * 60)
    print("✅ ALL TESTS PASSED - Binance API is accessible!")
    print("   Your VPS can run the bot without 451 errors")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_binance_api()
    sys.exit(0 if success else 1)

