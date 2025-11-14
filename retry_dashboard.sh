#!/bin/bash
echo "Checking dashboard readiness..."
echo ""
echo "Parquet files in exports:"
find lake_data/exports -name "*.parquet" 2>/dev/null | wc -l
echo ""
echo "If 0, wait 10 more minutes and try again"
echo "If > 0, dashboard should work!"
echo ""
echo "To start dashboard: pdr dashboard my_ppss.yaml sapphire-mainnet"
