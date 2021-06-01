"""
networking.py - Python Shell

A module created for supplying the required functions to the shell application. The functions and classes defined in this module ease many tasks at the shell application, in general way they are used in executing the task assigned by the user via the commands. This module contains functions and classes related to directory handling and other such stuff.

Author : Rishav Das (https://github.com/rdofficial/)
Created on : June 1, 2021

Last modified by : -
Last modified on : -

Authors contributed to this script (Add your name below if you have contributed) :
1. Rishav Das (github:https://github.com/rdofficial/, email:rdofficial192@gmail.com)
"""

# Importing the required functions and modules
try:
	import socket
	from urllib import request
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
			# If the user did not specified the port ranges properly, then we start scaning ports in the range (default port range)

			initial = 1
			final = 65535
			print('[ Executing the port scanner with default ports (i.e., 1 to 65535) ]')
		
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

		self.address = socket.gethostname()

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