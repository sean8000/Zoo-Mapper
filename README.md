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
- `selenium` version  4.19.0
- `docx` version 0.2.4
- `time` version 1.0.0
- `pandas` version 2.1.2
- `datetime` any version

### For Mac/Linux
If you are using a Mac or Linux system, open a unix shell. Start by cloning this repository by running `git clone https://github.com/channum/Zoo-Mapper.git`. Then do `cd sezarc` and press enter to move into the project directory. Here, execute the command `pip install -r requirements.txt`. This will install the required packages that were listed above. Now you are all set to get ready to run the application.

## Running the Program
Simply Click on zoo.exe to run on windows. This will create a pop-up window with the Zoo-Mapper UI.

## ZooMapper Tutorials
We have a few tutorial videos that can help you learn how to use the application. Below are links to the different videos:
- [Importing a Spreadsheet](https://udel.zoom.us/rec/share/VCGKLe5nntcPSUNYJkbaEekL52scUIWGUSg2HzuWJL4pfsbGY5w8EI0WutgUqGer.UmCEEjVtGqZwWM8G?startTime=1622577255000)
- [Saving and Loading an Import](https://udel.zoom.us/rec/share/32WImZp6MNGgyktIQaTj68yvUDfJDmx7VVMOovH93ugVZmMoMgU8mflVTY-AZxdv.MQ0zBIGSD8YWWYkS?startTime=1622477688000)
- [The Graph Page](https://udel.zoom.us/rec/share/lVjZzdUA_8LlPKqdI1Sis832SjrBP4Dgrp9Hyho4CiG7HQftJ6mjHsQ8-TfOjl3y.h1LNrsZTN2d3zNT1)
- [Exporting Calculations](https://udel.zoom.us/rec/share/VCGKLe5nntcPSUNYJkbaEekL52scUIWGUSg2HzuWJL4pfsbGY5w8EI0WutgUqGer.UmCEEjVtGqZwWM8G?startTime=1622577759000)
