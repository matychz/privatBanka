# Skript pro spuštění generátoru logů
$scriptPath = Join-Path $PSScriptRoot "log_generator.py"

if (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Host "Spouštím generátor logů..." -ForegroundColor Cyan
    python -u $scriptPath
} else {
    Write-Error "Python nebyl nalezen. Ujistěte se, že máte nainstalován Python a je v cestě (PATH)."
}
