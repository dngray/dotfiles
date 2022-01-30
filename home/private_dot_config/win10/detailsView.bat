:: https://superuser.com/a/1120877

:: To reset folder view settings of all folders
Reg Delete "HKCU\SOFTWARE\Microsoft\Windows\Shell\BagMRU" /F
Reg Delete "HKCU\SOFTWARE\Microsoft\Windows\Shell\Bags" /F

Reg Delete "HKCU\SOFTWARE\Microsoft\Windows\ShellNoRoam\Bags" /F
Reg Delete "HKCU\SOFTWARE\Microsoft\Windows\ShellNoRoam\BagMRU" /F

Reg Delete "HKCU\SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows\Shell\BagMRU" /F
Reg Delete "HKCU\SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows\Shell\Bags" /F

Reg Delete "HKCU\SOFTWARE\Classes\Wow6432Node\Local Settings\Software\Microsoft\Windows\Shell\Bags" /F
Reg Delete "HKCU\SOFTWARE\Classes\Wow6432Node\Local Settings\Software\Microsoft\Windows\Shell\BagMRU" /F


:: To reset size of details, navigation, preview panes to default
Reg Delete "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Modules\GlobalSettings\Sizer" /F

:: Show Status Bar
reg add "HKCU\Software\Microsoft\Internet Explorer\Main" /v StatusBarOther /t REG_DWORD /d 1 /f

:: Apply Details view to All Folders
reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Streams /v Settings /t REG_BINARY ^
/d 08000000040000000000000000777E137335CF11AE6908002B2E1262040000001000000043000000 /f

:: To kill and restart explorer
taskkill /f /im explorer.exe
start explorer.exe

PAUSE
