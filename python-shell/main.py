"""
Python Practice Shell

This is the main file for the project 'Python Practice Shell'. This file defines the structure, command parsing algorithm as well as the command executing codes for the shell program. The entire project is powered by Python3, i.e., written in Python3 programming language.

Author : Rishav Das (https://github.com/rdofficial/)
Created on : May 9, 2021

Last modified by : Rishav Das (https://github.com/rdofficial/)
Last modified on : May 25, 2021

Changes made in the last modification :
1. Updated the initial working directory from the python script file's directory to the data/ directory.
2. Fixed the error for the command 'ls --directory' / 'ls -d'.

Authors contributed to this script (Add your name below if you have contributed) :
1. Rishav Das (github:https://github.com/rdofficial/, email:rdofficial192@gmail.com)
"""

# Importing the required modules
try:
	# Importing regular modules (the ones that are available in the standard python library)
	from os import system, path, listdir, remove, chdir, mkdir
	from sys import platform, argv as arguments

	# Importing the installed modules (the ones that are installed using pip3, or any external source)
	# 

	# Importing the self-defined modules (the custom modules created in this project)
	from modules import directory as DirectoryTools
	# from modules import 
except Exception as e:
	# If there are any errors during the importing of the modules, then we display the error on the console screen

	input(f'\n[ Error : {e} ]\nPress enter key to continue...')
	exit()

class Shell:
	def __init__(self):
		# Initially switching to the data/ directory as it is the default location for our shell
		if path.isdir(f'{path.dirname(__file__)}/data/'):
			# If the data/ directory exists, then we directly switch to it

			chdir(f'{path.dirname(__file__)}/data/')
		else:
			# If the data/ directory does not exists, then we first create it and then switch to it

			mkdir(f'{path.dirname(__file__)}/data/')
			chdir(f'{path.dirname(__file__)}/data/')
		
		# Setting the initial directory and the current working directory
		self.initialDirectory = f'{path.dirname(__file__)}/data/'
		self.currentWorkingDirectory = self.initialDirectory

		# Using a while true loop for infinite runtime of the shell, and would stop only if the user wants so
		while True:
			# The default shell prompt (It can be changed during thr runtime, if the user wants to)
			if self.currentWorkingDirectory == self.initialDirectory:
				# If the current working directory and the initial directory are same, then we donot display the working directory info on the shell prompt

				self.shellPrompt = 'wsb-shell:~$ '
			else:
				# If the current working directory and the initial directory are not same

				self.shellPrompt = f'wsb-shell:{self.currentWorkingDirectory}$ '

			# Asking the user to enter a command
			self.command = input(f'{self.shellPrompt}')

			# Parsing and executing the command
			token = self.commandParser()
			self.executeCommand(token)

			# The in-built commands defined in this shell
			# ----
			# 1. exit
			# 2. list-files / ls
			# 3. cd / chdir / change-dirrectory / change-dir
			# 4. add
			# ----

	def commandParser(self):
		""" """

		# The token which is a dictionary item, it contains the main command, as well as the arguments for the command
		token = {
		"command" : "",
		"arguments" : [],
		}

		# Setting the command to the token
		token["command"] = self.command.split(' ')[0].lower()

		# Setting the rest of the arguments from the command input
		for i in self.command.split(' ')[1:]: token["arguments"].append(i)
		return token

	def executeCommand(self, token):
		""" """

		# Executing the requested command on the basis of the token
		if token["command"] == '':
			# If the command is blank, then we skip the line

			pass
		elif token["command"] == 'exit':
			# If the user entered command is to exit the script, then we do it

			exit()
		elif token["command"] == 'list-files' or token["command"] == 'ls':
			# If the user entered command is to list the files and folders of the current directory, then we continue

			# Setting a blank variable for directory location
			directoryLocation = ''

			# Checking the user entered arguments
			if len(token["arguments"]) == 0:
				# If there are no arguments entered by the user, then we consider the current folder files to be listed

				directoryLocation = self.currentWorkingDirectory
			else:
				# If there are arguments entered by the user, then we consider the first argument to be the directory location

				if token["arguments"][0].lower() == '':
					# If the user entered argument is blank, then we consider the current working directory as the directory to be listed

					directoryLocation = self.currentWorkingDirectory
				elif token["arguments"][0].lower() == '--help':
					# If the user entered argument to display help info for list-files command, then we continue

					self.help('--help')
					return 0
				elif token["arguments"][0].lower() == '--tree' or token["arguments"][0].lower() == '-t':
					# If the user added the argument to display the directory info in the tree format

					if len(token["arguments"]) >= 2:
						# If the user entered 2 or more arguments, then we continue
					
						if token["arguments"][1] == '':
							# If the argument entered by the user is blank, then we conside the current working directory as the argument

							token["arguments"][1] = self.currentWorkingDirectory

						DirectoryTools.FilesLister(directory = token["arguments"][1], tree = True)
					else:
						# If the user does not entered more than 2 arguments, then we display an error on the console screen

						print(f'[ Error : Mention a directory location post --tree / -t argument ]')
					return 0
				elif token["arguments"][0].lower() == '--directory' or token["arguments"][0].lower() == '-d':
					# If the user added the argument to specify the directory, then we continue with it

					if len(token["arguments"]) >= 2:
						# If the user entered 2 or more arguments, then we continue
					
						if token["arguments"][1] == '':
							# If the argument entered by the user is blank, then we conside the current working directory as the argument

							token["arguments"][1] = self.currentWorkingDirectory

						DirectoryTools.FilesLister(token["arguments"][1])
					else:
						# If the user does not entered more than 2 arguments, then we display an error on the console screen

						print(f'[ Error : Mention a directory location post --directory / -d argument ]')
					return 0
				elif token["arguments"][0].lower() == '--size' or token["arguments"][0].lower() == '-s':
					# If the user added the argument to specify the size of the files too while listing them

					if len(token["arguments"]) >= 2:
						# If the user entered 2 or more arguments, then we continue
					
						if token["arguments"][1] == '':
							# If the argument entered by the user is blank, then we conside the current working directory as the argument

							token["arguments"][1] = self.currentWorkingDirectory

						DirectoryTools.FilesLister(directory = token["arguments"][1], size = True)
					else:
						# If the user does not entered more than 2 arguments, then we display an error on the console screen

						print(f'[ Error : Mention a directory location post --size / -s argument ]')
					return 0
				else:
					# If the argument is not recognized, then we treat it as the directory location

					directoryLocation = token["arguments"][0]

			# Printing the list of the files as per user specified directory location
			DirectoryTools.FilesLister(directory = directoryLocation)
			return 0
		elif token["command"] == 'change-directory' or token["command"] == 'change-dir' or token["command"] == 'chdir' or token["command"] == 'cd':
			# If the user entered command is to change the current working directory, then we continue the process

			# Checking for any argument to this command
			if len(token["arguments"]) == 0:
				# If there are no any arguments entered by the user, then we use the unix way and thus we kick the current working directory to the initial directory

				self.currentWorkingDirectory = self.initialDirectory
				chdir(self.currentWorkingDirectory)
			else:
				# If there are atleast 1 or more arguments entered by the user, then we continue to check them

				if token["arguments"][0] == '':
					# If the argument entered by the user is blank, then we make switch the current working directory to the initial directory

					self.currentWorkingDirectory = self.initialDirectory
					chdir(self.currentWorkingDirectory)
				else:
					# If the argument entered by the user is not blank, then we continue to check wheter a directory or not

					if path.isdir(token["arguments"][0]):
						# If the argument entered by the user is a existing directory, then we switch our current working directory to the user specified directory

						self.currentWorkingDirectory = token["arguments"][0]
						chdir(self.currentWorkingDirectory)
					else:
						# If the argument entered by the user is not an existing directory, then we check for other argument type

						if token["arguments"][0].lower(0) == '--help' or token["arguments"][0].lower(0) == '-h':
							# If the argument entered by the user asks for displaying the help info for the command, then we continue to do it

							self.help('cd')
						else:
							# If the argument entered by the user is neither recognized by the script nor it is a existing directory, then we display an directory not found error

							print(f'[ Error : No such directory "{token["arguments"][0]}" ]')
		elif token["command"] == 'add':
			# If the user command is to add, then we continue

			# Checking for the numeric arguments if exists
			if len(token["arguments"]) == 0:
				# If there are no arguments entered by the user

				print('[ add : requires arguments, use add --help for more info ]')
			else:
				# If there are atleast more than 0 arguments entered by the user

				isNumber = False
				for i in token["arguments"]:
					# if i.isnumeric():
					# 	isNumber = True
					# else:
					# 	isNumber = False
					# 	break

					# Checking wheter numeric or not
					try:
						i = float(i)
					except ValueError:
						# If the value error is encountered, it means the argument is not a numeric term

						isNumber = False
						break
					except Exception as e:
						# If there are any other errors encountered during the process, then we display the error on the console screen

						print(f'[ Error : Failed to parse the arguments for the command "{token["command"]}" ]')
						return 0
					else:
						# If there are no errors in the process, then we assume that the argument is a numebr

						isNumber = True
				if isNumber:
					# If the arguments are all numbers, then we continue to find out the sum

					result = 0
					for number in token["arguments"]:
						result += float(number)
					print(result)
				else:
					# If the arguments are not all numbers, then we continue to create a new file

					filename = token["arguments"][0]
					if filename.lower() == '--help':
						# If the user entered argument for displaying the help for the command, then here we go

						self.help(token["command"])
					else:
						choice = input('Creating a new file - Enter N to cancel : ')
						if choice.lower() == 'no' or choice.lower() == 'n':
							return 0
						else:
							open(f'data/{filename}', 'w+').write('')
							print(f'[ File created : {filename} ]')
		else:
			# If the user entered command is unrecognized, then we display an error on the console screen

			print(f'[ Command not recognized : {self.command.split(" ")[0]} ]')

	def help(self, command = None):
		""" This method / function serves the task of serving the help for the in-built commands defined in this shell project / application. This function takes 1 argument : command. The command argument is to be specified with a particular command of this shell. The function then prints the brief help information for that script on the console screen. The information would contain 2-3 lines for command purpose and then the arguments as well as the warning too. If the argument command is not specified, then the function displays the help info for the entire shell. """

		if command == None:
			# If the command is not mentioned, then we display the help info for the entire shell

			print(f'Help info for overall shell project - To be updated')
		else:
			# If the command is mentioned, then we display the help info for the specified command

			print(f'Help info for command : {command}')

if __name__ == '__main__':
	try:
		shell = Shell()
	except KeyboardInterrupt:
		# If the user presses CTRL+C key combo, then we exit the script

		print('\n[ Exiting the shell ]')
		exit()
	except Exception as e:
		# If there are any errors during the process, then we display the error on the console screen

		print(f'[ Error {e} ]')