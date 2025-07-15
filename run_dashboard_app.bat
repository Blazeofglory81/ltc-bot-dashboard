@echo off
cd /d "C:\Users\Russe\Desktop\ltc_bot_local_history"

echo Starting Litecoin Paper Bot & Dashboard...

REM Step 1: Activate venv
call venv\Scripts\activate

REM Step 2: Run bot in background
start cmd /k python bot.py

REM Step 3: Launch Streamlit dashboard
streamlit run dashboard.py

pause
