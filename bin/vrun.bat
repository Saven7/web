@echo on
set path=%cd%
cd %path%\venv/Scripts
activate && set FLASK_APP=%path%\calc.py && flask run