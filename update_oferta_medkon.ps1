param(
    [string]$Url = "https://medkon.pl/module/ceneo_xml/generate?secure_key=02f527f2c560e9b762d0025ef90d2179&id_shop=1&show_output=0",
    [string]$OutputPath = "oferta_medkon.xml",
    [switch]$KeepBackup,
    [int]$MinOfferCount = 1
)

$ErrorActionPreference = "Stop"

$workspace = Split-Path -Parent $MyInvocation.MyCommand.Path
$outputFullPath = [System.IO.Path]::GetFullPath((Join-Path $workspace $OutputPath))
$tempRawPath = Join-Path $workspace "oferta_medkon.download.tmp"
$tempXmlPath = Join-Path $workspace "oferta_medkon.xml.tmp"
$backupPath = Join-Path $workspace "oferta_medkon.xml.bak"
$logPath = Join-Path $workspace "oferta_medkon_update.log"

function Write-Log {
    param([string]$Message)

    $line = "{0} {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $Message
    Write-Host $line
    Add-Content -LiteralPath $logPath -Value $line -Encoding UTF8
}

function Remove-TempFiles {
    Remove-Item -LiteralPath $tempRawPath, $tempXmlPath -Force -ErrorAction SilentlyContinue
}

function Download-File {
    param(
        [string]$SourceUrl,
        [string]$DestinationPath
    )

    Write-Log "Pobieram: $SourceUrl"
    Invoke-WebRequest -Uri $SourceUrl -OutFile $DestinationPath -UseBasicParsing
}

function Copy-XmlFromDownloadedFile {
    param(
        [string]$SourcePath,
        [string]$DestinationPath
    )

    $reader = [System.IO.StreamReader]::new($SourcePath, $true)
    $writer = [System.IO.StreamWriter]::new($DestinationPath, $false, [System.Text.UTF8Encoding]::new($false))
    $started = $false

    try {
        while (($line = $reader.ReadLine()) -ne $null) {
            if (-not $started) {
                if ($line -match '^\s*(<\?xml|<offers\b)') {
                    $started = $true
                }
                else {
                    continue
                }
            }

            $writer.WriteLine($line)
        }
    }
    finally {
        $reader.Close()
        $writer.Close()
    }

    return $started
}

try {
    Remove-TempFiles

    Download-File -SourceUrl $Url -DestinationPath $tempRawPath

    if ((Get-Item -LiteralPath $tempRawPath).Length -eq 0) {
        throw "Pobrana odpowiedz jest pusta. Nie podmieniam $OutputPath."
    }

    $rawPreview = Get-Content -LiteralPath $tempRawPath -Raw
    if ($rawPreview -notmatch '^\s*(<\?xml|<offers\b)') {
        if ($rawPreview -match 'href="([^"]+)"') {
            $downloadUrl = [System.Net.WebUtility]::HtmlDecode($Matches[1])
            Write-Log "Odpowiedz nie jest XML. Znaleziono link do pobrania."
            Download-File -SourceUrl $downloadUrl -DestinationPath $tempRawPath
        }
        else {
            throw "Pobrana odpowiedz nie jest XML i nie zawiera linku download. Nie podmieniam $OutputPath."
        }
    }

    Write-Log "Przygotowuje XML do walidacji."
    $hasXmlStart = Copy-XmlFromDownloadedFile -SourcePath $tempRawPath -DestinationPath $tempXmlPath

    if (-not $hasXmlStart) {
        throw "Nie znaleziono poczatku XML w pobranym pliku. Nie podmieniam $OutputPath."
    }

    if ((Get-Item -LiteralPath $tempXmlPath).Length -eq 0) {
        throw "Przygotowany XML jest pusty. Nie podmieniam $OutputPath."
    }

    [xml]$xml = Get-Content -LiteralPath $tempXmlPath -Raw

    if ($xml.DocumentElement.Name -ne "offers") {
        throw "Niepoprawny root XML: $($xml.DocumentElement.Name). Oczekiwano offers. Nie podmieniam $OutputPath."
    }

    $offerCount = @($xml.offers.o).Count
    if ($offerCount -lt $MinOfferCount) {
        throw "XML zawiera za malo ofert: $offerCount. Minimum: $MinOfferCount. Nie podmieniam $OutputPath."
    }

    if ($KeepBackup -and (Test-Path $outputFullPath)) {
        Copy-Item -LiteralPath $outputFullPath -Destination $backupPath -Force
        Write-Log "Kopia poprzedniego pliku: $backupPath"
    }

    Move-Item -LiteralPath $tempXmlPath -Destination $outputFullPath -Force
    Write-Log "Gotowe: $outputFullPath"
    Write-Log "Liczba ofert: $offerCount"
}
finally {
    Remove-TempFiles
}
