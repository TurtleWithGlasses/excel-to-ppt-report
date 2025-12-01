@echo off
REM ReportForge - Launch Script with Cache Clearing
echo Clearing Python cache...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc 2>nul

echo Starting ReportForge...
python main.py

pause
