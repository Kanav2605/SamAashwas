@echo off
REM CivicSense AI / SamAashwas Git Sync Helper
echo [SamAashwas] Initializing and pushing to GitHub...
cd /d "%~dp0"

IF NOT EXIST ".git" (
    echo Initializing Git repository...
    git init
    git branch -M main
    git remote add origin https://github.com/Kanav2605/SamAashwas.git
)

echo Adding files...
git add .

set /p COMMIT_MSG="Enter commit message (or press Enter for default): "
IF "%COMMIT_MSG%"=="" set COMMIT_MSG="feat: complete CivicSense AI municipal platform implementation"

git commit -m "%COMMIT_MSG%"
echo Pushing to origin main...
git push -u origin main

echo [SamAashwas] Push complete!
pause
