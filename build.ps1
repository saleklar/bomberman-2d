#!/usr/bin/env powershell
# Build Bomberman.exe using PyInstaller

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Building Bomberman.exe" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan

# Ensure virtual environment is activated
$venvPath = ".\.venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & $venvPath
} else {
    Write-Host "Warning: Virtual environment not found at $venvPath" -ForegroundColor Red
}

# Check if PyInstaller is installed
Write-Host "Checking PyInstaller..." -ForegroundColor Yellow
python -m pip list | Select-String "pyinstaller" > $null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing PyInstaller..." -ForegroundColor Yellow
    python -m pip install pyinstaller
}

# Clean old builds
Write-Host "Cleaning old build files..." -ForegroundColor Yellow
if (Test-Path "build") { Remove-Item "build" -Recurse -Force }
if (Test-Path "dist") { Remove-Item "dist" -Recurse -Force }

# Run PyInstaller
Write-Host "Running PyInstaller..." -ForegroundColor Yellow
pyinstaller --onefile `
    --windowed `
    --name "Bomberman" `
    --icon "bomberman_2d\icon.ico" `
    --add-data "bomberman_2d\sprites:sprites" `
    "bomberman_2d\main.py"

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n==================================" -ForegroundColor Green
    Write-Host "Build successful!" -ForegroundColor Green
    Write-Host "Executable: dist\Bomberman.exe" -ForegroundColor Green
    Write-Host "==================================" -ForegroundColor Green
} else {
    Write-Host "`nBuild failed!" -ForegroundColor Red
    exit 1
}
