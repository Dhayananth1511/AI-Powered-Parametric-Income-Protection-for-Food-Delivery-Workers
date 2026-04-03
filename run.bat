@echo off
echo 🛡️  GigSecure Phase 2 Launcher
echo 📦  Installing dependencies...
python -m pip install -r gigsecure-backend\requirements.txt
echo 🚀  Starting GigSecure...
python main.py
pause
