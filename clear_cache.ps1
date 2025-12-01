# Clear Python cache - PowerShell version
Write-Host "Clearing Python cache..."
Get-ChildItem -Path . -Include __pycache__ -Recurse -Force | Remove-Item -Recurse -Force
Get-ChildItem -Path . -Filter *.pyc -Recurse -Force | Remove-Item -Force
Write-Host "Cache cleared!"
