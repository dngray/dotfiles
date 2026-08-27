@echo off
:: Ensure the script runs with Administrative Elevation
net session >nul 2>&1 || (echo Requesting admin privileges... && powerShell -Command "Start-Process -FilePath '%0' -Verb RunAs" && exit /b)

echo =========================================================
echo  WINDOWS DUAL-BOOT OPTIMIZATION & PERFORMANCE AUTOMATION
echo =========================================================

echo.
echo [1/6] Setting hardware clock to UTC (Linux Compatibility)...
:: FIXED: Changed from REG_QWORD to REG_DWORD
reg add "HKLM\System\CurrentControlSet\Control\TimeZoneInformation" /v RealTimeIsUniversal /d 1 /t REG_DWORD /f >nul 2>&1

echo [2/6] Disabling Local Password Reset Security Questions...
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\System" /v NoLocalPasswordResetQuestions /d 1 /t REG_DWORD /f >nul 2>&1

echo [3/6] Killing Fast Startup & Hibernation (Prevents Linux NTFS Corruptions)...
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Power" /v HiberbootEnabled /d 0 /t REG_DWORD /f >nul 2>&1
powercfg -h off >nul 2>&1

echo [4/6] Tweaking File Explorer: Showing Hidden Files & Extensions...
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v Hidden /d 1 /t REG_DWORD /f >nul 2>&1
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v HideFileExt /d 0 /t REG_DWORD /f >nul 2>&1

echo [5/6] Disabling Automatic Reboot on System Failure (BSOD freeze check)...
reg add "HKLM\SYSTEM\CurrentControlSet\Control\CrashControl" /v AutoReboot /d 0 /t REG_DWORD /f >nul 2>&1

echo [6/6] Disabling System Restore points via native PowerShell engines...
:: FIXED: Replaced dead policy with active WMI engine calls
powershell -Command "Disable-ComputerRestore -Drive 'C:\'" >nul 2>&1

echo.
echo [!] Restarting File Explorer shell to apply layout shifts...
taskkill /f /im explorer.exe >nul 2>&1
start explorer.exe >nul 2>&1

echo.
echo =========================================================
echo  SUCCESS: Distro dual-boot environment optimizations applied!
echo =========================================================
pause
