@echo off
setlocal
cd /d "%~dp0"
title Upload portfolio to GitHub

if /i "%~1"=="check" goto check

echo ============================================
echo   Upload portfolio to GitHub
echo ============================================
echo.
set /p GHUSER=Your GitHub username: 
if not defined GHUSER goto nouser
set REPO=warm-paw-portfolio

echo.
echo [1/3] Setting commit author...
git config user.name "%GHUSER%"
git config user.email "%GHUSER%@users.noreply.github.com"
git commit --amend --reset-author --no-edit >nul 2>&1

echo [2/3] Setting remote...
git remote remove origin >nul 2>&1
git remote add origin https://github.com/%GHUSER%/%REPO%.git

echo [3/3] Pushing...
echo       GitHub login: browser window will pop up, click Authorize
git push -u origin main
if errorlevel 1 goto fail

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
echo   1. repo %REPO% exists on GitHub and is PUBLIC
echo   2. repo was created WITHOUT README / gitignore / license
echo   3. username typed correctly (copy it from the URL bar)
echo   4. login popup was not cancelled
echo   5. network: try again, or run the other platform script
pause
exit /b 1

:check
echo [CHECK MODE] no push
git --version
git status --short --branch
git remote -v
pause
exit /b 0
