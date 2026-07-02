param(
    [string]$Url = "https://medkon.pl/module/ceneo_xml/generate?secure_key=02f527f2c560e9b762d0025ef90d2179&id_shop=1&show_output=0",
    [string]$OutputPath = "oferta_medkon.xml",
    [switch]$KeepBackup
)

$ErrorActionPreference = "Stop"

$workspace = Split-Path -Parent $MyInvocation.MyCommand.Path
$outputFullPath = [System.IO.Path]::GetFullPath((Join-Path $workspace $OutputPath))
$tempRawPath = Join-Path $workspace "oferta_medkon.download.tmp"
$tempCleanPath = Join-Path $workspace "oferta_medkon.clean.tmp"
$backupPath = Join-Path $workspace "oferta_medkon.xml.bak"

Write-Host "Pobieram XML..."
Invoke-WebRequest -Uri $Url -OutFile $tempRawPath -UseBasicParsing

Write-Host "Usuwam pierwszy wiersz..."
$reader = [System.IO.StreamReader]::new($tempRawPath, $true)
$writer = [System.IO.StreamWriter]::new($tempCleanPath, $false, [System.Text.UTF8Encoding]::new($false))

try {
    $null = $reader.ReadLine()

    while (($line = $reader.ReadLine()) -ne $null) {
        $writer.WriteLine($line)
    }
}
finally {
    $reader.Close()
    $writer.Close()
}

if ((Get-Item $tempCleanPath).Length -eq 0) {
    throw "Pobrany plik po usunieciu pierwszego wiersza jest pusty. Nie podmieniam $OutputPath."
}

if ($KeepBackup -and (Test-Path $outputFullPath)) {
    Copy-Item -LiteralPath $outputFullPath -Destination $backupPath -Force
    Write-Host "Kopia poprzedniego pliku: $backupPath"
}

Move-Item -LiteralPath $tempCleanPath -Destination $outputFullPath -Force
Remove-Item -LiteralPath $tempRawPath -Force

Write-Host "Gotowe: $outputFullPath"
