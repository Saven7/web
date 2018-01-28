@echo on
set path=.
cd %path%
C:\Windows\System32\choice.exe /C:RD /T:5 /D:R /N /M:"Press R to start Program, D to develop further."
if '%errorlevel%'=='1' goto vrun
if '%errorlevel%'=='2' start venv.bat
goto end
:vrun
start vrun.bat
echo HI
pause
goto end
:end
exit