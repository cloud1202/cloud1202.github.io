@echo off
REM ========================================
REM GitHub Pages 자동화 BAT 파일 모음
REM ========================================

REM =====================================================
REM 1) 로컬 서버 실행용 serve.bat
REM =====================================================
:: serve.bat
cd /d "%~dp0"
bundle exec jekyll serve --livereload
start http://localhost:4000
pause


