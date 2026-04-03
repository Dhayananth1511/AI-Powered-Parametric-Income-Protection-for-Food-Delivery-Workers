#!/bin/bash
echo "🛡️  GigSecure Phase 2 Launcher"
echo "📦  Installing dependencies..."
pip install -r gigsecure-backend/requirements.txt
echo "🚀  Starting GigSecure..."
python main.py
