@echo off
set path=C:\Users\saven\Documents\calc
cd %path%

:loop
C:\Windows\System32\choice /c:RT
if "%errorlevel%"=="1" goto flask
if "%errorlevel%"=="2" break

:flask
set FLASK_APP=calc.py
start flask run

goto loop