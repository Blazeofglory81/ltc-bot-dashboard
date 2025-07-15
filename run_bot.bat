@echo off
REM ⚠️ Set this to where you unzipped the folder:
cd /d "C:\Users\Russe\Desktop\ltc_bot_local_history"

echo [1/5] Creating virtual environment...
python -m venv venv

echo [2/5] Activating virtual environment...
call venv\Scripts\activate

echo [3/5] Installing required packages...
pip install --upgrade pip
pip install -r requirements.txt

echo [4/5] Running the Litecoin bot...
python bot.py

pause
