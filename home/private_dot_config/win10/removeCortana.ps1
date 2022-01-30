# Remove Cortana, all users

Get-appxpackage -allusers *Microsoft.549981C3F5F10* | Remove-AppxPackage
