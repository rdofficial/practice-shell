"""
regular.py - Python Shell

A module created for supplying the required functions to the shell application. The functions and classes defined in this module ease many tasks at the shell application, in general way they are used in executing the task assigned by the user via the commands. This module contains functions and classes related to directory handling and other such stuff.

Author : Rishav Das (https://github.com/rdofficial/)
Created on : May 25, 2021

Last modified by : -
Last modified on : -

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

class TerminalCommands:
	""" This class contains the variables which are the terminal commands like clearing the screen, pwd, etc. The terminal commands are defined as per the operating system type. If the linux, else windows. """

	if 'linux' in platform:
		# If the platform is of linux type, then we define the terminal commands as per the linux operating system

		CLEAR = 'clear'
	else:
		# If the platform is not if linux type, then we define the terminal commands as per the windows operating system

		CLEAR = 'cls'