@echo off
REM Change to the directory where your script is located
cd "C:\Users\vinov\Documents\Development\currency-convertor\.venv\Scripts\"

REM Activate the virtual environment (if needed for specific packages)
call activate.bat

REM Change to the directory where your python script is located
call cd ..
call cd ..

REM Run your Python script
python main.py

REM Deactivate the virtual environment (optional, but good practice)
call deactivate.bat

REM Optional: Pause to see output if running manually
REM pause