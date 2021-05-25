"""
regular.py - Python Shell

A module created for supplying the required functions to the shell application. The functions and classes defined in this module ease many tasks at the shell application, in general way they are used in executing the task assigned by the user via the commands. This module contains functions and classes related to directory handling and other such stuff.

Author : Rishav Das (https://github.com/rdofficial/)
Created on : May 25, 2021

Last modified by : Rishav Das (https://github.com/rdofficial/)
Last modified on : May 25, 2021

Changed made in the last modification :
1. Created the ColorVar class which contains all the color variables used for color output.

Authors contributed to this script (Add your name below if you have contributed) :
1. Rishav Das (github:https://github.com/rdofficial/, email:rdofficial192@gmail.com)
"""

# Importing the required functions and modules
try:
	from sys import platform
except Exception as e:
	# If there are any errors during the importing of the modules, then we display the error on the console screen

	input(f'\n[ Error : {e} ]\nPress enter key to continue...')
	exit()

class ColorVar:
	""" This function contains the color code variables which are used for printing colored output to the user. The colored output is made using the ANSII color codes supported by the linux/unix operating system's default terminal (bash). Thus, we can say that the color codes are only for the linux operating system and not for the windows. Also, the code is written as so that in the case of the windows, the color variable become an empty string. """

	if 'linux' in platform:
		# If the platform is of linux type, then we define the ANSII color code variables

		RED = '\033[91m'
		GREEN = '\033[92m'
		YELLOW = '\033[93m'
		BLUE = '\033[94m'
		RED_REV = '\033[07;91m'
		YELLOW_REV = '\033[07;93m'
		DEFCOL = '\033[00m'
	else:
		# If the platform is not if linux type, then we define the color variables as empty strings

		RED = ''
		GREEN = ''
		YELLOW = ''
		BLUE = ''
		RED_REV = ''
		YELLOW_REV = ''
		DEFCOL = ''

class TerminalCommands:
	""" This class contains the variables which are the terminal commands like clearing the screen, pwd, etc. The terminal commands are defined as per the operating system type. If the linux, else windows. """

	if 'linux' in platform:
		# If the platform is of linux type, then we define the terminal commands as per the linux operating system

		CLEAR = 'clear'
	else:
		# If the platform is not if linux type, then we define the terminal commands as per the windows operating system

		CLEAR = 'cls'