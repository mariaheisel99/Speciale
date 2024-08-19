@echo off
setlocal

REM Check if commit message is provided
if "%1"=="" (
  echo Usage: git-commit-push.bat "commit message"
  exit /b 1
)

REM Add all changes
git add .

REM Commit changes with the provided message
git commit -m "%1"

REM Push changes to the main branch
git push origin main

endlocal
