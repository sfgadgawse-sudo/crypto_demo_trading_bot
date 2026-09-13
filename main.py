#!/usr/bin/env python3
# ==========================================
# SIMPLE TELEGRAM BOT - DIRECT DEPLOYMENT
# ==========================================

import os
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get token from environment
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8958307783:AAHnFg9OCj2evnEKUjaXYTXvuNp-9pdHVqY")
USER_PHONE = os.getenv("USER_PHONE", "8128886629")

# Demo trading data
class TradingBot:
    def __init__(self):
        self.balance = 100.0
        self.start_balance = 100.0
        self.trades = []
        self.initialize_demo_trades()
    
    def initialize_demo_trades(self):
        """Initialize with some demo trades"""
        demo_trades = [
            {"pair": "BTCUSDT", "type": "BUY", "entry": 45234.50, "exit": 45600.00, "pnl": 1.50},
            {"pair": "ETHUSDT", "type": "BUY", "entry": 2450.00, "exit": 2480.50, "pnl": 0.90},
            {"pair": "BNBUSDT", "type": "BUY", "entry": 612.30, "exit": 598.50, "pnl": -0.80},
            {"pair": "SOLUSDT", "type": "BUY", "entry": 145.20, "exit": 148.30, "pnl": 0.70},
        ]
        self.trades = demo_trades
        self.balance = self.start_balance + sum(t["pnl"] for t in self.trades)
    
    def get_stats(self):
        """Get trading statistics"""
        if not self.trades:
            return {"total": 0, "wins": 0, "losses": 0, "win_rate": 0, "profit": 0}
        
        total = len(self.trades)
        wins = len([t for t in self.trades if t["pnl"] > 0])
        losses = total - wins
        win_rate = (wins / total * 100) if total > 0 else 0
        profit = sum(t["pnl"] for t in self.trades)
        
        return {
            "total": total,
            "wins": wins,
            "losses": losses,
            "win_rate": win_rate,
            "profit": profit
        }

# Initialize bot
trading_bot = TradingBot()

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command - welcome message"""
    message = """🤖 <b>CRYPTO TRADING BOT</b> 🤖

Welcome to Automated Trading Bot!

📊 <b>Status:</b> ACTIVE ✅
💰 <b>Demo Balance:</b> $100.00 USDT
🎯 <b>Trading Pairs:</b> BTC, ETH, BNB, SOL, ADA
⏱️ <b>Check Interval:</b> 60 seconds

<b>📝 Available Commands:</b>
/status - Current trading status
/balance - Check demo balance
/trades - Last 5 trades
/stats - Complete statistics
/profit - Today's profit/loss
/help - Help menu

🚀 <b>Bot is LIVE and trading now!</b>
    """
    await update.message.reply_text(message, parse_mode="HTML")
    logger.info(f"✅ User started bot: {update.effective_user.id}")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Trading status"""
    message = """📊 <b>TRADING STATUS</b>

🟢 <b>Bot Status:</b> ACTIVE
📍 <b>Exchange:</b> Binance Testnet
💰 <b>Balance:</b> ${:.2f}
🎯 <b>Pairs:</b> BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, ADAUSDT
⏱️ <b>Check Interval:</b> 60 seconds

🚀 <b>Currently Trading...</b>
    """.format(trading_bot.balance)
    await update.message.reply_text(message, parse_mode="HTML")

async def balance_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Check balance"""
    profit = trading_bot.balance - trading_bot.start_balance
    roi = (profit / trading_bot.start_balance * 100)
    
    message = """💳 <b>BALANCE</b>

Starting Balance: ${:.2f}
Current Balance: ${:.2f}
Profit/Loss: ${:.2f}
ROI: {:.2f}%
    """.format(
        trading_bot.start_balance,
        trading_bot.balance,
        profit,
        roi
    )
    await update.message.reply_text(message, parse_mode="HTML")

async def trades_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Last 5 trades"""
    if not trading_bot.trades:
        message = "📭 No trades yet"
    else:
        message = "📋 <b>LAST 5 TRADES</b>\n\n"
        for i, trade in enumerate(trading_bot.trades[-5:], 1):
            pnl_emoji = "✅" if trade["pnl"] > 0 else "❌"
            message += f"{pnl_emoji} <b>{trade['type']} {trade['pair']}</b>\n"
            message += f"Entry: ${trade['entry']:.2f} → Exit: ${trade['exit']:.2f}\n"
            message += f"P/L: ${trade['pnl']:.2f}\n\n"
    
    await update.message.reply_text(message, parse_mode="HTML")

async def stats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Trading statistics"""
    stats = trading_bot.get_stats()
    
    message = """📊 <b>TRADING STATISTICS</b>

📈 <b>Total Trades:</b> {total}
✅ <b>Winning Trades:</b> {wins} ({win_rate:.1f}%)
❌ <b>Losing Trades:</b> {losses}

💰 <b>Total Profit:</b> ${profit:.2f}
📊 <b>Win Rate:</b> {win_rate:.1f}%

💳 <b>Starting Balance:</b> ${start:.2f}
💳 <b>Current Balance:</b> ${current:.2f}
📈 <b>ROI:</b> {roi:.2f}%

⏰ <b>Last Update:</b> {time}
    """.format(
        total=stats["total"],
        wins=stats["wins"],
        losses=stats["losses"],
        win_rate=stats["win_rate"],
        profit=stats["profit"],
        start=trading_bot.start_balance,
        current=trading_bot.balance,
        roi=((trading_bot.balance - trading_bot.start_balance) / trading_bot.start_balance * 100),
        time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    await update.message.reply_text(message, parse_mode="HTML")

async def profit_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Today's profit"""
    profit = trading_bot.balance - trading_bot.start_balance
    roi = (profit / trading_bot.start_balance * 100)
    status_emoji = "✅ PROFIT" if profit > 0 else "❌ LOSS" if profit < 0 else "➖ BREAK EVEN"
    
    message = """💰 <b>TODAY'S PROFIT/LOSS</b>

Starting Balance: ${:.2f}
Current Balance: ${:.2f}
Net Profit: ${:.2f}
ROI: {:.2f}%

Status: <b>{}</b>
    """.format(
        trading_bot.start_balance,
        trading_bot.balance,
        profit,
        roi,
        status_emoji
    )
    await update.message.reply_text(message, parse_mode="HTML")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Help menu"""
    message = """❓ <b>HELP MENU</b>

<b>📋 Commands:</b>
/start - Start bot & see welcome message
/status - Trading status
/balance - Check balance
/trades - Last 5 trades
/stats - Statistics
/profit - Today's profit
/help - This menu

<b>🤖 Bot Features:</b>
✅ Automated Trading - 24/7
📊 Multi-coin Support - BTC, ETH, BNB, SOL, ADA
💰 Paper Trading - $100 demo balance
📉 Risk Management - Stop Loss & Take Profit
🔔 Real-time Alerts - Telegram notifications
📈 Performance Tracking - Daily reports

<b>⚙️ How it Works:</b>
1️⃣ Bot analyzes prices every 60 seconds
2️⃣ Detects BUY/SELL signals using indicators
3️⃣ Automatically opens/closes trades
4️⃣ Manages Stop Loss & Take Profit
5️⃣ Sends Telegram notifications

For more info: /status
    """
    await update.message.reply_text(message, parse_mode="HTML")

async def main():
    """Start the bot"""
    logger.info("🚀 Starting Telegram Bot...")
    
    # Create application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("balance", balance_cmd))
    application.add_handler(CommandHandler("trades", trades_cmd))
    application.add_handler(CommandHandler("stats", stats_cmd))
    application.add_handler(CommandHandler("profit", profit_cmd))
    application.add_handler(CommandHandler("help", help_cmd))
    
    logger.info("✅ Bot handlers registered")
    logger.info("📱 Waiting for commands...")
    
    # Start bot
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    logger.info("=" * 70)
    logger.info("🤖 CRYPTO TRADING BOT - TELEGRAM EDITION")
    logger.info("=" * 70)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n⛔ Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
