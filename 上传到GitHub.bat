@echo off
setlocal
cd /d "%~dp0"
title Upload portfolio to GitHub

if /i "%~1"=="check" goto check

echo ============================================
echo   Upload portfolio to GitHub  (SSH over 443)
echo ============================================
echo.
set /p GHUSER=Your GitHub username: 
if not defined GHUSER goto nouser
set REPO=warm-paw-portfolio

echo.
echo [1/4] Setting commit author...
git config user.name "%GHUSER%"
git config user.email "%GHUSER%@users.noreply.github.com"
git commit --amend --reset-author --no-edit >nul 2>&1

echo [2/4] Setting SSH remote...
git remote remove origin >nul 2>&1
git remote add origin git@github.com:%GHUSER%/%REPO%.git

echo [3/4] Testing SSH login...
ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=15 -T git@github.com

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

:nouser
echo Username is empty. Exit.
pause
exit /b 1

:fail
echo.
echo PUSH FAILED. Check these:
echo   1. SSH key added on GitHub: https://github.com/settings/keys
echo   2. repo %REPO% exists and is PUBLIC
echo   3. username typed correctly (copy from URL bar)
echo   4. if SSH says Permission denied: the key was not added yet
pause
exit /b 1

:check
echo [CHECK MODE] no push
git --version
git status --short --branch
git remote -v
ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=10 -T git@github.com
pause
exit /b 0
