@echo off
setlocal

echo ==================================================================
echo GigSecure - AI-Powered Parametric Income Protection v2.1.0
echo ==================================================================
echo.

where python >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python is not installed. Please install Python 3.10+
  exit /b 1
)

for /f "delims=" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo [OK] Python available: %PYVER%
echo.

if not exist ".venv\Scripts\python.exe" (
  echo [INFO] Creating virtual environment...
  python -m venv .venv
)

echo [INFO] Using virtual environment: .venv
echo [INFO] Installing dependencies...
.\.venv\Scripts\python.exe -m pip install -q -r gigsecure\requirements.txt
echo.
echo ==================================================================
echo Starting GigSecure API...
echo ==================================================================
echo.

if not "%PORT%"=="" (
  set APP_PORT=%PORT%
) else (
  set APP_PORT=8000
)

echo Open: http://localhost:%APP_PORT%
echo Demo login: http://localhost:%APP_PORT%/gigsecure_login.html
echo API docs: http://localhost:%APP_PORT%/docs
echo.
echo Demo credentials:
echo Worker: ravi.kumar@swiggy.in / demo1234
echo Worker: arjun.raj@zomato.in / demo1234
echo Admin : admin@digit.com / admin123
echo.

.\.venv\Scripts\python.exe main.py

if errorlevel 1 (
  echo.
  echo [ERROR] Failed to start GigSecure
  echo.
  echo Troubleshooting:
  echo 1. Ensure port %APP_PORT% is not already in use
  echo 2. Make sure Python virtual environment was created successfully
  echo 3. Try: set PORT=8001 ^&^& START_GIGSECURE.bat
  echo.
  exit /b 1
)

endlocal
