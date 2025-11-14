#!/bin/bash
# Quick test for Binance API access from VPS

echo "============================================================"
echo "Testing Binance API Access"
echo "============================================================"
echo ""

# Test 1: Exchange Info
echo "Test 1: Exchange Info"
echo "------------------------------------------------------------"
response=$(curl -s -w "\n%{http_code}" "https://api.binance.com/api/v3/exchangeInfo" --max-time 10)
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

echo "HTTP Status Code: $http_code"

if [ "$http_code" = "451" ]; then
    echo "❌ ERROR: 451 - Service unavailable from restricted location"
    echo "   Your VPS location is BLOCKED by Binance"
    exit 1
elif [ "$http_code" = "200" ]; then
    echo "✅ SUCCESS: Can access Binance API"
    symbol_count=$(echo "$body" | grep -o '"symbol"' | wc -l)
    echo "   Found ~$symbol_count trading pairs"
else
    echo "⚠️  Unexpected status code: $http_code"
    exit 1
fi

echo ""

# Test 2: OHLCV Data (what bot uses)
echo "Test 2: OHLCV/Klines for BTC/USDT 5m"
echo "------------------------------------------------------------"
response=$(curl -s -w "\n%{http_code}" "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=5m&limit=5" --max-time 10)
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

echo "HTTP Status Code: $http_code"

if [ "$http_code" = "451" ]; then
    echo "❌ ERROR: 451 - Service unavailable from restricted location"
    echo "   Your VPS location is BLOCKED by Binance"
    exit 1
elif [ "$http_code" = "200" ]; then
    echo "✅ SUCCESS: Can fetch OHLCV data (what bot needs)"
    candle_count=$(echo "$body" | grep -o '\[' | wc -l)
    echo "   Fetched $candle_count candles"
else
    echo "⚠️  Unexpected status code: $http_code"
    exit 1
fi

echo ""
echo "============================================================"
echo "✅ ALL TESTS PASSED - Binance API is accessible!"
echo "   Your VPS can run the bot without 451 errors"
echo "============================================================"

