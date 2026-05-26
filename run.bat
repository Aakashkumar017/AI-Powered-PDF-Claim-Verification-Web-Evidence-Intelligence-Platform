@echo off
cd /d "%~dp0"
echo Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
echo.
echo Starting backend FastAPI server...
start "Backend" cmd /k "cd /d "%~dp0backend" && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
timeout /t 3
echo.
echo Starting frontend Streamlit app...
cd /d "%~dp0frontend"
python -m streamlit run app.py
pause
