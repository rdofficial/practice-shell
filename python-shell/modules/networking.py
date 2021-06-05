"""
networking.py - Python Shell

A module created for supplying the required functions to the shell application. The functions and classes defined in this module ease many tasks at the shell application, in general way they are used in executing the task assigned by the user via the commands. This module contains functions and classes related to directory handling and other such stuff.

Author : Rishav Das (https://github.com/rdofficial/)
Created on : June 1, 2021

Last modified by : Rishav Das (https://github.com/rdofficial/)
Last modified on : June 3, 2021

Changes made in the last modifications :
1. Updated the console screen output texts and code for the 'Connections' class and its inner methods / functions.

Authors contributed to this script (Add your name below if you have contributed) :
1. Rishav Das (github:https://github.com/rdofficial/, email:rdofficial192@gmail.com)
"""

# Importing the required functions and modules
try:
	# Importing the networks and connections related functions and modules
	import socket
	from socketserver import TCPServer
	from http.server import SimpleHTTPRequestHandler
	from urllib import request

	# Importing the other functions and modules that are required
	from os import chdir, path
	from json import loads
	from sys import stdout
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

		# Fetching the hostname of the local machine
		self.address = socket.gethostname()

		# Displaying the fetched information on the console screen (Also fetching them during the print process)
		print(f"""[#] Local hostname : {self.address}\n[#] Local IP address : {socket.gethostbyname(self.address)}""")

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

					raise ValueError ('[ Error : Invalid port number specified. Proper numeric value between 1-65535 should be provided. ]')
			elif argument == '--root' or argument == '-r':
				# If the argument is for specifying the root location, then we continue to parse the next argument as the entered value

				try:
					self.root = arguments[index + 1]
				except IndexError:
					# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

					continue
			else:
				# If the currently iterated argument is not recognized, then we skip the current iteration

				continue

		# Checking the port number and root location input from the user
		if self.port == None:
			# If the port number is stil not specified by the user, then we ask the port number from the user manually

			self.port = input('Enter the port number : ')
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

				raise SystemError(f'[ Error : No such directory found "{self.root}". ]')

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
	""" The class which serves the feature of the connectins command of the shell. There are functions and methods defined under this class which executes the various tasks under the connections commands. The tasks served by this functions are listed below :
	1. Check all the connections available on a user specified deviced (example - 127.0.0, 192.168.43)

	Some notable points for this class and internal defined variables :
	1. Only IPv4 type address are accepted by this tool, and there are two types of addresses taken in by this function. 1st is the IP address in format xxx.xxx.xxx (Here all the combinations of 1-255 numbers are used post in order to check for connections), and 2nd type is xxx.xxx.xxx.xxx (Here only this single specified IP address is checked for connections).
	2. If the port number 0 entered by the user, then the tool scans for all the port numbers ranging from 1 to 65535. Otherwise they check for a particular port numer. This port number is defined by the argument '-p' or '--port'.
	3. Same if the user does not specifies the port number in the arguments, then the tool checks for all the port numbers ranging from 1 to 65535. """

	def __init__(self, arguments = [], task = None):
		# Setting the self.port and self.address class variables
		self.port = None
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
			elif argument == '--ip-address' or argument == '-i':
				# If the argument is for specifying the IP address, then we continue to parse the next argument as the entered value

				try:
					self.address = arguments[index + 1]
				except IndexError:
					# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

					continue
			else:
				# If the currently iterated argument is not recognized, then we skip the current iteration

				continue

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

				raise SyntaxError('[ Error : Please provide a proper IPv4 address for scanning. Use the --help argument for more information. ]')
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

				raise ValueError('[ Error : Invalid port number specified. Proper numeric value between 1-65535 should be provided. ]')

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