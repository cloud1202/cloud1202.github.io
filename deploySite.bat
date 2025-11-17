@echo off
REM =====================================================
REM 2) GitHub Pages 배포용 deploy.bat
REM =====================================================
:: deploy.bat
cd /d "%~dp0"
bundle exec jekyll clean
bundle exec jekyll build

REM Git add, commit, push
set COMMITMSG=Update site %date% %time%
git add .
git commit -m "%COMMITMSG%"
git push origin main
pause
