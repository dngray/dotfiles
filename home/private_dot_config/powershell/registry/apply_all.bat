@echo off
:: Ensure the runner jumps into its own physical directory path context
cd /d "%~dp0"

echo =========================================================
echo  LAUNCHING SEQUENTIAL WINDOWS REGISTRY OPTIMIZATIONS
echo =========================================================

:: Loop through and execute every batch file starting with a number
for %%f in ([0-9]*.bat) do (
    echo.
    echo Running target profile: %%f...
    call "%%f"
)

echo.
echo =========================================================
echo  ALL REGISTRY PROFILES APPLIED SUCCESSFULLY!
echo =========================================================
pause
