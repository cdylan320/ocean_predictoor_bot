#!/bin/bash

echo "================================"
echo "Ocean Predictoor Multisim Runner"
echo "================================"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/Scripts/activate

# Load environment variables
echo "Loading environment variables..."
source pdr_config.env

# Add pdr to PATH
export PATH=$PATH:.

echo "✓ Environment ready"
echo ""
echo "Starting multisim optimization..."
echo "This will test 36 different configurations to find the best one."
echo "Expected time: 2-3 hours"
echo ""
echo "Parameters being tested:"
echo "  - max_n_train: 500, 1000, 2000"
echo "  - autoregressive_n: 2, 3, 5"
echo "  - approach: Linear, XGBoost"
echo "  - balance_classes: None, SMOTE"
echo ""
echo "Press Ctrl+C to cancel at any time."
echo ""
sleep 3

# Run multisim
pdr multisim multisim_ppss.yaml sapphire-mainnet

echo ""
echo "================================"
echo "Multisim Complete!"
echo "================================"
echo ""
echo "Check the results to find the best configuration."
echo "The winning config will have the highest accuracy."
