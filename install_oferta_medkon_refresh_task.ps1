param(
    [string]$TaskName = "Medkon - odswiez oferta_medkon.xml",
    [string]$At = "09:30"
)

$ErrorActionPreference = "Stop"

$workspace = Split-Path -Parent $MyInvocation.MyCommand.Path
$scriptPath = Join-Path $workspace "update_oferta_medkon.ps1"

if (-not (Test-Path $scriptPath)) {
    throw "Nie znaleziono skryptu: $scriptPath"
}

$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`""

$trigger = New-ScheduledTaskTrigger -Daily -At $At
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -MultipleInstances IgnoreNew

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Description "Cykliczne pobieranie oferta_medkon.xml z modulu Ceneo XML z pominieciem pierwszego wiersza." `
    -Force

Write-Host "Dodano zadanie: $TaskName"
Write-Host "Godzina uruchomienia: $At"
