@echo off

if not exist venv (
  echo Virtual environment not found. Run install.bat first.
  exit /b 1
)

call venv\scripts\activate

python -m src.xtts_demo