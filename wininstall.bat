@echo off
python --version >NUL
if errorlevel 1 goto nopython

:checkpip
pip --version >NUL
if errorlevel 1 goto nopip

:showoutput
if NOT "%errormsg%" == "" goto showerror

echo Installing Opencv
pip install opencv-python

echo Installing TextToSpeech dependencies
pip install pyttsx3
pip install pywin32

echo Installing Machine Learning dependencies
pip install scikit-learn
pip install tensorflow
pip install keras

echo Installing User Interface dependencies
pip install pyqt5
pip install matplotlib

echo ------------------------
echo ------------------------

pip show opencv-python >NUL
if errorlevel 1 echo Failed to download opencv-python

pip show pyttsx3 >NUL
if errorlevel 1 echo Failed to download pyttsx3

pip show pywin32 >NUL
if errorlevel 1 echo Failed to download pywin32

pip show scikit-learn >NUL
if errorlevel 1 echo Failed to download scikit-learn

pip show tensorflow >NUL
if errorlevel 1 echo Failed to download tensorflow

pip show keras >NUL
if errorlevel 1 echo Failed to download keras

pip show pyqt5 >NUL
if errorlevel 1 echo Failed to download pyqt5

pip show matplotlib >NUL
if errorlevel 1 echo Failed to download matplotlib

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