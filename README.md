# TUTOR

## Description
Purpose of this application is to help users with learning information collected as a set of questions and answers. Simular pattern of learning is used in flashcards, wildly used in languages learning.

## Configuration from source code
Create virtual environment  
_$ python3 -m venv <virtual environment file name>_
Activate virtual environment  
_$ source venv/bin/activate_
Download dependencies
_$ python3 -m pip install -r requirements.txt_

## Run program
In previously created and configured virtual environment run command:
_$ python3 src/run_gui.py_

## Additional information
### Generating python model files from PySide/PyQt .ui files
*pyside6-uic src/gui/<file_name>.ui -o src/gui/<file_name>_ui.py -g python*
