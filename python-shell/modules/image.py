"""
image.py - Python Shell

A module created for supplying the required functions to the shell application. The functions and classes defined in this module ease many tasks at the shell application, in general way they are used in executing the task assigned by the user via the commands. This module contains functions and classes related to directory handling and other such stuff.

Author : Rishav Das (https://github.com/rdofficial/)
Created on : June 18, 2021

Last modified by : Rishav Das (https://github.com/rdofficial/)
Last modified on : June 18, 2021

Changes made in the last modification :
1. Added the code for importing all the required modules (the standard python module that are required for all the functions and classes defined in this file to be run properly without any errors).

Authors contributed to this script (Add your name below if you have contributed) :
1. Rishav Das (github:https://github.com/rdofficial/, email:rdofficial192@gmail.com)
"""

# Importing the required functions and modules
try:
	from base64 import b64encode, b64decode, decodebytes
	from io import TextIOWrapper
	from os import stat, path
except Exception as e:
	# If there are any errors during the importing of the modules, then we display the error on the console screen

	input(f'\n[ Error : {e} ]\nPress enter key to continue...')
	exit()

class ImageDetails:
	""" """

	def __init__():
		pass

	def getimgdetails(self):
		pass

class ImageResizer:
	""" """

	def __init__(self):
		pass

	def resize(self):
		pass

	def compress(self):
		pass

	def getimgdetails(self):
		pass

class ImageRawConverter:
	""" """

	def __init__(self):
		pass

	def makeraw(self):
		pass

	def makeimage(self):
		pass

	def getimgdetails(self):
		pass