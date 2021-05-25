"""
directory.py - Python Practice Shell

A module created for supplying the required functions to the shell application. The functions and classes defined in this module ease many tasks at the shell application, in general way they are used in executing the task assigned by the user via the commands. This module contains functions and classes related to directory handling and other such stuff.

Author : Rishav Das (https://github.com/rdofficial/)
Created on : May 9, 2021

Last modified by : Rishav Das (https://github.com/rdofficial/)
Last modified on : May 25, 2021

Changes made in the last modifications :
1. Updated the size listing format specifier in the FilesLister(size = True). From integer %d to float %f format specifier.
2. Added the feature to display the quantity of the files in the directory whose files are to be listed.

Authors contributed to this script (Add your name below if you have contributed) :
1. Rishav Das (github:https://github.com/rdofficial/, email:rdofficial192@gmail.com)
"""

# Importing the required functions and modules
try:
	from os import path, listdir, stat
except Exception as e:
	# If there are any errors during the importing of the modules, then we display the error on the console screen

	input(f'\n[ Error : {e} ]\nPress enter key to continue...')
	exit()

class FilesLister:
	""" This class is used to list files in a directory in various ways. There are many methods and functions that are defined under this class. We can use this function to get our desired output of the files listing on the console screen. Just check the below information for proper usage of this class :

1. To list the files of a directory: module.FilesLister(directory = '/directory/location/')
2. To list the files of a directory along with the file sizes : module.FilesLister(directory = '/directory/location', size = True)
3. To list the files of a directory in tree format : module.FilesLister(directory = '/directory/location', tree = True)"""

	def __init__(self, directory = 'data/', size = False, tree = False):
		# First, we will check wheter the specified directory exists or not
		if path.isdir(directory) == False:
			# If the specified directory does not exists, then we display an error on the console screen

			print(f'[ Error : No such directory "{directory}" ]')
		else:
			# If the specified directory exists, then we continue

			# Checking for the other parameters mentioned
			if size:
				# If the argument for displaying the size as well is also mentioned, then we continue

				print(f'\nContents of "{directory}" :')
				files = listdir(directory)
				for file in files:
					if path.isfile(file):
						# If the currently iterated item is a file, then we mention its size

						print('[*] %-40s    %.2f KB' %(file, (stat(directory + '/' + file).st_size / 1024)))
					elif path.isdir(file):
						# If the currently iterated item is a directory, then we do not mention its size 
						# ----
						# 1. The directory sizes are'not calculated that easily, they requires per file calculation. So, if we see the stats of the directory using the regular way, then we can only see the 4KBs of the space it takes for  the directory node, not the actual size of the overall contents inside the folder
						# ----

						print('[*] %-40s    ----- KB' %(file))
					else:
						# If the currently iterated item is neither a file nor a directory, then we print it as per the way we did for the files

						print('[*] %-40s    %-5d KB' %(file, (stat(directory + '/' + file).st_size / 1024)))
				print(f'\nTotal files : {len(files)}')
			elif tree:
				# If the argument for displaying the list of files in tree format

				print(f'\nThe tree format for "{directory}" :')
				self.files = []
				self.tree(directory)
				for file in self.files:
					print(f'[*] {file}')
				print(f'\nTotal files : {len(self.files)}')
				del self.files
			else:
				# If there are no arguments defined, then we list the files in plain form

				print(f'\nContents of "{directory}" :')
				files = listdir(directory)
				for file in files:
					print(f'[*] {file}')
				print(f'\nTotal files : {len(files)}')

	def tree(self, directory):
		""" This method of the FilesLister class, returns the total files in the directory and even inside it's sub directories and more inside too. As the name says, the tree of the files. The function when called requires an argument, the directory location of where we want to list the files in the tree format. Also, note the algorithm used by the function is very different. It first iterates through an directory and then append the listed files to a class variable (property) list, and then proceed to each sub-directories using the same algorithm. Thus, we need also to define an object with the class FilesLister, before using this method alone. The class variable where this function saves the fetched file list is a list / array type data object named as files (self.files). """

		for file in listdir(directory):
			# Iterating through each components (either file or a sub-directory) in the directory
			
			# Giving absolute path to the files / sub-directories
			file = directory + '/' + file
			file.replace('//', '/')

			# Checking wheter a file or directory
			if path.isfile(file):
				# If the currently iterated item is a file, then we append it to the self.files array

				self.files.append(file)
			elif path.isdir(file):
				# If the currently iterated item is a directory, then we continue to iterate it again by calling the method tree() again with the parameter of the absolute path of the currently iterated item

				self.tree(file)
			else:
				# If the current iterated item is neither a file nor a directory, then we skip the current iteration

				continue