"""
networking.py - Python Shell

A module created for supplying the required functions to the shell application. The functions and classes defined in this module ease many tasks at the shell application, in general way they are used in executing the task assigned by the user via the commands. This module contains functions and classes related to directory handling and other such stuff.

Author : Rishav Das (https://github.com/rdofficial/)
Created on : June 1, 2021

Last modified by : Rishav Das (https://github.com/rdofficial/)
Last modified on : June 13, 2021

Changes made in the last modifications :
1. Updated the entire commented docs (__doc__) of the Mail.encryptedmail() method.

Authors contributed to this script (Add your name below if you have contributed) :
1. Rishav Das (github:https://github.com/rdofficial/, email:rdofficial192@gmail.com)
"""

# Importing the required functions and modules
try:
	# Importing the networks and connections related functions and modules
	import socket
	from socketserver import TCPServer
	from http.server import SimpleHTTPRequestHandler
	from urllib import request, parse
	from pexpect import pxssh

	# Importing the mail and mail server related functions and modules
	import smtplib
	from email.mime.multipart import MIMEMultipart
	from email.mime.text import MIMEText

	# Importing the other functions and modules that are required
	from os import chdir, path
	from json import loads
	from sys import stdout
	from base64 import b64encode, b64decode
except Exception as e:
	# If there are any errors during the importing of the modules, then we display the error on the console screen

	input(f'\n[ Error : {e} ]\nPress enter key to continue...')
	exit()

class IP:
	""" The class which serves the features of the IP tools and commands of the shell. The class defines some functions / methods which serves some of the particular tasks as per specified. This class serves the commands relating to the ip, else. The tasks served by this class / tool are listed below :
	1. IP tracking
	2. Port Scanning
	3. Local IP address information fetching
	4. Get the particular IP address from a hostname. """

	def __init__(self, address = None):

		# Assigning the user specified address of the host as a class variable
		self.address = address

	def track(self):
		""" This method / function serves the task of tracking the information of the user specified IP address. The information is fetched using an external API service (http://ipinfo.io/). The user specified IP address is taken out from the class variable self.address. """

		# Sending the HTTP POST request to fetch the information about the IP address
		response = request.urlopen(f'http://ipinfo.io/{self.address}')

		# Checking the response from the server
		if response.status == 200:
			# If the response from the server states clear response, then we continue

			# Decoding and parsing the response from the server
			response = response.read().decode()
			response = loads(response)

			# Priting the fetched information on the console screen in an organised form
			for key, value in response.items():
				# Iterating through each key-value pairs in the response from the server

				print('[#] %-25s	:	%-25s' %(key.upper(), value))
		else:
			# If the response from the server states error in the process, then we raise an error

			raise ValueError('Failed to fetch the information of the specified IP address from the server.')

	def portscan(self, initial = None, final = None):
		""" This method / function serves the task of executing a port scan on the user specified target IP address. The user provided address (hostname) is stored in the class variable self.gethostbyname. The function checks for all the ports ranging from port number 1 to 65535. The function also has some particular range of ports for being specified by the user. """

		# Checking for the user specified ports
		if initial == None or final == None:
			# If the user did not specified the port number ranges properly, then we start scaning ports in the range (default port range)

			initial = 1
			final = 65535
			print('[ Executing the port scanner with default ports (i.e., 1 to 65535) ]')
		else:
			# If the user did specified the port number ranges, then we convert them to the integer form (valid form of a port number)

			try:
				initial = int(initial)
				final = int(final)
			except ValueError:
				# If there are errors encountered in parsing the port number into int format, then we display the error on the console screen

				print(f'[ Error : Unsupported value for port numbers. Numeric values required. ]')
				return 0
		
		# Defining a list which will store the ports which were found open during port scan
		openPorts = []

		# Executing the attack
		for port in range(initial, final + 1):
			# Intiating a connection to the target host with the currently iterated port number
			connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			socket.setdefaulttimeout(1) 

			# Returns an error indicator 
			result = connection.connect_ex((self.address, port)) 
			stdout.write('\r')
			if result == 0:
				# If the port is open

				stdout.write('[!] Port %d : open' %port)
				openPorts.append(port)
			else:
				# If the port is not open (i.e., closed)

				stdout.write('[!] Port %d : closed' %port)
			stdout.flush()

			# Closing the initiated connection
			connection.close()

		# Displaying the filtered and open ports on the console screen
		print('\n\nThe ports which were found open during the port scan are listed below : ')
		if len(openPorts) == 0:
			# If there are no open ports found on the target in the port scan, then we continue to display the no ports found message on the console screen

			print('No ports were found open')
		else:
			# If there are open ports found, then we continue to iterate them on the console screen

			for port in openPorts:
				print(f'[#] {port}')

	def localinfo(self):
		""" This method / function serves the task of fetching the information about the local IP address. The self.address field might not be required to be present for using this particular function. We will directly call this function from the class. """

		# Fetching the public information for our computer machine's IP address
		print('Public information :')
		self.address = ''
		self.track()

		# Fetching the hostname of the local machine
		self.address = socket.gethostname()

		# Displaying the fetched information on the console screen (Also fetching them during the print process)
		print(f'\nLocal information :\n[#] Local hostname : {self.address}\n[#] Local IP address : {socket.gethostbyname(self.address)}')

		# Scanning open ports on the local machine
		ports = []  # The list to store the ports on the local machine which were found open during the port scan
		stdout.write('\r')
		for port in range(1, 65536):
			# Iterating through each port number from 1 to 65535

			# Displaying the port scan information on the console screen
			stdout.write(f'[ Scanning ports : {port} ]')

			# Intiating a connection to the target host with the currently iterated port number
			connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			socket.setdefaulttimeout(1) 

			# Returns an error indicator 
			result = connection.connect_ex((self.address, port)) 
			stdout.write('\r')
			if result == 0:
				# If the port is open, then we append it to the ports list

				openPorts.append(port)
			else:
				# If the port is not open (i.e., closed)

				continue

			# Closing the initiated connection
			connection.close()

		# Checking the result of the port scan
		stdout.write(f'[#] Ports found open : ',)
		stdout.flush()
		if len(ports) == 0:
			# If there are no open ports were found during the port scan

			print(f'None')
		else:
			# If there are atleast one or more ports that were found open during the port scan proces, then we display them on the console screen

			for port in ports:
				print({port}, end = ' ,')

	def gethostbyname(self):
		""" This method / function serves the task of fetching the host IP address using the hostname (address) provided by the user. The user provided address (hostname) is stored in the class variable self.gethostbyname. The result is then displayed on the console screen. This function fetches the IP addresses from hostname like www.google.com, etc. Example usage is given below :

		IP(address = 'www.google.com').gethostbyname() """
 
 		# Fetching the IP address of the hostname provided
		self.address = socket.gethostbyname(self.address)
		print(self.address)

	def trackhostbyname(self):
		""" This method / function serves the task of fetching the information of an IP address using the hostname (address) provided by the user. The user provided address (hostname) is stored in the class variable self.gethostbyname. The result is then displayed on the console screen. This function fetches the IP addresses from hostname like www.google.com, etc. Example usage is given below :

		IP(address = 'www.google.com').trackhostbyname() """

		# Fetching the IP address of the hostname provided
		self.address = socket.gethostbyname(self.address)

		# Tracking the required information about the IP address with the specified hostname (Just calling the track() method defined within this class)
		self.track()

	def portscanhostbyname(self, initial = None, final = None):
		""" This method / function serves the task of executing a port scan on the IP address fetched using the user provided hostname address. The user provided address (hostname) is stored in the class variable self.gethostbyname. The function first fetches the IP address of the target using the specified hostname. The function checks for all the ports ranging from port number 1 to 65535. The function also has some particular range of ports for being specified by the user. """

		# Fetching the IP address of the hostname provided
		self.address = socket.gethostbyname(self.address)

		# Executing the port scan attack (by calling the portscan() method defined withing this class)
		self.portscan(initial = initial, final = final)

	def portscan_beta(self, initial, final):
		""" Beta version for the portscanning feature of this Class / tool (IP). Changes here are : changed way of output on the console screen. """

		# Checking for the user specified ports
		if initial == None or final == None:
			# If the user did not specified the port ranges properly, then we start scaning ports in the range (default port range)

			initial = 1
			final = 65535
			print('[ Executing the port scanner with default ports (i.e., 1 to 65535) ]')
		
		# Defining a list which will store the ports which were found open during port scan
		ports = []

		# Executing the attack
		for port in range(initial, final + 1):
			# Intiating a connection to the target host with the currently iterated port number
			connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			socket.setdefaulttimeout(1) 

			# Returns an error indicator 
			result = connection.connect_ex((self.address, port)) 
			stdout.write('\r')
			if result == 0:
				# If the port is open

				stdout.write('[!] Port %d : open' %port)
				ports.append(port)
			else:
				# If the port is not open (i.e., closed)

				stdout.write('[!] Port %d : closed' %port)

			# Closing the initiated connection
			connection.close()

		# Displaying the filtered and open ports on the console screen
		stdout.write('Ports found open : ')
		stdout.flush()
		if len(ports) == 0:
			# If there are no open ports found on the target in the port scan, then we continue to display the no ports found message on the console screen

			print('None')
		else:
			# If there are open ports found, then we continue to iterate them on the console screen

			for port in ports:
				print(port, end = ', ')

class HttpServer:
	""" The class which serves the features of the HttpServer tool / command of the shell. The class contains certain functions (methods) defined within itself. The simple server can be launched by just calling the class as an object. """

	def __init__(self, arguments = []):
		# Setting the self.port and self.root class variables
		self.port = None
		self.root = None
		self.documentation = False

		# Parsing the argument sent to this class while creating the object
		for index, argument in enumerate(arguments):
			# Iterating through each argument item

			if argument == '--port' or argument == '-p':
				# If the argument is for specifying the port number, then we continue to parse the next argument as the entered value

				try:
					self.port = int(arguments[index + 1])
				except IndexError:
					# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

					continue
				except ValueError:
					# If there are errors in parsing the port number input from the user to integer format, then we display the error on the console screen

					raise ValueError ('Invalid port number specified. Proper numeric value between 1-65535 should be provided.')
			elif argument == '--root' or argument == '-r':
				# If the argument is for specifying the root location, then we continue to parse the next argument as the entered value

				try:
					self.root = arguments[index + 1]
				except IndexError:
					# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

					continue
			elif argument == '--help':
				# If the argument is for displaying the help information, then we mark the documentation mode True

				self.documentation = True
			else:
				# If the currently iterated argument is not recognized, then we skip the current iteration

				continue

		# Checking whether the class object is called for documentation mode (display help) or just running tasks
		if self.documentation:
			# If the class object is called for displaying the documentation, then we continue displaying the help section contents

			print('\nhttp startserver\nUsage : http startserver <arguments>\n\n"http startserver" is a tool which provides the feature to launch a very basic http server. The server hosted at the user speciifed port and root location. The server just hosts the html, js and css files. It does not allows databases or any form\nof backend functionality as it is a simple server. Just display the files in the root location and its sub-directories. Make sure that the index.html file is present in the root directory for proper indexing.\n\nSome arguments used are :\n--port, -p    Used to specify the port number\n--root, -r    Used to specify the root location\n--help        Displays this text\n\nSome points to be noted :\n1. The port number input should be an integer between 1 to 65535.\n2. Some of the port numbers requires superuser permissions in order to work.\n3. The root location input should be an existing and a directory with the user permitted to work on.\n\nSee the docs of this project for more information about this tool (http startserver).')
		else:
			# If the class object is called for executing tasks instead of the documentation mode, then we continue

			# Checking the port number and root location input from the user
			if self.port == None:
				# If the port number is stil not specified by the user, then we ask the port number from the user manually

				self.port = int(input('Enter the port number : '))
			if self.root == None:
				# If the root location is still not specified by the user, then we give use the current directory as the root location and launch the server

				print('[ Launching the server at current directory ]')
			else:
				# If the root location is specified, then we launch the server at the custom provided root location

				if path.isdir(self.root):
					# If the user specified directory does exists, then we continue

					# Moving to the specified directory
					chdir(self.root)
					print(f'[ Launching the server at : {self.root} ]')
				else:
					# If the user specified directory does not exists, then we display the error message on the console screen

					raise SystemError(f'No such directory found "{self.root}"')

			# Saving the initial directory location to a class variable
			self.initialDirectory = path.dirname(path.abspath(__file__))

			# Setting and launching the server
			handler = SimpleHTTPRequestHandler
			with TCPServer(('', self.port), handler) as httpd:
				# Launching the http server

				try:
					print(f'Serving at port : {self.port}')
					httpd.serve_forever()
				except KeyboardInterrupt:
					# If the user pressed CTRL+C key combo, then we stop the server

					chdir(self.initialDirectory)  # Unsetting the current root location to the intial working directory
					httpd.server_close()
				except Exception as e:
					# If there are any errors encountered during the process, then we display the error message on the console screen

					print(f'[ Http Server Error : {e} ]')

class Connections:
	""" The class which serves the feature of the connections command of the shell. There are functions and methods defined under this class which executes the various tasks under the connections commands. The tasks served by this functions are listed below :
	1. Check all the connections available on a user specified deviced (example - 127.0.0, 192.168.43)

	Some notable points for this class and internal defined variables :
	1. Only IPv4 type address are accepted by this tool, and there are two types of addresses taken in by this function. 1st is the IP address in format xxx.xxx.xxx (Here all the combinations of 1-255 numbers are used post in order to check for connections), and 2nd type is xxx.xxx.xxx.xxx (Here only this single specified IP address is checked for connections).
	2. If the port number 0 entered by the user, then the tool scans for all the port numbers ranging from 1 to 65535. Otherwise they check for a particular port numer. This port number is defined by the argument '-p' or '--port'.
	3. Same if the user does not specifies the port number in the arguments, then the tool checks for all the port numbers ranging from 1 to 65535. """

	def __init__(self, arguments = [], task = None):
		# Setting the self.port and self.address class variables
		self.port = None
		self.address = None
		self.documentation = False

		# Parsing the argument sent to this class while creating the object
		for index, argument in enumerate(arguments):
			# Iterating through each argument item

			if argument == '--port' or argument == '-p':
				# If the argument is for specifying the port number, then we continue to parse the next argument as the entered value

				try:
					self.port = int(arguments[index + 1])
				except IndexError:
					# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

					continue
				except ValueError:
					# If there are errors in parsing the port number input from the user to integer format, then we display the error on the console screen

					raise ValueError('Invalid port number specified. Proper numeric value between 1-65535 should be provided.')
			elif argument == '--ip-address' or argument == '-i':
				# If the argument is for specifying the IP address, then we continue to parse the next argument as the entered value

				try:
					self.address = arguments[index + 1]
				except IndexError:
					# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

					continue
			elif argument == '--help':
				# If the argument is for displaying the help information, then we mark the documentation mode True

				self.documentation = True
			else:
				# If the currently iterated argument is not recognized, then we skip the current iteration

				continue

		# Checking whether the class object is called for documentation mode (display help) or just running tasks
		if self.documentation:
			# If the class object is called for displaying the documentation, then we continue displaying the help section contents

			print('connections\nUsage : connections [task] <arguments>\n\n"connections" is a tool which provides the feature of serving various tasks related to networks and connections. Currently servers tasks are listed below with the specific command to invoke them.\n\nconnections list <arguments>    Lists all the active connections in the local address / user provided network address\nconnections check-ssh <arguments>    Checks for availablity of SSH connections on the network\n\nArguments that can be used are :\n--port, -p            Used to specify the port number\n--ip-address, -i     Used to specify the IP address of the device\n--help               Displays this text\n\nUsage :\n[Listing available connections on a network]\n1. For listing available connections in network with IP address format in 192.168.43.xxx, we may scan all the ports of each devices using the command specified below\nconnections list -i 192.168.43\n\n2. For listing available connections in network with IP address format in 192.168.43.xxx + fixed port number, we may scan all the ports of each devices using the command specified below\nconnections list -i 192.168.43 -p 80\n\n3. For listing available connections in a single device (the available ports) (device IP : 192.168.43.1 For example), we use the command specified below\nconnections list -i 192.68.43.1\n\n4. For listing available connections in a single device (the available ports) (device IP : 192.168.43.1 For example + fixed port number), we use the command specified below\nconnections list -i 192.68.43.1 -p 80\n\nSummary : Either you can scan all the devices on the network (192.xxx.xxx.1 to 192.xxx.xxx.255) or any particular device. Either you can scan all the ports ranging 1 to 65535, or just a specific port of the network devices.\n\n[Checking SSH connection availability]\n1. List all the available SSH connections on the network, with IP address format 192.168.43.xxx, use the below command (It checks for port 22 and 8022 for all the devices 1-255).\nconnections check-ssh -i 192.168.43\n\n2. Check for a particular port for SSH connection of all the devices in the network (with IP address of format 192.168.43.xxx), we use the below specified command.\nconnections check-ssh -i 192.168.43 -p 8022\n\n3. Check for a particular device on the network for SSH connection (For example, IP : 192.168.43.1 with all the ports), we use the below specified command.\nconnections check-ssh -i 192.168.43.1\n\n4. Check for a particular device on the network for SSH connection with a particular port number specified (For example, IP : 192.168.43.1, port : 22), we use the below specified command :\nconnections check-ssh -i 192.168.43.1 -p 22\n\nSummary : Either you can scan all the devices on the network (192.xxx.xxx.1 to 192.xxx.xxx.255) or any particular device. Either you can scan all the ports ranging 1 to 65535, or just a specific port of the network devices.\n\nSee the docs of this project for more information about this tool (connections).')
		else:
			# If the class object is called for executing tasks instead of the documentation mode, then we continue

			# Checking the address type
			if self.address == None:
				# If there are no addresses provided by the user, then we continue with the default address (127.0.0.x / local machine address)

				self.address = '127.0.0.'
				self.addressType = 'half'
			else:
				# If the user provided some of a IP address to the class object, then we continue with the validation of the user entered IP address

				address = self.address
				if address[len(address) - 1] == '.':
					# If the user entered IP address does have its last term as '.'

					address = address.split('.')
					address.pop()
				else:
					# If the user entered IP address does not have its last term as '.'

					address = address.split('.')

				# Checking the lengths of sections of the IP address provided
				if len(address) == 3:
					# If the user entered IP address have 3 sections for the numbers, then we continue

					self.addressType = 'half'
					if self.address[len(self.address) - 1] != '.':
						# Appending a period in the end of the IP address if there aint any (for half addresses)

						self.address += '.'
				elif len(address) == 4:
					# If the user entered IP address have 4 sections for the numbers, then we continue

					self.addressType = 'full'
				else:
					# If the user entered IP address have neither 3 nor 4 sections, then we display the error message on the console screen

					raise SyntaxError('Please provide a proper IPv4 address for scanning. Use the --help argument for more information.')
				del address

			# Validating the port number specified
			if self.port == None or self.port == 0:
				# If the port number is not specified by the user in the arguments, then we mark the port number as 0 (for 1-65535 ports scanning)

				self.port = 0
			else:
				# If the port number is specified by the user in the arguments, then we check the range for it

				if 1 <= self.port or self.port >= 65535:
					# If the port number specified by the user is in valid range, then we continue

					pass
				else:
					# If the port number specified by the user is not in valid range, then we display the error on the console screen

					raise ValueError('Invalid port number specified. Proper numeric value between 1-65535 should be provided.')

			# Checking the task assigned to this objext
			if task == None:
				# If the task is not assigned by the user, then we just pass

				pass
			elif task == 'list':
				# If the task assigned by the user is to list active and available connections, then we continue

				self.listAvailableConnections()
			elif task == 'check-ssh':
				# If the task assigned by the user is to check for ssh connections, then we continue

				self.checkSSH()
			else:
				# If the task assigned by the user is not recognized, then we we display the error on the console screen

				print(f'[ Error : Task specified to the Connections tool is not recognized. ]')

	def listAvailableConnections(self):
		""" The method / function which checks for the connections at the user specified IP addresses, then lists them in order. This function checks for the IP address stored in the class variable self.address, and the port number stored in the class variable self.port.

		The method scans for the connections in the specified ports of the specified IP address. The IP addresses should be of IPv4 format + there are two forms of the IP addresses accepted here (as explained in the class __doc__). Just for inforamtion :
		1. For 3 groups of numbers in the IP address (half) : This function scans for all combination of the last section with 1-255. Example - For input as 192.168.43., the function checks for IPs 192.168.43.1, 192.168.43.2, 192.168.43.3, etc.
		2. For 4 groups of numbers in the IP address (full) : This function scans for the input as provided. Example - For input as 192.168.43.1, this function scans for 192.68.43.1 only. """

		# Checking for the IP address type
		if self.addressType == 'half':
			# If the IP address entered by the user is half type address, then we continue

			for i in range(1, 256):
				# Checking for all the devices on the network

				# Checking the port number input
				if self.port == 0:
					# If the port number is 0, then we check for all the ports ranging from 1 to 65535

					for port in range(1, 65536):
						# Iterating through each port number

						# Establishing a connection to the currently iterated device (with the IP address) with the specified port number
						connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						socket.setdefaulttimeout(1)
						result = connection.connect_ex((f'{self.address}{i}', port))
						stdout.write('\r')
						stdout.write('[!] Checking connection at %-20s' %(f'{self.address}{i}:{port}'))
						if result == 0:
							# If the connection is made successfully (i.e., port is open for this device), then we display it

							print(f'\r[#] {self.address}{i} | Port {port} -> available [{self.address}{i}:{port}]')
						stdout.flush()
				else:
					# If the port number is something more specific, then we check for connection to that specific port number

					# Establishing a connection to the currently iterated device (with the IP address) with the specified port number
					connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					socket.setdefaulttimeout(1)
					result = connection.connect_ex((f'{self.address}{i}', self.port))
					stdout.write('\r')
					stdout.write('[!] Checking connection at %-20s' %(f'{self.address}:{self.port}'))
					if result == 0:
						# If the connection is made successfully (i.e., port is open for this device), then we display it

						print(f'\r[#] {self.address}{i} | Port {self.port} -> available [{self.address}{i}:{self.port}]')
					stdout.flush()
			print('\r[================== Scan completed ==================]')
		elif self.addressType == 'full':
			# If the IP address entered by the user is full type address, then we continue

			# Checking the port number input
			if self.port == 0:
				# If the port number is 0, then we check for all the ports ranging from 1 to 65535

				for port in range(1, 65536):
					# Iterating through each port number

					# Establishing a connection to the device (with the IP address) with the currently iterated port number
					connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					socket.setdefaulttimeout(1)
					result = connection.connect_ex((self.address, port))
					stdout.write('\r')
					stdout.write('[!] Checking connection at %-20s' %(f'{self.address}:{port}'))
					if result == 0:
						# If the connection is made successfully (i.e., port is open for this device), then we display it

						print(f'\r[#] {self.address} | Port {port} -> available [{self.address}:{port}]')
					stdout.flush()
			else:
				# If the port number is something more specific, then we check for connection to that specific port number

				# Establishing a connection to the device (with the IP address) with the specified port number
				connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				socket.setdefaulttimeout(1)
				result = connection.connect_ex((self.address, self.port))
				stdout.write('\r')
				stdout.write('[!] Checking connection at %-20s' %(f'{self.address}:{self.port}'))
				if result == 0:
					# If the connection is made successfully (i.e., port is open for this device), then we display it

					print(f'\r[#] {self.address} | Port {self.port} -> available [{self.address}:{self.port}]')
				stdout.flush()
			print('\r[================== Scan completed ==================]')
		else:
			# If the IP address entered by the user is not recognized by any of the types, then we display the error message on the console screen

			print(f'[ Error : Improper IP address provided or failed to render the input from the user. ]')
			return 0

	def checkSSH(self):
		""" This method / function checks whether the SSH connections are available for the user entered IP address. This function checks for the IP address stored in the class variable self.address, also uses the same algorithms for half and full addresses as per provided. We will check for the port numbers [22, 8022]. """

		# Checking for the IP address type
		if self.addressType == 'half':
			# If the IP address entered by the user is half type address, then we continue

			# Checking for the connectivity to the devices in the network via the particular HTTP ports (which are used for SSH)
			for i in range(1, 256):
				# Iterating through each number ranging from 1 to 255 in order to check for all available devices

				for port in [22, 8022]:
					# Iterating through each port number in the list

					connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					socket.setdefaulttimeout(1)
					result = connection.connect_ex((f'{self.address}{i}', port))
					stdout.write('\r')
					stdout.write('[!] Checking SSH connection at %-20s' %(f'{self.address}{i}:{port}'))
					if result == 0:
						# If the connection is made successfully (i.e., port is open for this device), then we display it

						print(f'\r[#] [{self.address}{i}:{port}] --> Available for connections')
					stdout.flush()
			print('\r[================== Scan completed ==================]')
		elif self.addressType == 'full':
			# If the IP address entered by the user is a full type address, then we continue

			# Checking for the connectivity to the specified device on the network via the particular HTTP ports (which are used for SSH)
			for port in [22, 8022]:
				# Iterating through each port number in the list

				connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				socket.setdefaulttimeout(1)
				result = connection.connect_ex((self.address, port))
				stdout.write('\r')
				stdout.write('[!] Checking SSH connection at %-20s' %(f'{self.address}:{port}'))
				if result == 0:
					# If the connection is made successfully (i.e., port is open for this device), then we display it

					print(f'\r[#] [{self.address}:{port}] --> Available for connections')
				stdout.flush()
			print('\r[================== Scan completed ==================]')
		else:
			# If the IP address entered by the user is not recognized by any of the types, then we display the error message on the console screen

			print(f'[ Error : Improper IP address provided or failed to render the input from the user. ]')
			return 0

class SSH:
	""" The class which defines the functionality of the SSH commands of the shell. 


	TO BE UPDATED. CURRENTLY NOT WORKING. WILL BE UPDATED LATER, REMEMBER THIS ONE!!!
	"""

	def __init__(self, arguments = [], task = None):
		# Setting the class variables (properties) to their respective default values
		self.port = 22
		self.username = None
		self.password = None
		self.address = None

		# Parsing the argument sent to this class while creating the object
		for index, argument in enumerate(arguments):
			# Iterating through each argument item

			if argument == '--port' or argument == '-p':
				# If the argument is for specifying the port number, then we continue to parse the next argument as the entered value

				try:
					self.port = int(arguments[index + 1])
				except IndexError:
					# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

					continue
				except ValueError:
					# If there are errors in parsing the port number input from the user to integer format, then we display the error on the console screen

					raise ValueError('[ Error : Invalid port number specified. Proper numeric value between 1-65535 should be provided. ]')
			elif argument == '--address' or argument == '-i' or argument == '--hostname' or argument == '-h':
				# If the argument is for specifying the IP address, then we continue to parse the next argument as the entered value

				try:
					self.address = arguments[index + 1]
				except IndexError:
					# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

					continue
			elif argument == '--username' or argument == '-u':
				# If the argument is for specifying the username for the SSH login, then we continue to parse the next argument as the entered value

				try:
					self.username = arguments[index + 1]
				except IndexError:
					# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

					continue
			elif argument == '--password' or argument == '-k':
				# If the argument is for specifying the password for the SSH login, then we continue to parse the next argument as the entered value

				try:
					self.password = arguments[index +  1]
				except IndexError:
					# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

					continue
			else:
				# If the currently iterated argument is not recognized, then we skip the current iteration

				continue

		# Checking for the task
		if task == None:
			# If the task is not specified, then we just connect to the required server and return the status

			try:
				ssh = pxssh.pxssh()
				ssh.login(self.address, self.username, self.password)
				ssh.sendline('uptime')
				ssh.prompt()
				print(ssh.before)
				ssh.logout()
			except pxssh.ExceptionPxssh as e:
				# If there are any errors during the process, then we display the error message on the console screen

				print(f'[ Error : {e} ]')
		else:
			# If the task specified by the user is not recognized by the user, then we display the error on the console screen

			print(f'[ Error : Task specified to the SSH tool is not recognized. ]')

	def sendFiles(self):
		pass

	def recieveFiles(self):
		pass

class HttpRequest:
	""" This class serves the functionality of the 'http requests' command of the shell. This class executes HTTP requests on the user specified URLs as well as also includes the HTTP data as per the user specifies. The class is currently not developed enough for file uploads, but can execute normal data sending during HTTP requests.

	The class object work in two ways :
	1. With arguments specifed

		When the arguments are directly specified, then the class parses the arguments list in order to filter out the class variables and make proper data for executing the HTTP requests.
		These arguments are generally parsed arguments from the shell commands (i.e., when the user enters any command on the shell, then the shell backend parses the arguments into seperate tokens).

		The arguments that the class object will parse are :
		--url, -u    Used to specify the URL for the HTTP request
		--data, -d   Used to specify the data for the HTTP request
		--help       Used to display the help text for the command (Only displays the help version for the command version of the tool, not for the entire class object)

		When specifying the data via arguments (i.e., specifying the data in the shell commands for the HTTP requests), then note the following points :
		* The data will be parsed in JSON format. So, directly type in the data for the request in a dictionary.
		* The whitespaces will separate two arguments during the token parsing,
		thus use the whitespace escape sequence in order to indicate an whitespace ('\ ' is an whitespace escape sequence).

	2. With parameters directly specified

		The syntax for calling out an HTTP request passing parameters directly to the class object :
		request = HttpRequest(url = <str>, method = <str>, data = <dict>)
		
		When the paramters for the HTTP requests are specified directly, then we have to note the following points :
		* The URL is to be specified in string format.
		* The method paramter specifies the type of HTTP request to be executed. Either method = 'get' or method = 'post'.
		* The data parameter specifies the HTTP data for the request. It can either be in direct python object (dictionary) format or in a JSON (str) format. """

	def __init__(self, url = None, method = None, data = None, arguments = None):
		# Setting the class variables
		if arguments == None:
			# If the arguments are not specified, then we set the class variables for the url and data

			self.url = url
			self.data = data
		else:
			# If the arguments are specified, then we continue to parse them

			# Parsing the argument sent to this class while creating the object
			self.url = None
			self.data = None
			for index, argument in enumerate(arguments):
				# Iterating through each argument item

				if argument == '--url' or argument == '-u':
					# If the argument is for specifying the port number, then we continue to parse the next argument as the entered value

					try:
						self.url = arguments[index + 1]
					except IndexError:
						# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

						continue
				elif argument == '--data' or argument == '-d':
					# If the argument is for specifying the root location, then we continue to parse the next argument as the entered value

					try:
						self.data = arguments[index + 1]
					except IndexError:
						# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

						continue
				elif argument == '--help':
					# If the argument is for displaying the help information, then we mark the method as 'help'

					method = 'help'
				else:
					# If the currently iterated argument is not recognized, then we skip the current iteration

					continue

		# Parsing the data items as per specified by the user
		if type(self.data) == dict and self.data != None:
			# If the data is a dictionary object, then we pass

			pass
		elif type(self.data) == str and self.data != None:
			# If the data is a string object, then we proceed forward to parse in JSON format

			try:
				self.data = loads(self.data)
			except Exception as e:
				# If there are any errors encountered during the process, then we proceed forward to check for custom parsing of the data string

				try:
					data = self.data.split(';')
					self.data = {}
					for item in data:
						# Iterating over each data items (key:value pairs)

						item = item.split(':')
						self.data[item[0]] = item[1]
				except Exception as e:
					# If there are any errors encountered during the process, then we raise an error with a custom message

					raise SyntaxError('Provided data failed to parse. Supported formats : JSON, default. Check out docs for more information')

		# Checking the method of the request as per entered by the user
		if method == None:
			# If the method is not specified (default value), then we pass

			pass
		elif method.lower() == 'get':
			# If the method is specified to be a GET request by the user, then we continue

			self.get()
		elif method.lower() == 'post':
			# If the method is specified to be a POST request by the user, then we continue

			self.post()
		elif method.lower() == 'help':
			# If the method is specified for displaying the help text, then we continue

			print('http request\nUsage : http request [task] <arguments>\n\n\'http request\' is a tool which provides the feature of serving HTTP requests around the web. We can use this tool to do GET and POST requests.\n\nTasks that can be assigned are :\nhttp request get <arguments>     To execute a HTTP GET request\nhttp request post <arguments>    To execute a HTTP POST request\n\nArguments that can be used are :\n--url, -u            Used to specify the URL of the server\n--data, -d           Used to specify the HTTP data to be sent along the request\n--help               Displays this text\n\nRead the below steps for proper usage :\n1. Example for executing HTTP GET request,\nhttp request get --url https://www.google.com\n\n2. Example for executing HTTP GET request with data (Use whitespace in the data to swap out whitespaces and avoid an error)\nhttp request get --url https://www.google.com --data {"q":"Search\\ query"}\n\n3. Example for executing HTTP POST request\nhttp request post --url https://website.com --data {"username":"risahvdas",\\ "password":"easy\\ password"}\n\nFor more detailed information, check out the docs.')
		else:
			# If the method specified is not recognized, then we raise an error with custom message

			raise SyntaxError(f'method = {method} not recognized')

	def get(self):
		""" This method / function serves the functionality of executing a HTTP GET request using the user specified URL and data parameters. This function uses the values of the URL and data from the class variables self.url and self.data. This function uses the 'request' function from the urllib module which is by default available in the standard python3 library. """

		# Sending the HTTP GET request (Also with custom validation of the data)
		if self.url != None:
			# If the URL is not left default, then we continue

			if self.data != None:
				# If the data is not defined for this GET request, then we continue without specifying the data

				# Sending the GET request
				response = request.urlopen(self.url)
			else:
				# If the data is defined, then we continue with custom data (Parsing and encoding them too)

				if self.url[len(self.url)-1:] != '?':
					self.url += '?'
				self.data = parse.urlencode(self.data)
				response = request.urlopen(f'{self.url}{self.data}')
				del self.data
		else:
			# If the URL is left default (not specified by the user), then we raise an error

			raise ValueError('No proper URL specified for HTTP GET request')
			return 0

		# Checking the HTTP GET request response status code
		if response.status == 200:
			# If the request response HTTP code is 200, then we continue

			self.status = response.status

			# Setting the response message to a class variable
			self.text = response.read().decode()
			return 0
		else:
			# If the request response HTTP code is anything else than 200, then we return the value

			self.status = response.status
			return 0

	def post(self):
		""" This method / function serves the functionality of executing a HTTP POST request using the user specified URL and data parameters. This function uses the values of the URL and data from the class variables self.url and self.data. This function uses the 'request' function from the urllib module which is by default available in the standard python3 library. """

		# Sending the HTTP POST request
		self.data = parse.urlencode(self.data).encode()
		req = request.Request(self.url, data = self.data)
		response = request.urlopen(req)
		del req, self.data
		if response.status == 200:
			# If the request response HTTP code is 200, then we continue

			self.status = response.status

			# Setting the response message to a class variable
			self.text = response.read().decode()
			return 0
		else:
			# If the request response HTTP code is anything else than 200, then we return the value

			self.status = response.status
			return 0

class Mail:
	""" This class serves the functionality of the mail command of the shell. This class is defined with some methods and functins that make the proper sending of emails via the web. The class requires the smtplib library in order to work properly. The class can send emails using the following web services : gmail (google), yahoo.

	Currently, only the simple text based emails can be sent. The functions of email sending with file attachement and mutlimedia support is still in developement. 

	This class object takes two types of inputs in order to send emails :
	1. Arguments parsing

		In this mode, the arguments parsed at the shell after the user enters a command are passed to this class object. The syntax is below
		Mail(arguments = <parsed arguments list>)
		
		The arguments that are recongized by this class object are listed below
		--sender        Used to specify the sender's username
		--password      Used to specify the sender's password
		--receiver      Used to specify the receiver's email address (target email address)
		--subject       Used to specify the subject of the mail
		--body          Used to specify the file location which contains the contents of the body of the mail
		--service       Used to specify the web service used by the sender (Google, Yahoo)

		As we all know that the argument token are parsed on the basis of whitespaces, therefore if the any of the input argument requires whitespaces between them. Then, we will use the whitespace character escape sequence in order to use the whitespace values in our parameters. Example of such is shown below.
		mail --sender <username> --password <password> --receiver <target-email-address> --subject Subject\ with\ whitespace --body <content file> --service google

	2. Parameters passed directly

		In this mode, the values are directly passed as parameters to the class object. The rules are same, except the fact that the whitespace escape sequence is not used here. As the values are passed directly as strings.
		Below is an example syntax.

		Mail(
			sender = <username>,
			password = <password>,
			receiver = <receiver email adddress>,
			subject = <subject of the mail>,
			body = <body contents of the mail>,
			webservice = <web service used by sender>,
		)

		Note that the body parameter here takes the body contents directly instead of taking a file location as an input, from which the contents of the body is to be read.

	Currently supported web services (email services) are :
	1. Google (gmail)
	2. Yahoo Mail
			"""

	def __init__(self, sender = None, password = None, receiver = None, subject = None, body = None, webservice = None, arguments = None):
		# Checking if arguments provided or just the parameters directly
		if arguments == None:
			# If the arguments are not passed to this class object by the user, then we continue to use the default provided values

			# Setting the user provided parameters as the class variables
			self.sender = sender
			self.password = password
			self.receiver = receiver
			self.subject = subject
			self.body = body
			self.webservice = webservice
		else:
			# If the arguments are passed to this class object by the user, then we continue to parse the arguments

			# Parsing the arguments entered to this class object
			# ----
			# Setting the default value of the class variables to None
			self.sender = None
			self.password = None
			self.receiver = None
			self.subject = None
			self.body = None
			self.webservice = None
			self.documentation = False 	# Setting the documentation mode to False by default

			# Iterating through each argument to filter out the values
			for index, argument in enumerate(arguments):
				# Iterating through each argument item

				if argument == '--sender':
					# If the argument is for specifying the sender's username, then we continue to parse the next argument as the entered value

					try:
						self.sender = arguments[index + 1]
					except IndexError:
						# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

						continue
				elif argument == '--password':
					# If the argument is for specifying the user's password, then we continue to parse the next argument as the entered value

					try:
						self.password = arguments[index + 1]
					except IndexError:
						# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

						continue
				elif argument == '--receiver':
					# If the argument is for specifying the receiver's email address, then we continue to parse the next argument as the entered value

					try:
						self.receiver = arguments[index + 1]
					except IndexError:
						# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

						continue
				elif argument == '--subject':
					# If the argument is for specifying the subject of the mail, then we continue to parse the next argument as the entered value

					try:
						self.subject = arguments[index + 1]
					except IndexError:
						# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

						continue
				elif argument == '--body':
					# If the argument is for specifying the body of the mail, then we continue to parse the next argument as the entered value (The value would be of a text file which will contain the entire contents of the body of the mail)

					try:
						# Reading the data of the file location specified
						data = open(arguments[index + 1], 'r').read()
					except IndexError:
						# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

						continue
					else:
						# If there are not errors encountered during the process, then we set the contents of the specified file as the body of the email

						self.body = data
						del data
				elif argument == '--service':
					# If the argument is for specifying the web service of the mails, then we continue to parse the next argument as the entered value

					try:
						self.webservice = arguments[index + 1]
					except IndexError:
						# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

						continue
				elif argument == '--help':
					# If the argument is for displaying the help information, then we mark the self.documentation as True

					self.documentation = True
				else:
					# If the currently iterated argument is not recognized, then we skip the current iteration

					continue
			# ----

		# Checking whether user requested to be launched in documentation mode or execution mode
		if self.documentation:
			# If the user specified to be run in documentation mode, then we continue displaying the help text on the console screen

			print('mail\nUsage : mail <arguments>\n\n\'mail\' is a tool which serves the feature of sending emails. The tool requires the user login credentials for a particular email service (SMTP server). The email can be send by specifying the particular web service. Currently supported web services are : google (gmail), yahoo mail, protonmail. The arguments are used by this tool / command in order to get the user inputs required for the email to be sent properly.\n\nArguments that can be used are :\n--sender        Used to specify the username of the sender\'s email address (e.g., user12345 from user12345@gmail.com)\n--password      Used to specify the password of the sender\'s email address\n--receiver      Used to specify the receiver\'s email address\n--subject       Used to specify the subject of the email (to be sent)\n--body          Used to specify the file which contains the body of the email (to be sent)\n--service       Used to specify the web service by which the email is to be sent (e.g., google, yahoo)\n\nRead the below steps for proper usage :\n1. Example of sending an email using a gmail account. [Google account should allow access to third party apps]\n\nmail --sender user12345 --password <password> --receiver <receiver email address> --subject <subject> --body /file/body/contents.txt --webservice google\nOR\nmail --sender user12345 --password <password> --receiver <receiver email address> --subject <subject> --body /file/body/contents.txt --webservice gmail\n\n2. Example of sending an email using a yahoo mail account. [Yahoo account should allow access to third party apps]\n\nmail --sender user12345 --password <password> --receiver <receiver email address> --subject <subject> --body /file/body/contents.txt --webservice yahoo\nOR\nmail --sender user12345 --password <password> --receiver <receiver email address> --subject <subject> --body /file/body/contents.txt --webservice yahoomail\n\n3. Example of sending an email using a proton mail account. Sending emails using protonmail requires a protonmail bridge to be running on the local machine (at address: localhost). First launch the protonmail bridge on the local machine, then run the below specified command. Make sure you enter the proper port number here.\n\nmail --sender user12345 --password <password> --receiver <receiver email address> --subject <subject> --body /file/body/contents.txt --webservice proton\nOR\nmail --sender user12345 --password <password> --receiver <receiver email address> --subject <subject> --body /file/body/contents.txt --webservice protonmail\n\nFor more detailed information, check out the docs.')
		else:
			# If the user specified to be run in execution mode (not in documentation mode), then we continue

			# Validating the user entered inputs
			# ----
			# Validating the sender (sender's username) 
			if self.sender == None:
				# If the sender is not specified by the user, then we raise an error with custom message

				raise SyntaxError('sender not specified. Check out the help for more info and usage.')
			else:
				# If the sender is specified by the user, then we continue

				if type(self.sender) == str:
					# If the type of the value for sender entered by the user is string, then we continue

					if len(self.sender) < 3:
						# If the length of the sender string (sender's username string) is less than 3 characters, then we raise an error with a custom message

						raise ValueError('sender value should be string with a proper length. It is the username of the sender\'s email address.')
				else:
					# If the type of the value for sender entered by the user is not string, then we raise an error with a custom message

					raise TypeError('sender value should be a string. It is the username of the sender\'s email address.')

			# Validating the password (sender's password)
			if self.password == None:
				# If the password is not specified by the user, then we raise an error with custom message

				raise SyntaxError('password not specified. Check out the help for more info and usage.')
			else:
				# If the password is specified by the user, then we continue

				if type(self.password) == str:
					# If the type of the value for password entered by the user is string, then we continue

					if len(self.password) < 4:
						# If the length of the password string (password of the sender) is less than 4 characters, then we raise an error with a custom message

						raise ValueError('password value should be string with a proper length. It is the username of the password\'s email address.')
				else:
					# If the type of the value for password entered by the user is not string, then we raise an error with a custom message

					raise TypeError('password value should be a string. It is the username of the password\'s email address.')

			# Validating the receiver (receiver email address)
			if self.receiver == None:
				# If the receiver is not specified by the user, then we raise an error with custom message

				raise SyntaxError('receiver not specified. Check out the help for more info and usage.')
			else:
				# If the receiver is specified by the user, then we continue

				if type(self.receiver) == str:
					# If the type of the value for receiver entered by the user is string, then we continue

					if len(self.receiver) < 5:
						# If the length of the receiver string (receiver's email string) is less than 5 characters, then we raise an error with a custom message

						raise ValueError('receiver value should be string with a proper length. It is the receiver\'s email address.')
				else:
					# If the type of the value for receiver entered by the user is not string, then we raise an error with a custom message

					raise TypeError('receiver value should be a string. It is the username of the receiver\'s email address.')

			# Validating the subject of the mail
			if self.subject == None:
				# If the subject of the mail is not specified by the user, then we raise an error with a custom message

				raise SyntaxError('subject not specified. Check out the help for more info and usage.')
			else:
				# If the subject of the mail is specified by the user, then we continue

				if type(self.subject) == str:
					# If the type of value for subject of the mail entered by the user is string, then we continue

					if len(self.subject) == 0:
						# If the length of subject of the mail as per entered by the user is 0, then we raise an error with a custom message

						raise ValueError('subject value should be string with atleast length of 1. It is the subject of the mail.')
				else:
					# If the type of value for subject of the mail entered by the user is not string, then we raise an error with a custom message

					raise TypeError('subject value should be a string. It is the subject of the mail.')

			# Validating the body of the mail
			if self.body == None:
				# If the body of the mail is not specified by the user, then we continue

				raise SyntaxError('body not specifed. Check out the help for more info and usage.')
			else:
				# If the body of the mail is specified by the user, then we continue

				if type(self.body) == str:
					# If the type of value for body of the mail entered by the user is string, then we continue

					pass
				else:
					# If the type of value for body of the mail entered by the user is not string, then we raise an error with custom message

					raise TypeError('body value should be a string. It is the body of the mail.')

			# Validating the webservice input as provided
			if self.webservice == None:
				# If the webservice input is not specified by the user, then we raise an error with a custom message

				raise SyntaxError('web service not specified. Check out the help for more info and usage.')
			else:
				# If the webservice input is specified by the user, then we continue

				if type(self.webservice) == str:
					# If the type of webservice input is a string, then we continue

					pass
				else:
					# If the type of webservice input is not a string, then we raise an error with a custom message

					raise TypeError('webservice value should be a string. It is the web service in which the sender uses to send the email.') 
			# ----

			# Checking the web service (which is used to send the email)
			# ----
			if self.webservice.lower() == 'gmail' or self.webservice.lower() == 'google':
				# If the web service for sending the mail is google / gmail, then we continue

				self.gmail()
			elif self.webservice.lower() == 'yahoo' or self.webservice.lower() == 'yahoomail':
				# If the web service for sending the mail is yahoo / yahoomail, then we continue

				self.yahoomail()
			elif self.webservice.lower() == 'proton' or self.webservice.lower() == 'protonmail':
				# If the web service for sending the mail is proton / protonmail, then we continue

				self.protonmail()
			else:
				# If the web service specified by the user is not specified, then we raise an error with a custom message

				raise TypeError(f'Specified web service "{self.webservice}" is not recognized.')
			# ----

	def gmail(self):
		""" This method / function serves the functionality for sending the email through google / gmail. This function uses the value stored in the class variables self.sender, self.password, self.receiver, self.subject, self.body. The function requires the google account to have enabled third-party application access. Otherwise the function will result in error. """

		# Setting up the MIME
		message = MIMEMultipart()
		message["From"] = f'{self.sender}@gmail.com'
		message["To"] = self.receiver
		message["Subject"] = self.subject

		# Attaching the body of the mail
		message.attach(MIMEText(self.body, 'plain'))

		try:
			# Creating a SMTP session for sending the mail
			# Connecting to the SMTP server of the google mail (gmail) which is available at the port 587
			session = smtplib.SMTP('smtp.gmail.com', 587)
			session.starttls()
			session.login(self.sender, self.password)  # Logging into the SMTP session using the user provided username and password combination

			# Sending the mail
			message = message.as_string()
			session.sendmail(self.sender, self.receiver, message)
			session.quit()
		except Exception as e:
			# If there are any errors encountered during the process, then we display the error message on the console screen

			print(f'[ Error : {e} ]')
			return 0
		else:
			# If there are no errors encountered during the process, then we display the mail sent message on the console screen

			print('[ Mail sent ]')
			return 0

	def yahoomail(self):
		""" This method / function serves the functionality for sending the email through yahoo mail. This function uses the value stored in the class variables self.sender, self.password, self.receiver, self.subject, self.body. The function requires the google account to have enabled third-party application access. Otherwise the function will result in error. """

		# Setting up the MIME
		message = MIMEMultipart()
		message["From"] = f'{self.sender}@yahoo.com'
		message["To"] = self.receiver
		message["Subject"] = self.subject

		# Attaching the body of the mail
		message.attach(MIMEText(self.body, 'plain'))

		try:
			# Creating a SMTP session for sending the mail
			# Connecting to the SMTP server of the yahoo mail which is available at the port 587
			session = smtplib.SMTP('smtp.mail.yahoo.com', 587)
			session.starttls()
			session.login(f'{self.sender}@yahoo.com', self.password)  # Logging into the SMTP session using the user provided username and password combination

			# Sending the mail
			message = message.as_string()
			session.sendmail(self.sender, self.receiver, message)
			session.quit()
		except Exception as e:
			# If there are any errors encountered during the process, then we display the error message on the console screen

			print(f'[ Error : {e} ]')
			return 0
		else:
			# If there are no errors encountered during the process, then we display the mail sent message on the console screen

			print('[ Mail sent ]')
			return 0

	def protonmail(self):
		""" This method / function serves the functionality for sending the email through proton mail. This function uses the value stored in the class variables self.sender, self.password, self.receiver, self.subject, self.body. The function requires the google account to have enabled third-party application access. Otherwise the function will result in error.

		This function has the following requirements :
		1. A proton mail bridge should be running on the local machine and the particular port number should be memorized in order to connect to the SMTP server.
		2. The proton mail account should have allowed authorizations to these third party applications + 2-step verification is requried to be turned off, otherwise this function will never be able to connect to the respective SMTP server. """

		# Setting up the MIME
		message = MIMEMultipart()
		message["From"] = f'{self.sender}@protonmail.com'
		message["To"] = self.receiver
		message["Subject"] = self.subject

		# Attaching the body of the mail
		message.attach(MIMEText(self.body, 'plain'))

		try:
			# Creating a SMTP session for sending the mail

			# Asking the user to enter the port number where the ProtonMail bridge is running on the local machine
			port = int(input('Enter the port number (ProtonMail bridge) : '))

			# Connecting to the SMTP server of at the localhost with the user provided port number (where the proton mail bridge is running on the local machine)
			session = smtplib.SMTP('localhost', port)
			session.starttls()
			session.login(f'{self.sender}@protonmail.com', self.password)  # Logging into the SMTP session using the user provided username and password combination

			# Sending the mail
			message = message.as_string()
			session.sendmail(self.sender, self.receiver, message)
			session.quit()
		except Exception as e:
			# If there are any errors encountered during the process, then we display the error message on the console screen

			print(f'[ Error : {e} ]')
			return 0
		else:
			# If there are no errors encountered during the process, then we display the mail sent message on the console screen

			print('[ Mail sent ]')
			return 0

	@staticmethod
	def custommail(sender = None, password = None, receiver = None, subject = None, body = None, smtpserver_url = None, smtpserver_port = None, arguments = None):
		""" This method / function serves the functionality of sending emails through a custom / different SMTP server. This is a static method, thus this particular method of the Mail class can be used directly even without specifying the class variables.

		This method uses different parameters than the class object. This method requires its own parameters, and thus there are also two ways to specify the parameters in this function.
		First of all, the parameters are 
		
		sender -> The email address of the sender
		password -> The password of the sender's email account (Required in order to login into the SMTP server)
		receiver -> The email address of the receiver
		subject -> The subject of the email which is to be sent
		body -> The body of the email which is to be sent (The body means the message / contents of the email)
		smtpserver_url -> The URL at which the SMTP server is accessible
		smtpserver_port -> The port at which the SMTP server is running on the specified URL

		* All the paramters are requried to be specified in order for the email to be successfully sent.

		This function takes two types of inputs in order to send emails :
		1. Arguments parsing

			In this mode, the arguments parsed at the shell after the user enters a command are passed to this class object. The syntax is below
			Mail(arguments = <parsed arguments list>)
			
			The arguments that are recongized by this class object are listed below
			--sender        Used to specify the sender's username
			--password      Used to specify the sender's password
			--receiver      Used to specify the receiver's email address (target email address)
			--subject       Used to specify the subject of the mail
			--body          Used to specify the file location which contains the contents of the body of the mail
			--server-url    Used to specify the URL at which the SMTP server is accessible
			--server-port   Used to specify the port at which the STMP server is running (accessible)

			As we all know that the argument token are parsed on the basis of whitespaces, therefore if the any of the input argument requires whitespaces between them. Then, we will use the whitespace character escape sequence in order to use the whitespace values in our parameters. Example of such is shown below.
			mail custom --sender <username> --password <password> --receiver <target-email-address> --subject Subject\ with\ whitespace --body <content file> --service google

		2. Parameters passed directly

			In this mode, the values are directly passed as parameters to the class object. The rules are same, except the fact that the whitespace escape sequence is not used here. As the values are passed directly as strings.
			Below is an example syntax.

			Mail(
				sender = <username>,
				password = <password>,
				receiver = <receiver email adddress>,
				subject = <subject of the mail>,
				body = <body contents of the mail>,
				smtpserver_url = <url of the smtp server>,
				smtpserver_port = <port of the smtp server>,
			)

			Note that the body parameter here takes the body contents directly instead of taking a file location as an input, from which the contents of the body is to be read.

		How can we use this function :
		1. We can use this custommail() function in order to send emails from privately owned domains and else.
		2. We can also use this custommail() function in order to send emails from a custom made email server (SMTP server).
		"""

		# Checking if arguments provided or just the parameters directly
		if arguments == None:
			# If the arguments are not passed to this function by the user, then we continue to use the default provided values

			pass
		else:
			# If the arguments are passed to this function by the user, then we continue to parse the arguments

			# Parsing the arguments entered to this function
			# ----
			# Setting the default value of the variables to None
			sender = None
			password = None
			receiver = None
			subject = None
			body = None
			smtpserver_url = None
			smtpserver_port = None
			documentation = True

			# Iterating through each argument to filter out the values
			for index, argument in enumerate(arguments):
				# Iterating through each argument item

				if argument == '--sender':
					# If the argument is for specifying the sender's username, then we continue to parse the next argument as the entered value

					try:
						sender = arguments[index + 1]
					except IndexError:
						# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

						continue
				elif argument == '--password':
					# If the argument is for specifying the user's password, then we continue to parse the next argument as the entered value

					try:
						password = arguments[index + 1]
					except IndexError:
						# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

						continue
				elif argument == '--receiver':
					# If the argument is for specifying the receiver's email address, then we continue to parse the next argument as the entered value

					try:
						receiver = arguments[index + 1]
					except IndexError:
						# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

						continue
				elif argument == '--subject':
					# If the argument is for specifying the subject of the mail, then we continue to parse the next argument as the entered value

					try:
						subject = arguments[index + 1]
					except IndexError:
						# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

						continue
				elif argument == '--body':
					# If the argument is for specifying the body of the mail, then we continue to parse the next argument as the entered value (The value would be of a text file which will contain the entire contents of the body of the mail)

					try:
						# Reading the data of the file location specified
						data = open(arguments[index + 1], 'r').read()
					except IndexError:
						# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

						continue
					else:
						# If there are not errors encountered during the process, then we set the contents of the specified file as the body of the email

						body = data
						del data
				elif argument == '--server-url':
					# If the argument is for specifying the URL of the STMP server, then we continue to parse the next argument as the entered value

					try:
						smtpserver_url = arguments[index + 1]
					except IndexError:
						# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

						continue
				elif argument == '--server-port':
					# If the argument is for specifying the port in which the STMP server is running, then we continue to parse the next argument as the entered value

					try:
						smtpserver_port = int(arguments[index + 1])
					except IndexError:
						# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

						continue
					except ValueError:
						# If the next argument is not an integer (encountered in the process of parsing in int format), then we continue

						print(f'[ Error : Failed to fetch the port number of the SMTP server. Invalid value - {argument[index + 1]} ]')
						return 0
				elif argument == '--help':
					# If the argument is for displaying the help information, then we mark the self.documentation as True

					documentation = True
				else:
					# If the currently iterated argument is not recognized, then we skip the current iteration

					continue
			# ----

		# Checking whether the user requested the documentation mode or the execution mode
		if documentation:
			# If the user specified the documentation mode, then we display the entire help text on the console screen

			print('mail-custom\nUsage : mail-custom <arguments>\n\n\'mail-custom\' is a tool which serves the feature of sending emails from a custom SMTP server / email service. The tool requires the URL and port at which the SMTP server is running, as well as the login credentials of the user account from which the email is to be sent.\n\nThis tool / command can be used for these tasks :\n1. Sending emails from a custom SMTP server (A server either made by user, or someone).\n2. Sending emails from a email service that is not supported directly by the mail tool.\n\nArguments that can be used are :\n--sender        Used to specify the username of the sender\'s email address (e.g., user12345 from user12345@custom.com)\n--password      Used to specify the password of the sender\'s email address\n--receiver      Used to specify the receiver\'s email address\n--subject       Used to specify the subject of the email (to be sent)\n--body          Used to specify the file which contains the body of the email (to be sent)\n--server        Used to specify the URL at which the SMTP server is running\n--port          Used to specify the port at which the SMTP server is running\n\nExample of command (syntax) :\n\nmail-custom --sender <username> --password <password> --receiver <receiver\'s email address> --subject <subject> --body /file/body/contents.txt --server https://custom.mail.com/ --port 0000\n\nFor more detailed information, check out the docs.')
			return 0
		else:
			# If the user specified the execution mode, then we continue

			# Validating the user specified inputs
			# ----
			# Validating the sender parameter's input value (The sender's email address - complete email addresss)
			if sender == None:
				# If the value for the sender is not specified by the user (default value), then we raise an error with a custom message

				raise SyntaxError('sender value not specified. The value is of the sender\'s email address.')
			else:
				# If the value of the sender is specified by the user, then we continue for further validation

				if type(sender) == str:
					# If the value of the sender parameter specified by the user is of string type, then we continue for further validation

					if len(sender) >= 5:
						# If the length of the value of the sender parameter specified by the user is more than or equal to 5, then we continue

						pass
					else:
						# If the length of the value of the sender parameter specified by the user is not of valid length, then we raise an error with a custom message

						raise('sender value is invalid. The length of the sender parameter is less than 5 characters.')
				else:
					# If the value of the sender parameter specified by the user is not of string type, then we raise an error with a custom message

					raise ValueError('sender value is invalid. Requires a string value with proper length, as this parameter is to specify the email address of the sender.')

			# Validating the password parameter's input value (The password of the sender's email)
			if password == None:
				# If the value for the password is not specified by the user (default value), then we raise an error with a custom message

				raise SyntaxError('password value not specified. The value is of the sender\'s email password.')
			else:
				# If the value of the password is specified by the user, then we continue for further validation

				if type(password) == str:
					# If the value of the password parameter specified by the user is of string type, then we continue for further validation

					if len(password) >= 5:
						# If the length of the value of the password parameter specified by the user is more than or equal to 5, then we continue

						pass
					else:
						# If the length of the value of the password parameter specified by the user is not of valid length, then we raise an error with a custom message

						raise('password value is invalid. The length of the password parameter is less than 5 characters.')
				else:
					# If the value of the password parameter specified by the user is not of string type, then we raise an error with a custom message

					raise ValueError('password value is invalid. Requires a string value, as this parameter is to specify the password of the sender\'s email account.')

			# Validating the receiver paramter's input (The receiver's email address / target's email address)
			if receiver == None:
				# If the value for the receiver is not specified by the user (default value), then we raise an error with a custom message

				raise SyntaxError('receiver value not specified. The value is of the receiver\'s email address.')
			else:
				# If the value of the receiver is specified by the user, then we continue for further validation

				if type(receiver) == str:
					# If the value of the receiver parameter specified by the user is of string type, then we continue for further validation

					if len(receiver) >= 5:
						# If the length of the value of the receiver parameter specified by the user is more than or equal to 5, then we continue

						pass
					else:
						# If the length of the value of the receiver parameter specified by the user is not of valid length, then we raise an error with a custom message

						raise('receiver value is invalid. The length of the receiver parameter is less than 5 characters.')
				else:
					# If the value of the receiver parameter specified by the user is not of string type, then we raise an error with a custom message

					raise ValueError('receiver value is invalid. Requires a string value with proper length, as this parameter is to specify the email address of the receiver.')

			# Validating the subject parameter's input (The subject of the email to be sent)
			if subject == None:
				# If the value for the subject is not specified by the user (default value), then we raise an error with a custom message

				raise SyntaxError('subject value not specified. The value is of the subject of the mail to be sent.')
			else:
				# If the value of the subject is specified by the user, then we continue for further validation

				if type(subject) == str:
					# If the value of the subject parameter specified by the user is of string type, then we continue for further validation

					if len(subject) != 0:
						# If the length of the value of the subject parameter specified by the user is more than 0, then we continue

						pass
					else:
						# If the length of the value of the subject parameter specified by the user is not of valid length, then we raise an error with a custom message

						raise('subject value is invalid. The length of the subject parameter should atleast be of 1 character.')
				else:
					# If the value of the subject parameter specified by the user is not of string type, then we raise an error with a custom message

					raise ValueError('subject value is invalid. Requires a string value with atleast length of 1 character, as this parameter is to specify the subject of the email that is to be sent.')

			# Validating the body parameter's input (The body of the email to be sent / The contents of the email)
			if body == None:
				# If the value for the body is not specified by the user (default value), then we raise an error with a custom message

				raise SyntaxError('body value not specified. The value is of the body of the mail to be sent.')
			else:
				# If the value of the body is specified by the user, then we continue for further validation

				if type(body) == str:
					# If the value of the body parameter specified by the user is of string type, then we continue for further validation

					if len(body) != 0:
						# If the length of the value of the body parameter specified by the user is more than 0, then we continue

						pass
					else:
						# If the length of the value of the body parameter specified by the user is not of valid length, then we raise an error with a custom message

						raise('body value is invalid. The length of the body parameter should atleast be of 1 character.')
				else:
					# If the value of the body parameter specified by the user is not of string type, then we raise an error with a custom message

					raise ValueError('body value is invalid. Requires a string value with length of alteast 1 character, as this parameter is to specify the body of the email that is to be sent.')

			# Validating the SMTP server URL parameter's input (The URL at the which the SMTP server can be accessible)
			if smtpserver_url == None:
				# If the value for the smtpserver_url is not specified by the user (default value), then we raise an error with a custom message

				raise SyntaxError('smtpserver_url value not specified. The value is of the URL where the SMTP server is accessible.')
			else:
				# If the value of the smtpserver_url is specified by the user, then we continue for further validation

				if type(smtpserver_url) == str:
					# If the value of the smtpserver_url parameter specified by the user is of string type, then we continue for further validation

					if len(smtpserver_url) > 3:
						# If the length of the value of the smtpserver_url parameter specified by the user is more than 3, then we continue

						pass
					else:
						# If the length of the value of the smtpserver_url parameter specified by the user is not of valid length, then we raise an error with a custom message

						raise('smtpserver_url value is invalid.')
				else:
					# If the value of the smtpserver_url parameter specified by the user is not of string type, then we raise an error with a custom message

					raise ValueError('smtpserver_url value is invalid. Requires a string value with proper length.')

			# Validating the SMTP server port parameter's input (The port number at which the SMTP server is running on)
			if smtpserver_port == None:
				# If the value for the smtpserver_port is not specified by the user (default value), then we raise an error with a custom message

				raise SyntaxError('smtpserver_port value not specified. The value is of the port where the SMTP server is running.')
			else:
				# If the value of the smtpserver_url is specified by the user, then we continue for further validation

				if type(smtpserver_port) == int:
					# If the value of the smtpserver_port parameter specified by the user is of int type, then we continue for further validation

					pass
				else:
					# If the value of the smtpserver_port parameter specified by the user is not of int type, then we raise an error with a custom message

					raise ValueError('smtpserver_port value is invalid. Requires a proper numeric port number.')
			# ----

			# Setting up the MIME
			message = MIMEMultipart()
			message["From"] = sender
			message["To"] = receiver
			message["Subject"] = subject

			# Attaching the body of the mail
			message.attach(MIMEText(body, 'plain'))

			try:
				# Creating a SMTP session for sending the mail

				# Connecting to the SMTP server with custom url and port as per specified by the user
				session = smtplib.SMTP(smtpserver_url, smtpserver_port)
				session.starttls()
				session.login(sender, password)  # Logging into the SMTP session using the user provided username and password combination

				# Sending the mail
				message = message.as_string()
				session.sendmail(sender, receiver, message)
				session.quit()
			except Exception as e:
				# If there are any errors encountered during the process, then we display the error message on the console screen

				print(f'[ Error : {e} ]')
				return 0
			else:
				# If there are no errors encountered during the process, then we display the mail sent message on the console screen

				print('[ Mail sent ]')
				return 0

	@staticmethod
	def encryptedmail(sender = None, password = None, receiver = None, subject = None, body = None, encryption_key = None, webservice = None, documentation = False, arguments = None):
		""" This method / function serves the functionality of sending encrypted emails. The task of encryption is done using a password / encryption key. This method is a static method that can be called directly without passing the other parameters to the main class objects. Just like

		Mail.encryptedmail(<parameters>)

		This function takes the parameters in two formats :
		1. Parsing arguments :

			Here, the parsed tokens from the arguments entered by the user at the command line / shell are used to extract the parameters for the function to run properly. The arguments that are parsed via this function are listed below.

			--sender            Used to specify the sender's username / email address
			--password          Used to specify the password of the sender
			--receiver          Used to specify the receiver's email address
			--subject           Used to specify the subject of the email to be sent
			--body              Used to specify the body of the email to be sent
			--encryption-key    Used to specify the key / password for encrypting / decrypting the email contents
			--service           Used to specify the email service to be used for sending the email

			The way of parsing argument tokens uses the whitespace method, thus we cannot specify the entire body contents here. And, instead we are just taking the input of a text file which contains the body contents / the contents of the message in the mail. The file location specified after the --body tag / argument is then used to read the file and extract the complete file contents. The extracted file contents are then used as the message of the email to be sent.

			Below is a syntax / example of this way of usage of this encryptedmail tool

			mail encrypted --sender <sender email address> --password <password> --receiver <receiver email address> --subject <subject of the mail> --body /file/email/body.txt --encryption-key <encryption password> --service <email service to be used>

		2. Directly from parameters :

			Here, the parameters are directly specified to the function. The parameters used / accepted by this function are listed below.

			sender -> Parameter to specify the sender's username / email address
			password -> Parameter to specify the password of the sender
			receiver -> Parameter to specify the receiver's email address
			subject -> Paramter to specify the subject of the email that is to be sent
			body -> Parameter to specify the body of the email that is to be sent
			encryption_key -> Parameter to specify the key / password for encrypting / decrypting the email contents
			webservice -> Parameter to specify the email service to be used for sending the email

			Here, the contents of the body file is to be specified directly, instead of reading from a file. The user is meant to write / type in the complete body content of the email in the parameter of 'body'. An example for the executing the function in this way is shown below.

			Mail.encryptedmail(
				sender = 'test123'
				password = 'somerandompassword123',
				receiver = 'somerandomuser@gmail.com',
				subject = 'Testing our encrypted mail feature',
				body = 'The contents of the body of the email. This piece of text is encrypted with password that the user provides.',
				encryption_key = 'somerandompassword098',
				webservice = 'google',
			)

		There are some points to be noted while using this function. These are :
		* The sender parameter is used to specify the sender's username as well as email address. Here is the rule : When using google (gmail), yahoo, or proton mail service, then just mention the username of the sender. And, when using any custom mailing service or any service other than the ones mentioned, then specify the full email address in the sender parameter.

		* The password parameter is the password for the sender's email account, this is required as we are gonna need it to authenticate ourselves into the SMTP server.

		* The encrypted mails can be decrypted using the StringEncrypter.decrypt() method which is defined in the encryption.py module file.
		"""

		# Checking if arguments provided or just the parameters directly
		if arguments == None:
			# If the arguments are not passed to this function by the user, then we continue to use the default provided values

			pass
		else:
			# If the arguments are passed to this function by the user, then we continue to parse the arguments

			# Parsing the arguments entered to this function
			# ----
			# Setting the default value of the variables to None
			sender = None
			password = None
			receiver = None
			subject = None
			body = None
			encryption_key = None
			webservice = None
			documentation = True

			# Iterating through each argument to filter out the values
			for index, argument in enumerate(arguments):
				# Iterating through each argument item

				if argument == '--sender':
					# If the argument is for specifying the sender's username, then we continue to parse the next argument as the entered value

					try:
						sender = arguments[index + 1]
					except IndexError:
						# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

						continue
				elif argument == '--password':
					# If the argument is for specifying the user's password, then we continue to parse the next argument as the entered value

					try:
						password = arguments[index + 1]
					except IndexError:
						# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

						continue
				elif argument == '--receiver':
					# If the argument is for specifying the receiver's email address, then we continue to parse the next argument as the entered value

					try:
						receiver = arguments[index + 1]
					except IndexError:
						# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

						continue
				elif argument == '--subject':
					# If the argument is for specifying the subject of the mail, then we continue to parse the next argument as the entered value

					try:
						subject = arguments[index + 1]
					except IndexError:
						# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

						continue
				elif argument == '--body':
					# If the argument is for specifying the body of the mail, then we continue to parse the next argument as the entered value (The value would be of a text file which will contain the entire contents of the body of the mail)

					try:
						# Reading the data of the file location specified
						data = open(arguments[index + 1], 'r').read()
					except IndexError:
						# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

						continue
					else:
						# If there are not errors encountered during the process, then we set the contents of the specified file as the body of the email

						body = data
						del data
				elif argument == '--encryption-key':
					# If the argument is for specifying the encryption key of the email, then we continue to parse the next argument as the entered value

					try:
						encryption_key = arguments[index + 1]
					except IndexError:
						# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

						continue
				elif argument == '--service':
					# If the argument is for specifying the email service, then we continue to parse the next argument as the entered value

					try:
						webservice = arguments[index + 1]
					except IndexError:
						# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

						continue
				elif argument == '--help':
					# If the argument is for displaying the help information, then we mark the self.documentation as True

					documentation = True
				else:
					# If the currently iterated argument is not recognized, then we skip the current iteration

					continue
			# ----

		# Checking whether the user requested the documentation mode or the execution mode
		if documentation:
			# If the user specified the documentation mode, then we display the entire help text on the console screen

			print('<--Help for encrypted mail-->')
			return 0
		else:
			# If the user specified the execution mode, then we continue

			# Validating the user specified inputs
			# ----
			# Validating the sender parameter's input value (The sender's email address - complete email addresss)
			if sender == None:
				# If the value for the sender is not specified by the user (default value), then we raise an error with a custom message

				raise SyntaxError('sender value not specified. The value is of the sender\'s email address.')
			else:
				# If the value of the sender is specified by the user, then we continue for further validation

				if type(sender) == str:
					# If the value of the sender parameter specified by the user is of string type, then we continue for further validation

					if len(sender) >= 5:
						# If the length of the value of the sender parameter specified by the user is more than or equal to 5, then we continue

						pass
					else:
						# If the length of the value of the sender parameter specified by the user is not of valid length, then we raise an error with a custom message

						raise('sender value is invalid. The length of the sender parameter is less than 5 characters.')
				else:
					# If the value of the sender parameter specified by the user is not of string type, then we raise an error with a custom message

					raise ValueError('sender value is invalid. Requires a string value with proper length, as this parameter is to specify the email address of the sender.')

			# Validating the password parameter's input value (The password of the sender's email)
			if password == None:
				# If the value for the password is not specified by the user (default value), then we raise an error with a custom message

				raise SyntaxError('password value not specified. The value is of the sender\'s email password.')
			else:
				# If the value of the password is specified by the user, then we continue for further validation

				if type(password) == str:
					# If the value of the password parameter specified by the user is of string type, then we continue for further validation

					if len(password) >= 5:
						# If the length of the value of the password parameter specified by the user is more than or equal to 5, then we continue

						pass
					else:
						# If the length of the value of the password parameter specified by the user is not of valid length, then we raise an error with a custom message

						raise('password value is invalid. The length of the password parameter is less than 5 characters.')
				else:
					# If the value of the password parameter specified by the user is not of string type, then we raise an error with a custom message

					raise ValueError('password value is invalid. Requires a string value, as this parameter is to specify the password of the sender\'s email account.')

			# Validating the receiver paramter's input (The receiver's email address / target's email address)
			if receiver == None:
				# If the value for the receiver is not specified by the user (default value), then we raise an error with a custom message

				raise SyntaxError('receiver value not specified. The value is of the receiver\'s email address.')
			else:
				# If the value of the receiver is specified by the user, then we continue for further validation

				if type(receiver) == str:
					# If the value of the receiver parameter specified by the user is of string type, then we continue for further validation

					if len(receiver) >= 5:
						# If the length of the value of the receiver parameter specified by the user is more than or equal to 5, then we continue

						pass
					else:
						# If the length of the value of the receiver parameter specified by the user is not of valid length, then we raise an error with a custom message

						raise('receiver value is invalid. The length of the receiver parameter is less than 5 characters.')
				else:
					# If the value of the receiver parameter specified by the user is not of string type, then we raise an error with a custom message

					raise ValueError('receiver value is invalid. Requires a string value with proper length, as this parameter is to specify the email address of the receiver.')

			# Validating the subject parameter's input (The subject of the email to be sent)
			if subject == None:
				# If the value for the subject is not specified by the user (default value), then we raise an error with a custom message

				raise SyntaxError('subject value not specified. The value is of the subject of the mail to be sent.')
			else:
				# If the value of the subject is specified by the user, then we continue for further validation

				if type(subject) == str:
					# If the value of the subject parameter specified by the user is of string type, then we continue for further validation

					if len(subject) != 0:
						# If the length of the value of the subject parameter specified by the user is more than 0, then we continue

						pass
					else:
						# If the length of the value of the subject parameter specified by the user is not of valid length, then we raise an error with a custom message

						raise('subject value is invalid. The length of the subject parameter should atleast be of 1 character.')
				else:
					# If the value of the subject parameter specified by the user is not of string type, then we raise an error with a custom message

					raise ValueError('subject value is invalid. Requires a string value with atleast length of 1 character, as this parameter is to specify the subject of the email that is to be sent.')

			# Validating the body parameter's input (The body of the email to be sent / The contents of the email)
			if body == None:
				# If the value for the body is not specified by the user (default value), then we raise an error with a custom message

				raise SyntaxError('body value not specified. The value is of the body of the mail to be sent.')
			else:
				# If the value of the body is specified by the user, then we continue for further validation

				if type(body) == str:
					# If the value of the body parameter specified by the user is of string type, then we continue for further validation

					if len(body) != 0:
						# If the length of the value of the body parameter specified by the user is more than 0, then we continue

						pass
					else:
						# If the length of the value of the body parameter specified by the user is not of valid length, then we raise an error with a custom message

						raise('body value is invalid. The length of the body parameter should atleast be of 1 character.')
				else:
					# If the value of the body parameter specified by the user is not of string type, then we raise an error with a custom message

					raise ValueError('body value is invalid. Requires a string value with length of alteast 1 character, as this parameter is to specify the body of the email that is to be sent.')

			# Validating the encryption key (The password for encrypting / decrypting the body contents of the email to be sent)
			if encryption_key == None:
				# If the value for the encryption key is not specified by the user (default value), then we raise an error with a custom message

				raise SyntaxError('Encryption key value not specified. The key for encrypting / decrypting the contents of the email.')
			else:
				# If the value of the encryption key is specified by the user, then we continue for further validation

				if type(encryption_key) == str:
					# If the value of the encryption key parameter specified by the user is of string type, then we continue for further validation

					if len(encryption_key) > 5:
						# If the length of the value of the encryption key parameter specified by the user is more than 3, then we continue

						pass
					else:
						# If the length of the value of the encryption key parameter specified by the user is not of valid length, then we raise an error with a custom message

						raise('Encryption key value is invalid. Requires a string value with proper length of 6 characters.')
				else:
					# If the value of the encryption key parameter specified by the user is not of string type, then we raise an error with a custom message

					raise ValueError('Encryption key is invalid. Requires a string value with proper length of 6 characters.')

			# Validating the webservice parameter's input (The email providing service used by the sender to send the emails)
			if webservice == None:
				# If the value for the email service is not specified by the user (default value), then we raise an error with a custom message

				raise SyntaxError('Email service value not specified. The email providing service from which the sender will send the emails.')
			else:
				# If the value of the email service is specified by the user, then we continue for further validation

				if type(webservice) == str:
					# If the value of the email service parameter specified by the user is of string type, then we continue for further validation

					if len(webservice) > 3:
						# If the length of the value of the email service parameter specified by the user is more than 3, then we continue

						pass
					else:
						# If the length of the value of the email service parameter specified by the user is not of valid length, then we raise an error with a custom message

						raise('Email service value is invalid. Requires a string value with proper length.')
				else:
					# If the value of the email service parameter specified by the user is not of string type, then we raise an error with a custom message

					raise ValueError('Email service value is invalid. Requires a string value with proper length.')
			# ----

			# Encrypting the contents / body / message of the email
			# ----
			# Generating the key from the encryption using the user entered password for encryption / decryption
			key = 0
			isEven = True

			for i in encryption_key:
				# Iterating over each character in the encrypted key entered by the user
				
				if isEven:
					# If the current iteration is even number, then we add the char code value

					key += ord(i)
				else:
					# If the current iteration is odd number (not even), then we subtract the char code value

					key -= ord(i)

			# Making the key possitive
			if key < 0:
				key *= (-1)

			# Adding the length of the password to itself
			key += len(encryption_key)
			encryption_key = key
			del key, isEven

			# Converting the plain text of the message / body of the email to cipher format
			encryptedText = ''
			for character in body:
				# Iterating through each character in the body of the email

				encryptedText += chr((ord(character) + encryption_key) % 256)

			# Encoding the cipher text into base64 algorithm / format / encoding
			body = b64encode(encryptedText.encode()).decode()
			del encryptedText, encryption_key
			# ----

			# Sending the email
			# ----
			# Checking the emailing service as mentioned by the user
			if webservice.lower() == 'google' or webservice.lower() == 'gmail':
				# If the emailing service specified by the user is google / gmail, then we continue

				try:
					# Setting up the MIME
					message = MIMEMultipart()
					message["From"] = f'{sender}@gmail.com'
					message["To"] = receiver
					message["Subject"] = subject

					# Attaching the body of the mail
					message.attach(MIMEText(body, 'plain'))

					# Creating a SMTP session for sending the mail
					# Connecting to the SMTP server of google mail (gmail)
					session = smtplib.SMTP('smtp.gmail.com', 587)
					session.starttls()
					session.login(sender, password)  # Logging into the SMTP session using the user provided username and password combination

					# Sending the mail
					message = message.as_string()
					session.sendmail(sender, receiver, message)
					session.quit()
				except Exception as e:
					# If there are any errors encountered during the process, then we display the error message on the console screen

					print(f'[ Error : {e} ]')
					return 0
				else:
					# If there are no errors encountered during the process, then we display the mail sent message on the console screen

					print('[ Mail sent. Remember the encryption key. ]')
					return 0
			elif webservice.lower() == 'yahoo' or webservice.lower() == 'yahoomail':
				# If the emailing service specified by the user is yahoo / yahoomail, then we continue

				try:
					# Setting up the MIME
					message = MIMEMultipart()
					message["From"] = f'{sender}@yahoo.com'
					message["To"] = receiver
					message["Subject"] = subject

					# Attaching the body of the mail
					message.attach(MIMEText(body, 'plain'))

					# Creating a SMTP session for sending the mail
					# Connecting to the SMTP server of yahoo mail
					session = smtplib.SMTP('smtp.mail.yahoo.com', 587)
					session.starttls()
					session.login(f'{sender}@yahoo.com', password)  # Logging into the SMTP session using the user provided username and password combination

					# Sending the mail
					message = message.as_string()
					session.sendmail(sender, receiver, message)
					session.quit()
				except Exception as e:
					# If there are any errors encountered during the process, then we display the error message on the console screen

					print(f'[ Error : {e} ]')
					return 0
				else:
					# If there are no errors encountered during the process, then we display the mail sent message on the console screen

					print('[ Mail sent. Remember the encryption key. ]')
					return 0
			elif webservice.lower() == 'proton' or webservice.lower() == 'protonmail':
				# If the emailing service specified by the user is proton mail, then we continue

				try:
					# Setting up the MIME
					message = MIMEMultipart()
					message["From"] = f'{sender}@protonmail.com'
					message["To"] = receiver
					message["Subject"] = subject

					# Attaching the body of the mail
					message.attach(MIMEText(body, 'plain'))

					# Asking the user for the URL and the port where the ProtonMail bridge is running on the local machine / local network
					url = input('Enter the URL where the ProtonMail bridge is runnning (leave blank for localhost) : ')
					if len(url) == 0 or url == ' ':
						# If the URL input is left blank, then we mark the url as the localhost

						url = 'localhost'
					port = int(input('Enter the port at which the ProtonMail bridge is running : '))

					# Creating a SMTP session for sending the mail
					# Connecting to the SMTP server of proton mail
					session = smtplib.SMTP(url, port)
					session.starttls()
					session.login(f'{sender}@protonmail.com', password)  # Logging into the SMTP session using the user provided username and password combination

					# Sending the mail
					message = message.as_string()
					session.sendmail(sender, receiver, message)
					session.quit()
				except Exception as e:
					# If there are any errors encountered during the process, then we display the error message on the console screen

					print(f'[ Error : {e} ]')
					return 0
				else:
					# If there are no errors encountered during the process, then we display the mail sent message on the console screen

					print('[ Mail sent. Remember the encryption key. ]')
					return 0
			elif webservice.lower() == 'custom':
				# If the emailing service specified by the user is custom, then we continue

				try:
					# Setting up the MIME
					message = MIMEMultipart()
					message["From"] = sender
					message["To"] = receiver
					message["Subject"] = subject

					# Attaching the body of the mail
					message.attach(MIMEText(body, 'plain'))

					# Asking the user for the URL and the port where the ProtonMail bridge is running on the local machine / local network
					url = input('Enter the URL of the SMTP server (leave blank for localhost) : ')
					if len(url) == 0 or url == ' ':
						# If the URL input is left blank, then we mark the url as the localhost

						url = 'localhost'
					port = int(input('Enter the port at which the SMTP server is available : '))

					# Creating a SMTP session for sending the mail
					# Connecting to the SMTP server with the user specified url and port
					session = smtplib.SMTP(url, port)
					session.starttls()
					session.login(sender, password)  # Logging into the SMTP session using the user provided username and password combination

					# Sending the mail
					message = message.as_string()
					session.sendmail(sender, receiver, message)
					session.quit()
				except Exception as e:
					# If there are any errors encountered during the process, then we display the error message on the console screen

					print(f'[ Error : {e} ]')
					return 0
				else:
					# If there are no errors encountered during the process, then we display the mail sent message on the console screen

					print('[ Mail sent. Remember the encryption key. ]')
					return 0
			else:
				# If the emailing service specified by the user is not recognized, then we raise an error with a custom message

				raise TypeError(f'Specified web service "{self.webservice}" is not recognized.')
			# ----