@echo off
:: Ensure the script runs with Administrative Elevation
rcut >nul 2>&1 || (echo Requesting admin privileges... && powerShell -Command "Start-Process -FilePath '%0' -Verb RunAs" && exit /b)

echo =========================================================
echo  WINDOWS 11 FILE EXPLORER AUTOMATED RESET & OPTIMIZATION
echo =========================================================

echo.
echo [1/4] Force-closing File Explorer and Shell interfaces...
taskkill /f /im explorer.exe >nul 2>&1

echo [2/4] Wiping the folder layout cache memory databases...
Reg Delete "HKCU\SOFTWARE\Microsoft\Windows\Shell\BagMRU" /F >nul 2>&1
Reg Delete "HKCU\SOFTWARE\Microsoft\Windows\Shell\Bags" /F >nul 2>&1
Reg Delete "HKCU\SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows\Shell\BagMRU" /F >nul 2>&1
Reg Delete "HKCU\SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows\Shell\Bags" /F >nul 2>&1
Reg Delete "HKCU\SOFTWARE\Classes\Wow6432Node\Local Settings\Software\Microsoft\Windows\Shell\Bags" /F >nul 2>&1
Reg Delete "HKCU\SOFTWARE\Classes\Wow6432Node\Local Settings\Software\Microsoft\Windows\Shell\BagMRU" /F >nul 2>&1

echo [3/4] Resetting Navigation, Preview, and Detail pane split widths...
Reg Delete "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Modules\GlobalSettings\Sizer" /F >nul 2>&1

echo [4/4] Enabling the Windows 11 Status Bar layout...
reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v "ShowStatusBar" /t REG_DWORD /d 1 /f >nul 2>&1

echo.
echo [!] Reinitializing Windows desktop environment...
start explorer.exe

echo.
echo =========================================================
echo  SUCCESS: Folder layouts and pane defaults restored!
echo =========================================================
pause
