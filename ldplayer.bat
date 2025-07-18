@echo off
title LDPlayer Manager
color 0A

echo ╔══════════════════════════════════════════════════════════════╗
echo ║                   🎮 LDPLAYER MANAGER 🎮                    ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo [1] 🚀 Start LDPlayers
echo [2] 🛑 Stop All LDPlayers
echo [3] ❌ Exit
echo.
set /p "choice=👉 Chọn (1-3): "

if "%choice%"=="1" goto START
if "%choice%"=="2" goto STOP
if "%choice%"=="3" exit
goto START

:START
cls
echo 🚀 Starting LDPlayers...

REM ===== CẤU HÌNH LDPLAYER Ở ĐÂY =====
REM Bỏ REM để enable, thêm REM để disable

"D:\LDPlayer\ldconsole.exe" launch --name MAX-1
timeout /t 3
"D:\LDPlayer\ldconsole.exe" launch --name MAX-2
timeout /t 3
"D:\LDPlayer\ldconsole.exe" launch --name MAX-3
timeout /t 3

"D:\LDPlayer\ldconsole.exe" launch --name MAX-4
timeout /t 3
"D:\LDPlayer\ldconsole.exe" launch --name MAX-5
timeout /t 3
"D:\LDPlayer\ldconsole.exe" launch --name MAX-6
timeout /t 3
"D:\LDPlayer\ldconsole.exe" launch --name MAX-7
timeout /t 3
"D:\LDPlayer\ldconsole.exe" launch --name MAX-8
timeout /t 3
"D:\LDPlayer\ldconsole.exe" launch --name MAX-9
timeout /t 3

echo.
echo ✅ Done! Waiting 15s for devices...
timeout /t 15
adb devices
pause
exit

:STOP
cls
echo 🛑 Stopping all LDPlayers...
"D:\LDPlayer\ldconsole.exe" quitall
echo ✅ All stopped!
timeout /t 5
adb devices
pause
exit