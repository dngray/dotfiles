@ECHO OFF

ECHO Setting time zone to UTC
ECHO https://wiki.archlinux.org/index.php/System_time#UTC_in_Windows
reg add "HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\TimeZoneInformation" /v RealTimeIsUniversal /d 1 /t REG_QWORD /f

ECHO Disabling Password reset questions
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\System" /v NoLocalPasswordResetQuestions /d 1 /t REG_DWORD /f

ECHO Disabling fast startup
ECHO https://wiki.archlinux.org/index.php/Dual_boot_with_Windows#Fast_Start-Up
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Power" /v HiberbootEnabled /d 0 /t REG_DWORD /f
powercfg -h off

ECHO Hidden files on
reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v Hidden /d 1 /t REG_DWORD /f

ECHO Show extensions for known file types
reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v HideFileExt /d 0 /t REG_DWORD /f

ECHO Disable automatic reboot
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control" /v CrashControl /d 0 /t REG_DWORD /f

ECHO Disable system restore
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows NT" /v SystemRestore /d 0 /t REG_DWORD /f

PAUSE
