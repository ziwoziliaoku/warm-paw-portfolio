@echo off
chcp 65001 >nul
cd /d "%~dp0"
title 暖爪咖啡作品集 - 一键上传

if /i "%~1"=="check" goto check

echo ============================================
echo    暖爪咖啡作品集 - 一键上传
echo ============================================
echo.
echo   1 = Gitee（码云，国内速度快，推荐先用这个）
echo   2 = GitHub（需要能正常打开 github.com）
echo.
set /p PLAT=请输入 1 或 2，然后回车：
if "%PLAT%"=="1" goto gitee
if "%PLAT%"=="2" goto github
echo 输入无效，退出。
pause
exit /b 1

:gitee
set HOST=gitee.com
set SITE=Gitee
goto askuser

:github
set HOST=github.com
set SITE=GitHub
goto askuser

:askuser
echo.
set /p GHUSER=请输入你在 %SITE% 的用户名（英文，例如 xiaoming）：
if "%GHUSER%"=="" (
  echo 用户名不能为空，退出。
  pause
  exit /b 1
)
set REPO=warm-paw-portfolio
if "%HOST%"=="gitee.com" (set NOREPLY=%GHUSER%@user.noreply.gitee.com) else (set NOREPLY=%GHUSER%@users.noreply.github.com)

echo.
echo [1/4] 设置提交署名...
git config user.name "%GHUSER%"
git config user.email "%NOREPLY%"
git commit --amend --reset-author --no-edit >nul 2>&1

echo [2/4] 绑定远程仓库...
git remote remove origin >nul 2>&1
git remote add origin https://%HOST%/%GHUSER%/%REPO%.git

echo [3/4] 上传中（第一次会要求登录，见下方提示）...
echo       GitHub：会弹出浏览器授权，点同意即可
echo       Gitee ：弹窗里用户名填 Gitee 用户名，密码填 Gitee 密码或私人令牌
git push -u origin main
if errorlevel 1 goto fail

echo.
echo [4/4] 完成！正在打开你的仓库页面：
echo     https://%HOST%/%GHUSER%/%REPO%
start "" "https://%HOST%/%GHUSER%/%REPO%"
pause
exit /b 0

:fail
echo.
echo 上传失败，对照检查：
echo   1. 平台上是否已经建好空仓库 warm-paw-portfolio（不要勾选初始化 README）
echo   2. 用户名是否输错
echo   3. 登录弹窗是否被关掉了（重新双击，再来一次）
echo   4. Gitee 提示密码错误：去 gitee.com 设置 - 私人令牌 生成一个，用它当密码
echo.
pause
exit /b 1

:check
echo [自检模式] 只检查，不上传。
echo.
git --version
echo.
git status --short --branch
echo.
git remote -v
echo.
pause
exit /b 0
