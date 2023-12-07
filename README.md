# Zoo Mapper

## About
This python program is a resource to go along with ZooMonitor© and other animal data collection applications. ZooMapper creates plots for 2D and 3D datasets, allows for interactive viewing and filtering of data, and can perform calculations for distances between animals. 

### File Structure
- `/data`: folder to contain data files, either as .xlsx or .csv
- `/src/main/resources`: contains image assets
- `/src/main`: python files
  - `zoo.py`: Main program file. Contains methods for handling imports, exporting distance calculations, and the spreadsheet view
  - `heatmap.py`: Handles methods for creating import configuration, and saving an import
  - `heatmappage.py`: Plotting of graphs, highlighting points, and real time distance calculating on graph
  - `pages.py`: Frames for the different pages of the application
  - `error.py`: provides error messages for error handling
- `/src/main/saves`: contains save configurations of imports. Saves as `.json` files

### Required packages
The following Python packages are used in this application and are all found in `requirements.txt`
- `matplotlib` version 3.1.1
- `numpy` version 1.16.5
- `pandas` version 0.25.1
- `pillow` version 6.2.0
- `scipy` version 1.3.1
- `tkinter` version 0.1.0
- `tksheet` version 5.0.25
- `xlrd` version 1.2.0
- `openpyxl` any version

## Setting up the program
First, you will need to install a Python version newer than 3.6. We reccoment installing python version 3.9.5 as this was the newest version during our development. The instructions on how to install Python 3.9.5 for your device can be found [here](https://www.python.org/downloads/).

### For Windows (revamped)
If you are using a Windows system, open up the command prompt (seach cmd in the serach bar). Start by cloning this repository by running `git clone https://github.com/sydneyph/Zoo-Mapper.git`.
1. Install R → remember its path
2. Install Python (the current version)
3. Go to VScode
4. Navigate to the Zoo-Mapper directory in the terminal
5. `pip install numpy matplotlib pandas pillow scipy tk tksheet xlrd rpy2 openpyxl`
    * If this doesn't work, then install these libraries separately, xlrd might need `pip install --user xlrd` .
6. Go to windows search bar → type in env and hit enter
7. On the bottom right click environment variables
8. Go to system variables → new
    * Variable name: R_HOME
    * Variable value: *Your path to your R in program files*
    * Example: **C:\Program Files\R\R-4.3.1**
9. Click OK
10. Edit your path variable (Make sure it’s the one in system variables) → New
11. Type in *Your previous path/bin/(whatever folder your R.exe is in)*
    * Example: **C:\Program Files\R\R-4.3.1\bin\x64**
12. Click OK
13. Go back to vscode
14. Run zoo.py
### Setup For Windows (Using Batch File)
1. Click on setup.bat inside of the setup folder
3. If you have not downloaded python, please allow the system to install python onto your system
4. If you have not downloaded R, please allow the system to install R onto your system
   * When installing, make sure it intalls in the folder C:\Program Files\R
5. You should be done! Zoo-Mapper will load automatically from this point and future runs can be completed using Zoo-Mapper.bat
### For Mac/Linux
If you are using a Mac or Linux system, open a unix shell. Start by cloning this repository by running `git clone https://github.com/channum/Zoo-Mapper.git`. Then do `cd sezarc` and press enter to move into the project directory. Here, execute the command `pip install -r requirements.txt`. This will install the required packages that were listed above. Now you are all set to get ready to run the application.

## Running the Program
First, navigate from the main sezarc directory to the directory `/src/main` by running `cd src/main`. Then, simply execute `python zoo.py`.

## ZooMapper Tutorials
We have a few tutorial videos that can help you learn how to use the application. Below are links to the different videos:
- [Importing a Spreadsheet](https://udel.zoom.us/rec/share/VCGKLe5nntcPSUNYJkbaEekL52scUIWGUSg2HzuWJL4pfsbGY5w8EI0WutgUqGer.UmCEEjVtGqZwWM8G?startTime=1622577255000)
- [Saving and Loading an Import](https://udel.zoom.us/rec/share/32WImZp6MNGgyktIQaTj68yvUDfJDmx7VVMOovH93ugVZmMoMgU8mflVTY-AZxdv.MQ0zBIGSD8YWWYkS?startTime=1622477688000)
- [The Graph Page](https://udel.zoom.us/rec/share/lVjZzdUA_8LlPKqdI1Sis832SjrBP4Dgrp9Hyho4CiG7HQftJ6mjHsQ8-TfOjl3y.h1LNrsZTN2d3zNT1)
- [Exporting Calculations](https://udel.zoom.us/rec/share/VCGKLe5nntcPSUNYJkbaEekL52scUIWGUSg2HzuWJL4pfsbGY5w8EI0WutgUqGer.UmCEEjVtGqZwWM8G?startTime=1622577759000)
