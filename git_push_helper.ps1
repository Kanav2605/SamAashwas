# CivicSense AI / SamAashwas Git Sync Helper (PowerShell)
param (
    [string]$CommitMessage = "feat: build complete CivicSense AI municipal platform"
)

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $RepoRoot

Write-Host "=== SamAashwas CivicSense AI Git Sync ===" -ForegroundColor Cyan

if (-not (Test-Path ".git")) {
    Write-Host "Initializing Git repository..." -ForegroundColor Yellow
    git init
    git branch -M main
    git remote add origin https://github.com/Kanav2605/SamAashwas.git
} else {
    $currentRemote = git remote get-url origin 2>$null
    if (-not $currentRemote) {
        git remote add origin https://github.com/Kanav2605/SamAashwas.git
    }
}

Write-Host "Staging files..." -ForegroundColor Yellow
git add .

Write-Host "Committing with message: '$CommitMessage'..." -ForegroundColor Yellow
git commit -m "$CommitMessage"

Write-Host "Pushing to GitHub (Kanav2605/SamAashwas main)..." -ForegroundColor Green
git push -u origin main

Write-Host "Done!" -ForegroundColor Green
