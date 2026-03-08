@echo off
echo Starting MyTime API...
echo.

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

echo Starting FastAPI server...
echo API will be available at: http://localhost:8000
echo Swagger docs: http://localhost:8000/docs
echo.

REM Run directly with uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause