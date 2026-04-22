# Run this once as Administrator to register the daily backup task.
# Right-click PowerShell → "Run as administrator", then paste:
#   & "C:\Users\johnn\Brain\.scripts\register-task.ps1"

$action  = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument '-NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File "C:\Users\johnn\Brain\.scripts\vault-backup.ps1"'

$trigger  = New-ScheduledTaskTrigger -Daily -At "23:30"

$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -DontStopOnIdleEnd `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 5)

Register-ScheduledTask `
    -TaskName "Obsidian Vault Daily Backup" `
    -Action   $action `
    -Trigger  $trigger `
    -Settings $settings `
    -RunLevel Highest `
    -Force

Write-Host "Task registered. It will run daily at 23:30." -ForegroundColor Green
