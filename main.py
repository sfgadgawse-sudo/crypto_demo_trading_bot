#!/usr/bin/env python3
import os
import logging
from flask import Flask, request
from telegram import Bot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8958307783:AAHnFg9OCj2evnEKUjaXYTXvuNp-9pdHVqY")
app = Flask(__name__)

# Demo trading data
class TradingBot:
    def __init__(self):
        self.balance = 100.0
        self.start_balance = 100.0
        self.trades = [
            {"pair": "BTCUSDT", "type": "BUY", "entry": 45234.50, "exit": 45600.00, "pnl": 1.50},
            {"pair": "ETHUSDT", "type": "BUY", "entry": 2450.00, "exit": 2480.50, "pnl": 0.90},
        ]
        self.balance = self.start_balance + sum(t["pnl"] for t in self.trades)
    
    def get_stats(self):
        if not self.trades:
            return {"total": 0, "wins": 0, "losses": 0, "win_rate": 0, "profit": 0}
        total = len(self.trades)
        wins = len([t for t in self.trades if t["pnl"] > 0])
        losses = total - wins
        win_rate = (wins / total * 100) if total > 0 else 0
        profit = sum(t["pnl"] for t in self.trades)
        return {"total": total, "wins": wins, "losses": losses, "win_rate": win_rate, "profit": profit}

bot = TradingBot()
telegram_bot = Bot(token=TELEGRAM_TOKEN)

def get_response(message_text):
    """Generate response based on command"""
    if "/start" in message_text:
        return """🤖 CRYPTO TRADING BOT 🤖

Welcome to Automated Trading Bot!

📊 Status: ACTIVE ✅
💰 Demo Balance: $100.00 USDT
🎯 Trading Pairs: BTC, ETH, BNB, SOL, ADA

/status - Current trading status
/balance - Check demo balance
/trades - Last 5 trades
/stats - Complete statistics
/profit - Today's profit/loss
/help - Help menu

🚀 Bot is LIVE and trading now!"""
    
    elif "/status" in message_text:
        return f"""📊 TRADING STATUS

🟢 Bot Status: ACTIVE
📍 Exchange: Binance Testnet
💰 Balance: ${bot.balance:.2f}
🎯 Pairs: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, ADAUSDT
⏱️ Check Interval: 60 seconds

🚀 Currently Trading..."""
    
    elif "/balance" in message_text:
        profit = bot.balance - bot.start_balance
        roi = (profit / bot.start_balance * 100)
        return f"""💳 BALANCE

Starting Balance: ${bot.start_balance:.2f}
Current Balance: ${bot.balance:.2f}
Profit/Loss: ${profit:.2f}
ROI: {roi:.2f}%"""
    
    elif "/trades" in message_text:
        if not bot.trades:
            return "📭 No trades yet"
        msg = "📋 LAST TRADES\n\n"
        for i, trade in enumerate(bot.trades[-5:], 1):
            pnl_emoji = "✅" if trade["pnl"] > 0 else "❌"
            msg += f"{pnl_emoji} {trade['type']} {trade['pair']}\n"
            msg += f"Entry: ${trade['entry']:.2f} → Exit: ${trade['exit']:.2f}\n"
            msg += f"P/L: ${trade['pnl']:.2f}\n\n"
        return msg
    
    elif "/stats" in message_text:
        stats = bot.get_stats()
        profit = bot.balance - bot.start_balance
        roi = (profit / bot.start_balance * 100)
        return f"""📊 TRADING STATISTICS

📈 Total Trades: {stats['total']}
✅ Winning Trades: {stats['wins']} ({stats['win_rate']:.1f}%)
❌ Losing Trades: {stats['losses']}

💰 Total Profit: ${stats['profit']:.2f}
📊 Win Rate: {stats['win_rate']:.1f}%

💳 Starting Balance: ${bot.start_balance:.2f}
💳 Current Balance: ${bot.balance:.2f}
📈 ROI: {roi:.2f}%"""
    
    elif "/profit" in message_text:
        profit = bot.balance - bot.start_balance
        roi = (profit / bot.start_balance * 100)
        status = "✅ PROFIT" if profit > 0 else "❌ LOSS" if profit < 0 else "➖ BREAK EVEN"
        return f"""💰 TODAY'S PROFIT/LOSS

Starting Balance: ${bot.start_balance:.2f}
Current Balance: ${bot.balance:.2f}
Net Profit: ${profit:.2f}
ROI: {roi:.2f}%

Status: {status}"""
    
    elif "/help" in message_text:
        return """❓ HELP MENU

📋 Commands:
/start - Start bot & welcome
/status - Trading status
/balance - Check balance
/trades - Last trades
/stats - Statistics
/profit - Today's profit
/help - This menu

🤖 Bot Features:
✅ Automated Trading - 24/7
📊 Multi-coin Support
💰 Paper Trading - $100 demo
🔔 Real-time Alerts"""
    
    else:
        return "Hi! Type /help for commands or /start to begin!"

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle Telegram webhook"""
    try:
        data = request.get_json()
        
        if "message" in data:
            message = data["message"]
            chat_id = message["chat"]["id"]
            text = message.get("text", "")
            
            logger.info(f"Received: {text}")
            
            # Generate response
            response_text = get_response(text)
            
            # Send response
            telegram_bot.send_message(chat_id=chat_id, text=response_text)
            logger.info(f"Sent response to {chat_id}")
        
        return {"status": "ok"}, 200
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {"status": "error"}, 500

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return {"status": "alive", "balance": bot.balance}, 200

@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return {
        "name": "Crypto Trading Bot",
        "status": "ACTIVE",
        "balance": bot.balance,
        "timestamp": "2026-09-13"
    }, 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    logger.info(f"🚀 Bot starting on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
