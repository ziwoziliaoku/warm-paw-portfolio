@echo off
chcp 65001 >nul
cd /d "%~dp0"
title 暖爪咖啡作品集 - 推送到 GitHub

if /i "%~1"=="check" goto check

echo ==========================================
echo   暖爪咖啡作品集 - 一键推送到 GitHub
echo ==========================================
echo.

set /p GHUSER=请输入你的 GitHub 用户名（英文，例如 xiaoming）:
if "%GHUSER%"=="" (
  echo.
  echo 用户名不能为空，脚本退出。
  pause
  exit /b 1
)

set REPO=warm-paw-portfolio

echo.
echo [1/4] 设置提交署名...
git config user.name "%GHUSER%"
git config user.email "%GHUSER%@users.noreply.github.com"
git commit --amend --reset-author --no-edit >nul 2>&1

echo [2/4] 绑定远程仓库...
git remote remove origin >nul 2>&1
git remote add origin https://github.com/%GHUSER%/%REPO%.git

echo [3/4] 推送到 GitHub（第一次会弹出登录窗口，登录一次以后不用再登）...
git push -u origin main
if errorlevel 1 goto fail

echo.
echo [4/4] 完成！正在打开你的仓库页面：
echo     https://github.com/%GHUSER%/%REPO%
start "" "https://github.com/%GHUSER%/%REPO%"
pause
exit /b 0

:fail
echo.
echo 推送失败，常见原因：
echo   1. 还没在 GitHub 上创建仓库 %REPO%（先建，建的时候不要勾选 README）
echo   2. GitHub 用户名输错了
echo   3. 登录弹窗被关掉了（重新双击本文件，再登录一次）
echo.
pause
exit /b 1

:check
echo [自检模式] 只检查，不推送。
echo.
git --version
echo.
git status --short --branch
echo.
if exist ".git" (echo 仓库已初始化：是) else (echo 仓库已初始化：否)
echo.
pause
exit /b 0
