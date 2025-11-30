@echo off
echo ========================================
echo ReportForge - Universal Report Generator
echo ========================================
echo.
echo Select an option:
echo 1. Launch Main App (Report Generator)
echo 2. Launch Template Builder
echo 3. Exit
echo.
choice /c 123 /n /m "Enter your choice (1-3): "

if errorlevel 3 goto :EOF
if errorlevel 2 goto builder
if errorlevel 1 goto main

:main
echo.
echo Launching Main App...
python main.py
goto :EOF

:builder
echo.
echo Launching Template Builder...
python main.py --builder
goto :EOF
