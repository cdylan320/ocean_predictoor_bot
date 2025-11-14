#!/bin/bash
# Ocean Predictoor Bot Launcher
# This script automatically loads environment variables and runs the bot

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}Ocean Predictoor Bot Launcher${NC}"
echo -e "${GREEN}================================${NC}\n"

# Activate virtual environment
if [ -f "venv/Scripts/activate" ]; then
    echo -e "${YELLOW}Activating virtual environment...${NC}"
    source venv/Scripts/activate
elif [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo -e "${RED}Error: Virtual environment not found!${NC}"
    exit 1
fi

# Load environment variables
if [ -f "pdr_config.env" ]; then
    echo -e "${YELLOW}Loading environment variables...${NC}"
    source pdr_config.env
else
    echo -e "${RED}Error: pdr_config.env not found!${NC}"
    exit 1
fi

# Check if PRIVATE_KEY is set
if [ -z "$PRIVATE_KEY" ]; then
    echo -e "${RED}Error: PRIVATE_KEY not set in pdr_config.env!${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Environment loaded${NC}"
echo -e "${GREEN}✓ Wallet: $WALLET_ADDRESS${NC}"

# Run the bot with provided arguments or defaults
if [ "$1" = "sim" ]; then
    echo -e "${GREEN}✓ Mode: SIMULATION (offline, no blockchain)${NC}\n"
    echo -e "${YELLOW}Running in simulation mode...${NC}"
    pdr sim my_ppss.yaml
elif [ "$1" = "testnet" ]; then
    echo -e "${GREEN}✓ Network: TESTNET (sapphire-testnet)${NC}\n"
    echo -e "${YELLOW}Running on testnet...${NC}"
    pdr predictoor my_ppss.yaml sapphire-testnet
elif [ "$1" = "mainnet" ]; then
    echo -e "${GREEN}✓ Network: MAINNET (sapphire-mainnet)${NC}\n"
    echo -e "${YELLOW}Running on mainnet...${NC}"
    pdr predictoor my_ppss.yaml sapphire-mainnet
elif [ "$1" = "claim" ]; then
    echo -e "${GREEN}✓ Network: MAINNET (claiming rewards)${NC}\n"
    echo -e "${YELLOW}Claiming OCEAN rewards from mainnet...${NC}"
    pdr claim_OCEAN ppss.yaml
elif [ "$1" = "claim-rose" ]; then
    echo -e "${GREEN}✓ Network: MAINNET (claiming rewards)${NC}\n"
    echo -e "${YELLOW}Claiming ROSE rewards from mainnet...${NC}"
    pdr claim_ROSE ppss.yaml
elif [ -z "$1" ]; then
    # No argument provided - use default from env or mainnet
    echo -e "${GREEN}✓ Network: ${NETWORK:-sapphire-mainnet}${NC}\n"
    echo -e "${YELLOW}Running on ${NETWORK:-sapphire-mainnet}...${NC}"
    pdr predictoor my_ppss.yaml ${NETWORK:-sapphire-mainnet}
else
    # Pass through custom command
    echo -e "${YELLOW}Running custom command: $@${NC}"
    "$@"
fi


