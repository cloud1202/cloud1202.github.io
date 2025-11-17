@echo off
REM =====================================================
REM 2) GitHub Pages 배포용 deploy.bat
REM =====================================================
:: deploy.bat
cd /d "%~dp0"

REM Git add, commit, push
set COMMITMSG=Update site %date% %time%
git add .
git commit -m "%COMMITMSG%"
git push origin main
bundle exec jekyll clean
pause
bundle exec jekyll build

pause
