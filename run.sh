#!/bin/bash
# Quick Start Script for Trading Bot

echo "🚀 Installing dependencies..."
pip install -r requirements.txt

echo "✅ Dependencies installed!"
echo ""
echo "📊 Running Backtest..."
python backtester.py

echo ""
echo "🤖 Starting Live Bot..."
python bot.py
