@echo off
python --version >NUL
if errorlevel 1 goto nopython

:checkpip
pip --version >NUL
if errorlevel 1 goto nopip

:showoutput
if NOT "%errormsg%" == "" goto showerror

echo Installing opencv
pip install opencv-python
echo Installing TextToSpeech modules
pip install pyttsx3
pip install pywin32
echo ------------------------
echo ------------------------
pip show opencv-python >NUL
if errorlevel 1 echo Failed to download opencv-python

pip show pyttsx3 >NUL
if errorlevel 1 echo Failed to download pyttsx3

pip show pywin32 >NUL
if errorlevel 1 echo Failed to download pywin32

echo ------------------------
echo ------------------------
echo Installation done
pause
goto:eof


:nopython
set "errormsg=Python is not detected. "
goto checkpip

:nopip
set "errormsg=%errormsg%Pip is not detected."
goto showoutput

:showerror
echo ------------------------
echo ------------------------
echo %errormsg%
pause