@echo off
setlocal
cd /d "%~dp0"
title Upload portfolio to GitHub

if /i "%~1"=="check" goto check

echo ============================================
echo   Upload portfolio to GitHub
echo ============================================
echo.
set /p GHUSER=Your GitHub username (default: ziwoziliaoku): 
if not defined GHUSER set GHUSER=ziwoziliaoku
set REPO=warm-paw-portfolio

echo.
echo [1/4] Setting commit author...
git config user.name "%GHUSER%"
git config user.email "%GHUSER%@users.noreply.github.com"

echo [2/4] Staging changes...
git add -A
git diff --cached --quiet
if not errorlevel 1 goto nocommit
git commit -m "update: %DATE% %TIME%"
:nocommit

echo [3/4] Setting SSH remote...
git remote remove origin >nul 2>&1
git remote add origin git@github.com:%GHUSER%/%REPO%.git

echo [4/4] Pushing...
set ATTEMPT=0
:retry
set /a ATTEMPT+=1
git push -u origin main
if not errorlevel 1 goto ok
if %ATTEMPT% GEQ 3 goto fail
echo.
echo Retry %ATTEMPT% failed, waiting 3 seconds...
timeout /t 3 /nobreak >nul
goto retry

:ok
echo.
echo DONE:
echo   https://github.com/%GHUSER%/%REPO%
start "" "https://github.com/%GHUSER%/%REPO%"
pause
exit /b 0

:fail
echo.
echo PUSH FAILED. Check:
echo   1. SSH key still on GitHub: https://github.com/settings/keys
echo   2. repo %REPO% exists and is PUBLIC
echo   3. username correct
echo   4. network: run again
pause
exit /b 1

:check
echo [CHECK MODE] no push
git --version
git status --short --branch
git remote -v
pause
exit /b 0
