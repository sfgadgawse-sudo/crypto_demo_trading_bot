# ==========================================
# BINANCE TESTNET CONFIGURATION
# ==========================================

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Binance Testnet API Keys (Loaded from .env file)
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

# Trading Configuration
SYMBOL = "BTCUSDT"  # Trading pair
TIMEFRAME = "1m"     # 1 minute candlestick
INITIAL_BALANCE = 100  # USDT (demo money)

# Strategy Configuration
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

# Risk Management
STOP_LOSS_PERCENT = 2      # 2% stop loss
TAKE_PROFIT_PERCENT = 1.5  # 1.5% take profit
POSITION_SIZE_PERCENT = 10  # Use 10% of balance per trade
MAX_POSITIONS = 3           # Max open positions

# Logging
LOG_FILE = "trading_bot.log"
DEBUG = True
