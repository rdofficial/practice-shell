"""
networking.py - Python Shell

A module created for supplying the required functions to the shell application. The functions and classes defined in this module ease many tasks at the shell application, in general way they are used in executing the task assigned by the user via the commands. This module contains functions and classes related to directory handling and other such stuff.

Author : Rishav Das (https://github.com/rdofficial/)
Created on : June 1, 2021

Last modified by : Rishav Das (https://github.com/rdofficial/)
Last modified on : June 2, 2021

Changes made in the last modifications :
1. Fixed the errors for the string and int format errors for the port number input in the IP.portscan() method.

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
		print(f"""[#] Local hostname : {self.address}
[#] Local IP address : {socket.gethostbyname(self.address)}""")

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

	def __init__(self, port = 8000, root = None):
		# The default port number is 8000
		# The root of the server will be of the current working directory
		self.port = port
		self.root = root

		if self.root != None:
			# If a specific directory is specified for the server intiliazation, then we continue

			self.changeroot()

		handler = SimpleHTTPRequestHandler
		with TCPServer(('', self.port), handler) as httpd:
			# Launching the http server

			try:
				print(f'Serving at port : {port}')
				httpd.serve_forever()
			except KeyboardInterrupt:
				# If the user pressed CTRL+C key combo, then we stop the server

				chdir(self.initialDirectory)  # Unsetting the current root location to the intial working directory
				httpd.server_close()
			except Exception as e:
				# If there are any errors encountered during the process, then we display the error message on the console screen

				print(f'[ Http Server Error : {e} ]')

	def changeroot(self):
		""" This method / function changes the current working directory to the user specified directory in order to set up as a root location for our simple web server. This function reads the user specified custom root location stored in the class variable self.root """

		# Saving the initial directory location to a class variable
		self.initialDirectory = path.dirname(path.abspath(__file__))

		if path.isdir(self.root):
			# If the user specified directory does exists, then we continue
			
			# Changing the current working directory to the user specified directory
			chdir(self.root)
		else:
			# If the user specified directory does not exists, then we raise the error message and continue with the default directory

			print(f'[ Error : No such directory found "{self.root}" ]')
			self.root = ''