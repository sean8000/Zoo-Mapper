from tkinter.ttk import Style
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
from tokenize import Double
from numpy import double, true_divide
import pandas as pd
import numpy as np
#import rpy2.robjects as robjects
#from rpy2.robjects import NULL, pandas2ri
#from rpy2.robjects import r
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import pandas as pd
import csv
import subprocess
import multiprocessing
import threading
import re
import json
import os

from joins_both import Joins_Page_Both
from joins_light import Joins_Page_Light
from joins_rubbing import Joins_Page_Rubbing
import heatmappage


LARGE_FONT = ("Bell Gothic Std Black", 40, 'bold')
MEDIUM_FONT = ("Bell Gothic Std Black", 25, 'bold')
BUTTON_FONT = ('Calibiri', 14, 'bold')
BACKGROUND_COLOR = '#407297'
LIGHT_BLUE = '#d4e1fa'

class Joins_Home_Page(tk.Frame):
	def __init__(self, parent, controller):
		"""
		This function creates the landing page when users decide to run any joins, they select which type 
		of join they want to do in this file. We will be able to select the file we want to
		run, run it and return to the home page
		Inputs:
			self: Represents the page that we have created
			parent:
			controller: 
		Results:
			The page will be up and ready for the user to interact with
		"""
		# Setting our variables

		# Creating the title of the web page
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Data Transformations", font=MEDIUM_FONT)    # Creates the title of the web page
		label.pack(pady=10, padx=10)                                                # Padding the name

		# Creating Buttons for web page
		#The light join, the rubbing join(not really a join but fits here best), join that does both, home button
		joins_light = ttk.Button(self, text="Joins(Light/Temp)",
							command=lambda: controller.show_frame(Joins_Page_Light))
		joins_light.pack()

		joins_rubbing = ttk.Button(self, text="Joins(Rubbing)",
							command=lambda: controller.show_frame(Joins_Page_Rubbing))
		joins_rubbing.pack()

		joins_both = ttk.Button(self, text="Joins(Both)",
							command=lambda: controller.show_frame(Joins_Page_Both))
		joins_both.pack()

		back_button = ttk.Button(self, text="Back to Home",
							command=lambda: controller.show_frame(heatmappage.StartPage))    # setting up the back to home button. goes back to start page for heat map
		back_button.pack()