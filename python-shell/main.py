"""
Python Shell

This is the main file for the project 'Python Practice Shell'. This file defines the structure, command parsing algorithm as well as the command executing codes for the shell program. The entire project is powered by Python3, i.e., written in Python3 programming language.

Author : Rishav Das (https://github.com/rdofficial/)
Created on : May 9, 2021

Last modified by : Rishav Das (https://github.com/rdofficial/)
Last modified on : June 17, 2021

Changes made in the last modification :
1. Added the code for serving the functionality of the command 'mail' and all its sub-tasks to the shell.

Authors contributed to this script (Add your name below if you have contributed) :
1. Rishav Das (github:https://github.com/rdofficial/, email:rdofficial192@gmail.com)
"""

# Importing the required modules
try:
	# Importing regular modules (the ones that are available in the standard python library)
	from os import system as cmd, path, listdir, remove, chdir, mkdir
	from sys import platform, argv as arguments

	# Importing the installed modules (the ones that are installed using pip3, or any external source)
	# 

	# Importing the self-defined modules (the custom modules created in this project)
	from modules import directory as DirectoryTools
	from modules.regular import TerminalCommands
	from modules.characters import NumberDetails
	from modules.networking import IP, HttpServer, HttpRequest, Connections, Mail
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

		# BASIC COMMANDS
		# ----
		elif token["command"] == 'exit':
			# If the user entered command is to exit the script, then we do it

			print('[ Exiting the shell ]')
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

					self.help(command = '--help')
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

						if token["arguments"][0].lower() == '--help' or token["arguments"][0].lower() == '-h':
							# If the argument entered by the user asks for displaying the help info for the command, then we continue to do it

							self.help(command = 'cd')
						else:
							# If the argument entered by the user is neither recognized by the script nor it is a existing directory, then we display an directory not found error

							print(f'[ Error : No such directory "{token["arguments"][0]}" ]')
		elif token["command"] == 'clear':
			# If the user entered command is to clear the terminal / console screen, then we continue

			# Clearing the terminal screen
			cmd(TerminalCommands.CLEAR)
		# ----

		# IP RELATED COMMANDS
		# ----
		elif token["command"] == 'ip':
			# If the user entered command is for ip related tasks, then we continue

			# Checking for the numeric arguments if exists
			if len(token["arguments"]) == 0:
				# If there are no arguments entered by the user

				print('[ ip : requires arguments, use ip --help for more info ]')
			else:
				# If there are atleast more than 0 arguments entered by the user

				if token["arguments"][0] == 'self':
					# If the argument entered by the user asks for displaying information related to the IP address of the local machine and local network

					IP().localinfo()
				elif token["arguments"][0] == 'track':
					# If the argument entered by the user asks for tracking a required IP address, then we continue

					# Getting the IP address input
					ip = ''
					if len(token["arguments"]) >= 2:
						# If there are equal or more than 2 arguments entered by the user, then we assume the second argument as the user entered IP address to track

						ip = token["arguments"][1]
					else:
						# If there are less than 2 arguments entered by the user, then we manually ask the user for the IP address
						
						ip = input('Enter the IP address : ')

					# Tracking the user specified IP address
					IP(address = ip).track()
				elif token["arguments"][0] == 'portscan':
					# If the argument entered by the user asks for port scanning the particular IP address, then we continue

					# Getting the IP address input
					ip = ''
					if len(token["arguments"]) >= 2:
						# If there are equal or more than 2 arguments entered by the user, then we assume the second argument as the user entered IP address to port scan for

						ip = token["arguments"][1]
					else:
						# If there are less than 2 arguments entered by the user, then we manually ask the user for the IP address

						ip = input('Enter the IP address : ')

					if len(token["arguments"]) >= 4:
						# If there are equal or more than 4 arguments entered by the user, then we assume the third argument as the start port and the fourth argument as the end port to scan for

						# Setting the port number range from the arguments
						number1 = token["arguments"][2]
						number2 = token["arguments"][3]
						
						# Starting a port scan attack on the user specified IP address
						IP(address = ip).portscan(initial = number1, final = number2)
					else:
						# If there are less than 4 arguments entered by the user, then we start from 1 to 65500 port number for the scanning

						# Starting a port scan attack on the user specified IP address (with default port number range)
						IP(address = ip).portscan()
				elif token["arguments"][0] == 'gethostbyname':
					# If the argument entered by the user asks for fetching the host IP address by name, then we continue

					# Getting the hostname input
					ip = ''
					if len(token["arguments"]) >= 2:
						# If there are equal or more than 2 arguments entered by the user, then we assume the second argument as the user entered hostname to fetch IP address

						ip = token["arguments"][1]
					else:
						# If there are less than 2 arguments entered by the user, then we manually ask the user for the hostname

						ip = input('Enter the hostname : ')

					# Tracking the host by the user specified hostname
					IP(address = ip).gethostbyname()
				elif token["arguments"][0] == 'trackhostbyname':
					# If the argument entered by the user asks for tracking the host by name, then we continue

					# Getting the hostname input
					ip = ''
					if len(token["arguments"]) >= 2:
						# If there are equal or more than 2 arguments entered by the user, then we assume the second argument as the user entered hostname to track

						ip = token["arguments"][1]
					else:
						# If there are less than 2 arguments entered by the user, then we manually ask the user for the hostname

						ip = input('Enter the hostname : ')

					# Tracking the host by the user specified hostname
					IP(address = ip).trackhostbyname()
				elif token["arguments"][0] == 'portscanhostbyname':
					# If the argument entered by the user asks for port scanning the host by name, then we continue

					# Getting the hostname input
					ip = ''
					if len(token["arguments"]) >= 2:
						# If there are equal or more than 2 arguments entered by the user, then we assume the second argument as the user entered hostname to port scan for

						ip = token["arguments"][1]
					else:
						# If there are less than 2 arguments entered by the user, then we manually ask the user for the hostname

						ip = input('Enter the hostname : ')

					if len(token["arguments"]) >= 4:
						# If there are equal or more than 4 arguments entered by the user, then we assume the third argument as the start port and the fourth argument as the end port to scan for

						# Setting the port number range from the arguments
						number1 = token["arguments"][2]
						number2 = token["arguments"][3]
						
						# Starting a port scan attack on the user specified host
						IP(address = ip).portscanhostbyname(initial = number1, final = number2)
					else:
						# If there are less than 4 arguments entered by the user, then we start from 1 to 65500 port number for the scanning

						# Starting a port scan attack on the user specified IP address (with default port number range)
						IP(address = ip).portscanhostbyname()
				elif token["arguments"][0] == 'all':
					# If the argument entered by the user asks for executing all the IP address related tasks (fetching information, port scanning etc), then we continue

					# Getting the IP address input
					ip = ''
					if len(token["arguments"]) >= 2:
						# If there are equal or more than 2 arguments entered by the user, then we assume the second argument as the user entered IP address

						ip = token["arguments"][1]
					else:
						# If there are less than 2 arguments entered by the user, then we manually ask the user for the IP address

						ip = input('Enter the IP address : ')

					# Fetching the information for the user specified host
					print(f'\n[ Fetching the information of {ip} ]')
					IP(address = ip).track()

					# Starting a port scan on the user specified host
					print(f'\n[ Starting port scan on {ip} ]')
					if len(token["arguments"]) >= 4:
						# If there are equal or more than 4 arguments entered by the user, then we assume the third argument as the start port and the fourth argument as the end port to scan for

						# Setting the port number range from the arguments
						number1 = token["arguments"][2]
						number2 = token["arguments"][3]
						
						# Starting a port scan attack on the user specified IP address
						IP(address = ip).portscan(initial = number1, final = number2)
					else:
						# If there are less than 4 arguments entered by the user, then we start from 1 to 65500 port number for the scanning

						# Starting a port scan attack on the user specified IP address (with default port number range)
						IP(address = ip).portscan()
				elif token["arguments"][0] == 'allbyname':
					# If the argument entered by the user asks for executing all the IP address related tasks (fetching information, port scanning etc) + using the user entered hostname (not IP address), then we continue

					# Getting the hostname input
					ip = ''
					if len(token["arguments"]) >= 2:
						# If there are equal or more than 2 arguments entered by the user, then we assume the second argument as the user entered hostname

						ip = token["arguments"][1]
					else:
						# If there are less than 2 arguments entered by the user, then we manually ask the user for the hostname

						ip = input('Enter the IP address : ')

					# Fetching the information for the user specified host
					print(f'\n[ Fetching the information of {ip} ]')
					IP(address = ip).trackhostbyname()

					# Starting a port scan on the user specified host
					print(f'\n[ Starting port scan on {ip} ]')
					if len(token["arguments"]) >= 4:
						# If there are equal or more than 4 arguments entered by the user, then we assume the third argument as the start port and the fourth argument as the end port to scan for

						# Setting the port number range from the arguments
						number1 = token["arguments"][2]
						number2 = token["arguments"][3]
						
						# Starting a port scan attack on the user specified IP address
						IP(address = ip).portscanhostbyname(initial = number1, final = number2)
					else:
						# If there are less than 4 arguments entered by the user, then we start from 1 to 65500 port number for the scanning

						# Starting a port scan attack on the user specified IP address (with default port number range)
						IP(address = ip).portscanhostbyname()
				elif token["arguments"][0] == '--help' or token["arguments"][0] == '-h':
					# If the argument entered by the user is for displaying the help related information for the ip command, then we continue

					self.help(command = 'ip')
				else:
					# If the argument entered by the user is not recognized, then we display the error message on the console screen

					print(f'[ Error : Unrecognized argument "{token["arguments"][0]}" for the command ip. Use ip --help command for more information. ]')
		# ----

		# HTTP RELATED COMMANDS
		# ----
		elif token["command"] == 'http':
			# If the user entered command is http/https related tasks, then we continue

			# Checking for the arguments if exists
			if len(token["arguments"]) == 0:
				# If there are no arguments entered by the user

				print('[ http : requires arguments, use http --help for more info ]')
			else:
				# If there are atleast more than 0 arguments entered by the user

				if token["arguments"][0] == 'startserver':
					# If the argument entered by the user is for starting a simple HTTP server, then we continue to launch the server with the user provided configs

					# Passing all the arguments and launching the HttpServer
					HttpServer(arguments = token["arguments"])
				elif token["arguments"][0] == 'get':
					# If the argument entered by the user is for executing a HTTP GET request, then we continue to execute it with the user provided configs

					# Passing all the parsed arguments and executing the HttpRequest
					request = HttpRequest(arguments = token["arguments"])
					request = request.get()
					if request.status == 200:
						# If the HTTP request return code states no failure (200), then we continue

						print('Output :\n', request.text)
						filelocation = input('\nEnter the file location to save the response (blank for skipping) : ')
						if len(filelocation) == 0:
							# If the user left the file location input blank, then we skip the process

							return 0
						else:
							# If the user entered some input for the file location to save the response of the GET request, then we continue to save it

							open(filelocation, 'w+').write(request.text)
							print(f'[ Response of the HTTP GET request is saved at {filelocation} ]')

						# Deleting some of the variables declared in this scope
						del filelocation, request
						return 0
					else:
						# If the HTTP request retrun code states failure (not 200), then we display the error message on the console screen

						print(f'[ Error : Failed to pull out the HTTP GET request. Response code - {request.status} ]')
						del request
						return 0
				elif token["arguments"][0] == 'post':
					# If the argument entered by the user is for executing a HTTP POST request, then we continue to execute it with the user provided configs

					# Passing all the parsed arguments and executing the HttpRequest
					request = HttpRequest(arguments = token["arguments"])
					request = request.post()
					if request.status == 200:
						# If the HTTP request return code states no failure (200), then we continue

						print('Output :\n', request.text)
						filelocation = input('\nEnter the file location to save the response (blank for skipping) : ')
						if len(filelocation) == 0:
							# If the user left the file location input blank, then we skip the process

							return 0
						else:
							# If the user entered some input for the file location to save the response of the GET request, then we continue to save it

							open(filelocation, 'w+').write(request.text)
							print(f'[ Response of the HTTP POST request is saved at {filelocation} ]')

						# Deleting some of the variables declared in this scope
						del filelocation, request
						return 0
					else:
						# If the HTTP request retrun code states failure (not 200), then we display the error message on the console screen

						print(f'[ Error : Failed to pull out the HTTP POST request. Response code - {request.status} ]')
						del request
						return 0
				else:
					# If the argument entered by the user is not recognized, then we display the error message on the console screen

					print(f'[ Error : Unrecognized argument "{token["arguments"][0]}" for the command http. Use http --help command for more information. ]')
		# ----

		# CONNECTIONS RELATED COMMANDS
		# ----
		elif token["command"] == 'connections':
			# If the user entered command is connections related tasks, then we continue

			# Checking for the arguments if exists
			if len(token["arguments"]) == 0:
				# If there are no arguments entered by the user

				print('[ connections : requires arguments, use connections --help for more info ]')
			else:
				# If there are atleast more than 0 arguments entered by the user

				if token["arguments"][0] == 'list':
					# If the argument entered by the user is to list all the active / available connections on a network, then we continue

					# Passing the arguments to the Connections object with task specified to 'list'
					Connections(arguments = token["arguments"], task = 'list')
				elif token["arguments"][0] == 'check-ssh':
					# If the argument entered by the user is to check for availability of SSH connections on the network, then we continue

					# Passing the arguments to the Connections object with task specified to 'check-ssh'
					Connections(arguments = token["arguments"], task = 'check-ssh')
				elif token["arguments"][0] == '--help':
					# If the argument entered by the user is to display the help / documentation of the connections command / tool, then we continue

					# Passing the arguments to the Connections object with help argument specified
					Connections(arguments = token["arguments"])
				else:
					# If the argument entered by the user is not recognized, then we display the error message on the console screen

					print(f'[ Error : Unrecognized argument "{token["arguments"][0]}" for the command connections. Use connections --help command for more information. ]')
		# ----

		# MAIL RELATED COMMANDS
		# ----
		elif token["command"] == 'mail':
			# If the user entered command is mail related tasks, then we continue

			# Checking for the arguments if exists
			if len(token["arguments"]) == 0:
				# If there are no arguments entered by the user

				print('[ mail : requires arguments, use mail --help for more info ]')
			else:
				# If there are atleast more than 0 arguments entered by the user

				if token["arguments"][0] == 'custom':
					# If the argument entered by the user is to send an email from custom SMTP server, then we continue

					# Launching the Mail.custommail() function with passing all the parsed argument tokens into it
					Mail.custommail(arguments = token["arguments"])
				elif token["arguments"][0] == 'encrypted':
					# If the argument entered by the user is to send an encrypted email, then we continue

					# Launching the Mail.encryptedmail() function with passing all the parsed argument tokens into it
					Mail.encryptedmail(arguments = token["arguments"])
				elif token["arguments"][0][0:2] == '--':
					# If the argument entered by the user is not a task, then we continue to send a basic email

					# Launching the Mail() object with passing all the parsed argument tokens into it
					Mail(arguments = token["arguments"])
		# ----

		# ARITHMETIC COMMANDS
		# ----
		elif token["command"] == 'add':
			# If the user entered command is to add, then we continue

			# Checking for the numeric arguments if exists
			if len(token["arguments"]) == 0:
				# If there are no arguments entered by the user

				print('[ add : requires arguments, use add --help for more info ]')
			else:
				# If there are atleast more than 0 arguments entered by the user

				isNumber = False
				for i in token["arguments"]:
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

						self.help(command = token["command"])
					else:
						choice = input('Creating a new file - Enter N to cancel : ')
						if choice.lower() == 'no' or choice.lower() == 'n':
							return 0
						else:
							open(f'data/{filename}', 'w+').write('')
							print(f'[ File created : {filename} ]')
		elif token["command"] == 'subtract':
			# If the user entered command is to subtract (arithmetic operation), then we continue

			# Asking the user to enter the numbers
			number1 = float(input('Enter the first number : '))
			number2 = float(input('Enter the second number : '))

			# Displaying the result on the console screen
			print(number1 - number2)
		elif token["command"] == 'multiply':
			# If the user entered command is to multiply (arithmetic operation), then we continue

			# Checking for the numeric arguments if exists
			if len(token["arguments"]) == 0:
				# If there are no arguments entered by the user, then we pass

				pass
			else:
				# If there are atleast more than 0 arguments entered by the user

				isNumber = False
				for i in token["arguments"]:
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

					result = 1
					for number in token["arguments"]:
						result *= float(number)
					print(result)
					return 0

			# If the arguments are not mentioned or the arguments aint numeric, then we continue to ask the user for the manual input
			number1 = float(input('Enter the first number : '))
			number2 = float(input('Enter the second number : '))
			print(number1 * number2)
		elif token["command"] == 'divide':
			# If the user entered command is to divide (arithmetic operation), then we continue

			# Asking the user to enter the numbers (2 currently)
			number1 = float(input('Enter the first number : '))
			number2 = float(input('Enter the second number : '))

			# Checking for 0 division error
			if number2 == 0:
				# If the second number entered by the user is 0, then we print the error

				print('[ Error : Cannot divide by 0. The second number entered is 0. ]')
			else:
				# If the second number entered by the user is not 0, then we continue to print the result

				print(number1 / number2)
		elif token["command"] == 'power':
			# If the user entered command is to calculate the power (arithmetic operation), then we continue

			# Checking for the user entered arguments
			if len(token["arguments"]) == 0:
				# If the user did not entered any arguments, then we continue to manually ask for the numbers (currently, we pass)

				pass
			else:
				# If the user did entered some arguments, then we continue

				# Checking wheter the arguments are numeric or not
				try:
					token["arguments"][0] = float(token["arguments"][0])
					token["arguments"][1] = float(token["arguments"][1])
				except ValueError:
					# If there occur any error in the conversion of the numbers, means the user entered arguments are not numeric, thus we break to the manual asking for numbers

					pass
				except Exception as e:
					# If there are any other errors encountered during the process, then we display the error on the console screen

					print(f'[ Error : Failed to parse the arguments for the command "{token["command"]}" ]')
					return 0
				else:
					# If there are no errors encountered during the process (i.e., the user entered arguments are numeric), then we continue to print the result

					print(token["arguments"][0] ** token["arguments"][1])
					return 0

			# Asking the user to enter the numbers manually
			number1 = float(input('Enter the base number : '))
			number1 = float(input('Enter the power number : '))
			print(number1 ** number2)
		elif token["command"] == 'square-root':
			# If the user entered argument is to calculate the square root (arithmetic operation), then we continue

			# Checking for user entered arguments
			if len(token["arguments"]) == 0:
				# If the user did not entered any arguments, then we continue to manually ask for the numbers (currently, we pass)

				pass
			else:
				# If the user did entered some arguments, then we continue

				# Checking wheter the user entered arguments are numeric or not
				try:
					token["arguments"][0] = float(token["arguments"][0])
				except ValueError:
					# If there occur any error in the conversion of the numbers, means the user entered arguments are not numeric, thus we break to the manual asking for numbers

					pass
				except Exception as e:
					# If there are any other errors encountered during the process, then we display the error on the console screen

					print(f'[ Error : Failed to parse the arguments for the command "{token["command"]}" ]')
					return 0
				else:
					# If there are no errors encountered during the process (i.e., the user entered arguments are numeric), then we continue to print the result

					print(token["arguments"][0] ** 0.5)
					return 0

			# Asking the number from the user manually (if the arguments are not mentioned properly)
			number1 = float(input('Enter the number :'))
			print(number1 ** 0.5)
		elif token["command"] == 'cube-root':
			# If the user entered argument is to calculate the cube root (arithmetic operation), then we continue

			# Checking for user entered arguments
			if len(token["arguments"]) == 0:
				# If the user did not entered any arguments, then we continue to manually ask for the numbers (currently, we pass)

				pass
			else:
				# If the user did entered some arguments, then we continue

				# Checking wheter the user entered arguments are numeric or not
				try:
					token["arguments"][0] = float(token["arguments"][0])
				except ValueError:
					# If there occur any error in the conversion of the numbers, means the user entered arguments are not numeric, thus we break to the manual asking for numbers

					pass
				except Exception as e:
					# If there are any other errors encountered during the process, then we display the error on the console screen

					print(f'[ Error : Failed to parse the arguments for the command "{token["command"]}" ]')
					return 0
				else:
					# If there are no errors encountered during the process (i.e., the user entered arguments are numeric), then we continue to print the result

					print(token["arguments"][0] ** (1/3))
					return 0

			# Asking the number from the user manually (if the arguments are not mentioned properly)
			number1 = float(input('Enter the number :'))
			print(number1 ** (1/3))
		elif token["command"] == "number-details":
			# If the user entered argument is to print out the number details, then we continue

			# Checking for user entered arguments
			if len(token["arguments"]) == 0:
				# If the user did not entered any arguments, then we continue to manually ask for the numbers (currently, we pass)

				pass
			else:
				# If the user did entered some arguments, then we continue

				if token["arguments"][0].lower() == '--number':
					# If the argument entered by the user is for specifying the number whose details are to be displayed, then we continue to assign it to the number

					number1 = int(token["arguments"][1])
					NumberDetails(number = number1, execute = True)
				else:
					# If the user entered argument is not --number, then we continue to check for other arguments after asking the user to enter the number manually

					try:
						number1 = int(input('Enter the number : '))
					except ValueError:
						# If the user either entered blank value or non-numeric value, then we display the error message on the console screen

						print('[ Error : Only numeric values are valid here ]')
					else:
						# If there are no errors encountered in the process, then we continue

						# Checking for other arguments and labels
						if token["arguments"][0].lower() == '--table':
							# If the user entered argument specifies to display the table of the number

							NumberDetails(number = number1).table()
						elif token["arguments"][0].lower() == '--factors':
							# If the user entered argument specifies to display the factors of the number

							NumberDetails(number = number1).factors()
						elif token["arguments"][0].lower() == '--pattern' or token["arguments"][0].lower() == '--print-pattern':
							# If the user entered argument specifies to display the pattern of the number

							NumberDetails(number = number1).printPattern()
						else:
							# If the argument entered by the user is not recognized, then we display just the number details on the console screen

							NumberDetails(number = number1, execute = True)
		# ----

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

		print(f'[ Error : {e} ]')