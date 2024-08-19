@echo off
setlocal

REM Check if commit message is provided
if "%1"=="" (
  echo Usage: git-commit-push.bat "commit message"
  exit /b 1
)

REM Check if branch  is provided
if "%2"=="" (
  echo Usage: git-commit-push.bat "branch"
  exit /b 2
)

REM Add all changes
git add .

REM Commit changes with the provided message
git commit -m "%1"

REM Push changes to the main branch
REM Push changes to the selected branch
git push origin %2

endlocal
