#!/bin/bash

pwd

:: Install Python to system
::python-3.12.0-amd64.exe 

pip install numpy matplotlib pandas pillow scipy tk tksheet xlrd rpy2 openpyxl selenium docx

:: Install R to System
::R-4.3.1-win.exe

:: INSTALL THE ENVIRONMENT VARIABLES for path and RHOME

::start setx /M path "%PATH%;C:\Program Files\R\R-4.3.1\bin\x64"
::start setx /M R_HOME "C:\Program Files\R\R-4.3.1"
:: Move into the directory with zoo.py
cd ../src/main

:: Run the SEZAEC App
python zoo.py

PAUSE