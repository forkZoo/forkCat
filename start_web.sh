#!/bin/bash

# ForkCat Web Interface Launcher

echo "🐵 Starting ForkCat Web Interface..."
echo ""

# Check if cat exists
if [ ! -f "cat_data/dna.json" ]; then
    echo "⚠️  No cat found! Initializing..."
    python src/cli.py init
    echo ""
fi

# Start web server
echo "🚀 Starting web server..."
python web/serve.py
