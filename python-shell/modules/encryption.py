"""
encryption.py - Python Shell

A module created for supplying the required functions to the shell application. The functions and classes defined in this module ease many tasks at the shell application, in general way they are used in executing the task assigned by the user via the commands. This module contains functions and classes related to directory handling and other such stuff.

Author : Rishav Das (https://github.com/rdofficial/)
Created on : June 13, 2021

Last modified by : Rishav Das (https://github.com/rdofficial/)
Last modified on : June 18, 2021

Changes made in the last modification :
1. Updated the minor string user input error in the 'StringEncrypter' class.

Authors contributed to this script (Add your name below if you have contributed) :
1. Rishav Das (github:https://github.com/rdofficial/, email:rdofficial192@gmail.com)
"""

# Importing the required functions and modules
try:
	from base64 import b64encode, b64decode, decodebytes
	from io import TextIOWrapper
	from os import path, listdir, remove, rename
	import hashlib
	from json import loads, dumps
	from datetime import datetime
except Exception as e:
	# If there are any errors during the importing of the modules, then we display the error on the console screen

	input(f'\n[ Error : {e} ]\nPress enter key to continue...')
	exit()

class StringEncrypter:
	""" This class serves the features / functionality of encryption as well as decryption of the strings. The encryption / decryption is carried out with a password (encryption key). The class uses its own seperate ways of encryption. Thus if any text / plain string is encrypted using this class (tool), then it can be only decrypted using the decrypt() method of this class.

	This class takes parameter inputs from the user in two ways :
	1. From parsing arguments

		In this mode, the arguments parsed at the shell after the user enters a command are passed to this class object. The syntax is below.

		StringEncrypter(arguments = <parsed arguments list>)

		--password			Used to specify the password for encryption / decryption
		--task              Used to specify the task whether encryption / decryption

		The text / string for encryption is then asked to the user to enter manually.
		Example of a command for encrypting a string is shown below.
		encrypt string --password somehardpassword123 --task encryption

		Example of a command for decrypting a string is shown below.
		encrypt string --password somehardpassword123 --task decryption

	2. From parameters directly

		In this mode, the parameters are defined directly to the class object. All the paramters that are acceptable are listed below in the syntax of this class.

		StringEncrypter(
			text = 'Some random string',
			password = 'Some hard password',
		)

		In this mode, the text that is to be encrypted is specified directly and there are no parameters to specify the task of encryption or decryption. The encryption and decryption can be done by calling the encrypt() and decrypt() method directly.
		Example is shown below.

		enc = StringEncrypter(text = 'Some random text to be processed.', password = 'somehardpassword123')

		enc.encrypt()
		enc.decrypt()

	Some points to be noted about this StringEncrypter are listed below :
	* Any text encrypted using this tool can be decrypted using only this class / tool and the encryption password only.
	* After encryption or decryption, the class variable self.text is replaced with the output text.
	"""

	def __init__(self, text = None, password = None, arguments = None):
		# Checking if arguments provided or just the parameters directly
		if arguments == None:
			# If the arguments are not passed to this function by the user, then we continue to use the default provided values

			self.text = text
			self.password = password
		else:
			# If the arguments are passed to this function by the user, then we continue to parse the arguments

			# Parsing the arguments entered to this function
			# ----
			# Setting the default value of the variables to None
			self.text = None
			self.password = None
			self.documentation = False
			self.task = None

			# Iterating through each argument to filter out the values
			for index, argument in enumerate(arguments):
				# Iterating through each argument item

				if argument == '--password':
					# If the argument is for specifying the password, then we continue to parse the next argument as the entered value

					try:
						self.password = arguments[index + 1]
					except IndexError:
						# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

						continue

				if argument == '--task':
					# If the argument is for specifying the task (encryption / decryption), then we continue to parse the next argument as the entered value

					try:
						self.task = arguments[index + 1]
					except IndexError:
						# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

						continue

				if argument == '--help':
					# If the argument is for specifying the help, then we continue to mark the documentation mode to be true

					self.documentation = True
			# ----

			# Checking whether the task is to be in documentation mode or execution mode
			if self.documentation:
				# If the user specified the documentation mode, then we continue to display the help text on the console screen

				print('encrypt string\nUsage : encrypt string <arguments>\n\n"encrypt string" is a tool which serves the functionality of encryption and decryption of strings. The encryption is done using a password, also the same password will be required for the decryption of the file. This tool uses the same encryption algorithm as used by the rest of the encryption tools. Any string encrypted with this tool, can only be decrypted using this tool only.\n\nArguments are :\n--password        Used to specify the password for encryption / decryption\n--task            Used to specify the task whether encryption / decryption\n--help            Used to display this help text\n\nCheck out the docs for more info.')
			else:
				# If the user specified the execution mode, then we continue to execute the task

				# Validating the user entered password
				# ----
				# Checking the password input type
				if type(self.password) == str:
					# If the password's value as per entered by the user is a string type variable, then we continue for further validation

					# Checking for string length
					if len(self.password) > 4:
						# If the user specified password has character length more than 4, then we continue

						pass
					else:
						# If the user specified password has character length less than 4 charcters, then we raise an error with a custom message

						raise SyntaxError('Password input is invalid. Requires to be an alphanumeric string with length atleast 5.')
				else:
					# If the user entered password's value is a non string variable, then we raise an error with a custom message

					raise SyntaxError('Password input is invalid. Requires to be an alphanumeric string with length atleast 5.')
				# ----

				# Checking the task specified and then continuing to execute the task
				if self.task == None:
					# If the task to be done is not specified by the user (default value), then we raise an error with a custom message

					raise SyntaxError('Task not specified. The task is needed to be specified whether encrypt / decrypt.')
				elif self.task.lower() == 'encrypt' or self.task.lower() == 'encryption':
					# If the task specified is for encryption, then we continue to encrypt

					# Asking the user to enter the string for the encryption / decryption
					self.text = input('Type>> ')

					# Launching the encrypt method in order to encrypt the user string entered by the user
					self.encrypt()
					print(f'Output :\n{self.text}')
				elif self.task.lower() == 'decrypt' or self.task.lower() == 'decryption':
					# If the task specified is for decryption, then we continue to decrypt

					# Asking the user to enter the string for the encryption / decryption
					self.text = input('Type>> ')

					# Launching the decrypt method in order to decrypt the user string entered by the user
					self.decrypt()
					print(f'Output :\n{self.text}')
				else:
					# If the task specified is not recognized, then we raise an error with a custom message

					raise ReferenceError('Task not recognized. Encrypt / decrypt are the two recognizable terms.')
				del self.task

	def generatekey(self):
		""" This method / function serves the purpose of generating a special key for the encryption and decryption using the user entered password. This function takes the value of the user entered password from the class variable self.password.
		The key is generated in such an algorithm, that the key remains possitive integer.

		This function returns the int format key back after the generation. """

		# Generating the key from the encryption using the user entered password for encryption / decryption
		key = 0
		isEven = True

		for i in self.password:
			# Iterating over each character in the encrypted key entered by the user
				
			if isEven:
				# If the current iteration is even number, then we add the char code value

				key += ord(i)
			else:
				# If the current iteration is odd number (not even), then we subtract the char code value

				key -= ord(i)
		del isEven

		# Making the key possitive
		if key < 0:
			# If the key value is less than 0, then we change the negative sign to possitive by simply multiplying it with -1

			key *= (-1)

		# Adding the length of the password to itself
		key += len(self.password)

		# Returning the generating key
		return key

	def encrypt(self):
		""" This method / function serves the functionality of encrypting the user specified string / text using the user specified password. This function uses the value of text and password stored in the class variables self.text, self.password. """

		# Generating the key for the encryption
		key = self.generatekey()

		# Converting each character in the user entered text to cipher format
		text = ''
		for character in self.text:
			# Iterating through each character

			text += chr((ord(character) + key) % 256)

		# Encoding the cipher text into base64 format
		text = b64encode(text.encode()).decode()

		# Setting the encrypted text as the class variable self.text
		self.text = text
		del key, text
		return self.text

	def decrypt(self):
		""" This method / function serves the functionality of decrypting the user specified string / text using the user specified password. This function uses the value of text and password stored in the class variables self.text, self.password. """

		# Generating the key for the encryption
		key = self.generatekey()

		# Decoding from the base64 format to cipher format
		self.text = b64decode(self.text.encode()).decode()

		# Converting each character from cipher text to plain format
		text = ''
		for character in self.text:
			# Iterating through each character

			text += chr((ord(character) - key) % 256)

		# Setting the decrypted text as the class variable self.text
		self.text = text
		del text, key
		return self.text

class FileEncrypter:
	""" This class serves the functionality of encryption and decryption of files (text files and other readable files). The encryption is aided with a password, which is required whenever we want to encrypt / decrypt the file.

	This class object takes input from the user in two ways :
	1. Parsing the argument tokens

		In this mode, the user entered arguments at the shell / terminal are passed to this class object at the parameter 'arguments'. The arguments that are parsed are listed below.

		--file            Used to specify the filename
		--password        Used to specify the password for encryption / decryption
		--task            Used to specify the task whether encryption / decryption

		The file name should be proper and valid. Below are some points listed for the input of the file parameter :
		* If there are whitespaces within the filename, then use the whitespace escape sequence '\ ' in order to make sure the filename is properly accepted into the class object.
		* The file should exists on the local machine as well as proper permission for the current user.

		There is also another flag for documentation mode (printing the help section text for the class object / tool). The flag / argument is --help.

		Example and syntax of the command is shown below.

		encrypt file --password somehardpassword123 --file /location/to/file.txt --task encrypt
		encrypt file --password somehardpassword123 --file /location/to/file.txt --task decrypt

	2. Directly from specified parameters

		In this mode, the user enters the parameters directly into the class object. Example as well as syntax is shown below.

		FileEncrypter(
			filename = '/location/to/file.txt',
			password = 'somehardpassword123',
		)

		Here, there are no needs to use the whitespace escape sequence in order to input the filenames with whitespaces.

	There are some points to be noted about this class :
	1. This class / tool uses the same encryption algorithm as used by the basic StringEncrypter.
	2. This class before decrypting the file, verifies the user entered password for encryption-decryption. If the password matches, then the process to decrypt the file. If the password does not matches, then an error message is displayed on the console screen.
	"""

	def __init__(self, filename = None, password = None, arguments = None):
		# Checking if arguments provided or just the parameters directly
		if arguments == None:
			# If the arguments are not passed to this function by the user, then we continue to use the default provided values

			self.filename = filename
			self.password = password
		else:
			# If the arguments are passed to this function by the user, then we continue to parse the arguments

			# Parsing the arguments entered to this function
			# ----
			# Setting the default value of the variables to None
			self.filename = None
			self.password = None
			self.task = None
			self.documentation = False  # Setting the documentation flag class variable to False by default

			# Iterating through each argument to filter out the values
			for index, argument in enumerate(arguments):
				# Iterating through each argument item

				if argument == '--password':
					# If the argument is for specifying the password, then we continue to parse the next argument as the entered value

					try:
						self.password = arguments[index + 1]
					except IndexError:
						# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

						continue

				if argument == '--file':
					# If the argument is for specifying the file, then we continue to parse the next argument as the entered value

					try:
						self.filename = arguments[index + 1]
					except IndexError:
						# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

						continue

				if argument == '--task':
					# If the argument is for specifying the task (encryption / decryption), then we continue to parse the next argument as the entered value

					try:
						self.task = arguments[index + 1]
					except IndexError:
						# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

						continue

				if argument == '--help':
					# If the argument is for specifying the help, then we continue to mark the documentation mode to be true

					self.documentation = True
			# ----

			# Checking whether the task is to be in documentation mode or execution mode
			if self.documentation:
				# If the user specified the documentation mode, then we continue to display the help text on the console screen

				print('encrypt file\nUsage : encrypt file <arguments>\n\n"encrypt file" is a tool which serves the functionality of encryption and decryption of text files (also other readable files). The encryption is done using a password, also the same password will be required for the decryption of the file. This tool uses the same encryption algorithm as used by the rest of the encryption tools. This tool also provides the feature of checking the passwords before decryption.\n\nArguments are :\n--file            Used to specify the filename\n--password        Used to specify the password for encryption / decryption\n--task            Used to specify the task whether encryption / decryption\n--help            Used to display this help text\n\nThe file name should be proper and valid. Below are some points listed for the input of the file parameter :\n* If there are whitespaces within the filename, then use the whitespace escape sequence \'\\ \' in order to make sure the filename is properly accepted into the class object.\n* The file should exists on the local machine as well as proper permission for the current user.\n\nCheck out the docs for more info.')
			else:
				# If the user specified the execution mode, then we continue to execute the task

				# Validating the user entered parameters
				# ----
				# Validating the filename parameter input (The name / location of the file that is to be encrypted using this tool)
				if self.filename == None:
					# If the filename parameter is not specified by the user (default), then we raise an error with a custom message

					raise SyntaxError('File name not specified.')
				else:
					# If the filename parameter is specified by the user, then we continue for further validation

					if type(self.filename) == str:
						# If the filename parameter input specified by the user is of str type, then we continue

						if path.isfile(self.filename):
							# If the file specified by the user does exists, then we continue

							pass
						else:
							# If the file specified by the user does not exists, then we raise an error with a custom message

							raise FileNotFoundError('Specified file does not exists.')
					else:
						# If the filename parameter input specified by the user is not of str type, then we raise an error on the console screen

						raise TypeError('File name parameter should be in str format.')

				# Validating the password parameter entered by the user
				if self.password == None:
					# If the password parameter is not specified by the user (default), then we raise an error with a custom message

					raise SyntaxError('Password not specified.')
				else:
					# If the password parameter is specified by the user, then we continue for further validation

					if type(self.password) == str:
						# If the password parameter input specified by the user is of str type, then we continue to validate further

						if len(self.password) > 4:
							# If the password parameter input specified by the user is more than 4 character length, then we continue

							pass
						else:
							# If the password parameter input specified by the user is less than 4 character length, then we raise an error with a custom message

							raise SyntaxError('Password invalid. The password input should be a string with atleast 5 character length.')
					else:
						# If the password parameter input specified by the user is not of str type, then we raise an error on the console screen

						raise TypeError('Password invalid. Password parameter should be in str format.')
				# ----

				# Checking the task specified and then continuing to execute the task
				if self.task == None:
					# If the task to be done is not specified by the user (default value), then we raise an error with a custom message

					raise SyntaxError('Task not specified. The task is needed to be specified whether encrypt / decrypt.')
				elif self.task.lower() == 'encrypt' or self.task.lower() == 'encryption':
					# If the task specified is for encryption, then we continue to encrypt

					if self.encrypt() == 0:
						# If the encrypt() method returns 0, then the file has been encrypted successfully and we display the success message on the console screen

						print(f'[ File encrypted : {self.filename} ]')
					else:
						# If the encrypt() method does not returns 0, then the file has been failed to encrypt and we display the failure message on the console screen

						print(f'[ File failed to encrypt : {self.filename} ]')
				elif self.task.lower() == 'decrypt' or self.task.lower() == 'decryption':
					# If the task specified is for decryption, then we continue to decrypt

					if self.decrypt() == 0:
						# If the decrypt() method returns 0, then the file has been decrypted successfully and we display the success message on the console screen

						print(f'[ File decrypted : {self.filename} ]')
					else:
						# If the decrypt() method does not returns 0, then the file has been failed to decrypt and we display the failure message on the console screen

						print(f'[ File failed to decrypt : {self.filename} ]')
				else:
					# If the task specified is not recognized, then we raise an error with a custom message

					raise ReferenceError('Task not recognized. Encrypt / decrypt are the two recognizable terms.')
				del self.task

	def generatekey(self):
		""" This method / function serves the purpose of generating a special key for the encryption and decryption using the user entered password. This function takes the value of the user entered password from the class variable self.password.
		The key is generated in such an algorithm, that the key remains possitive integer.

		This function returns the int format key back after the generation. """

		# Generating the key from the encryption using the user entered password for encryption / decryption
		key = 0
		isEven = True

		for i in self.password:
			# Iterating over each character in the encrypted key entered by the user
				
			if isEven:
				# If the current iteration is even number, then we add the char code value

				key += ord(i)
			else:
				# If the current iteration is odd number (not even), then we subtract the char code value

				key -= ord(i)
		del isEven

		# Making the key possitive
		if key < 0:
			# If the key value is less than 0, then we change the negative sign to possitive by simply multiplying it with -1

			key *= (-1)

		# Adding the length of the password to itself
		key += len(self.password)

		# Returning the generating key
		return key

	def checkpassword(self):
		""" This method / function serves the functionality of checking the user entered password against the original password stored in the file. This function uses the value of password from the class variable self.password.

		When a file is encrypted, the original password is also saved along with the encrypted contents of the file. Thus, we can verify the password of the file before decrypting the file. The function returns True if the password matches, and returns False if the password does not matches. """

		# Reading the contents of the file
		contents = open(self.filename, 'rb').read()
		contents = contents.decode()

		# Reading the password stored in the first line
		password = contents.split('\n')[0]
		del contents

		# Checking the user entered password against the original password stored in the file
		if hashlib.md5(self.password.encode()).hexdigest() == password:
			# If the hashes of user entered password and the original password matches, then we return True

			return True
		else:
			# If the hashes of user entered password and the original password matches, then we return False

			return False

	def encrypt(self):
		""" This method / function serves the feature of encrypting the contents of the file. This function reads the filename location input stored in the class variable self.filename. """

		# Reading the contents of the file specified by the user
		contents = open(self.filename, 'rb').read()
		contents = contents.decode()

		# Generating the encryption key
		key = self.generatekey()

		# Converting the plain text to cipher text
		text = ''
		for character in contents:
			# Iterating through each character

			text += chr((ord(character) + key) % 256)

		# Changing the encoding of the content to base64 format
		text = b64encode(text.encode()).decode()

		# Adding the password to the contents of the file
		text = hashlib.md5(self.password.encode()).hexdigest() + '\n' + text

		# Saving the encrypted content back to the file
		open(self.filename, 'wb').write(text.encode())

		# Deleting some of the variables declared within this function
		del text, key, contents

		# Returning 0 code (It will indicate that the function executed in success)
		return 0

	def decrypt(self):
		""" This method / function serves the feature of decrypting the contents of the file. This function reads the filename location input stored in the class variable self.filename. """

		# Validating the password before decrypting
		if self.checkpassword():
			# If the password matches, then we continue

			# Reading the contents of the file specified by the user
			contents = open(self.filename, 'rb').read()

			# Removing the password part from the file
			contents = contents.decode()
			contents = ' '.join(contents.split('\n')[1:])

			# Converting the base64 format text to plain text
			contents = b64decode(contents.encode()).decode()

			# Generating the encryption key
			key = self.generatekey()

			# Converting the cipher text to plain text
			text = ''
			for character in contents:
				# Iterating through each character

				text += chr((ord(character) - key) % 256)

			# Saving the decrypted content back to the file
			open(self.filename, 'wb').write(text.encode())

			# Deleting some of the variables declared within this function
			del text, key, contents

			# Returning 0 code (It will indicate that the function executed in success)
			return 0
		else:
			# If the password does not matches, then we display the error message on the console screen

			print(f'[ Incorrect password ]')
			return 403

class ImageEncrypter:
	""" This class serves the functionality of encryption and decryption of image files (JPG and PNG). The encryption is aided with a password, which is required whenever we want to encrypt / decrypt the file.

	This class object takes input from the user in two ways :
	1. Parsing the argument tokens

		In this mode, the user entered arguments at the shell / terminal are passed to this class object at the parameter 'arguments'. The arguments that are parsed are listed below.

		--file            Used to specify the image file
		--password        Used to specify the password for encryption / decryption
		--task            Used to specify the task whether encryption / decryption

		The image file name should be proper and valid. Below are some points listed for the input of the file parameter :
		* If there are whitespaces within the filename, then use the whitespace escape sequence '\ ' in order to make sure the filename is properly accepted into the class object.
		* The image file should exists on the local machine as well as proper permission for the current user.

		There is also another flag for documentation mode (printing the help section text for the class object / tool). The flag / argument is --help.

		Example and syntax of the command is shown below.

		encrypt image --password somehardpassword123 --file /location/to/image.jpg --task encrypt
		encrypt image --password somehardpassword123 --file /location/to/image.jpg --task decrypt

	2. Directly from specified parameters

		In this mode, the user enters the parameters directly into the class object. Example as well as syntax is shown below.

		ImageEncrypter(
			filename = '/location/to/image.jpg',
			password = 'somehardpassword123',
		)

		Here, there are no needs to use the whitespace escape sequence in order to input the filenames with whitespaces.

	There are some points to be noted about this class :
	1. This class / tool uses the same encryption algorithm as used by the basic StringEncrypter.
	2. This class before decrypting the file, verifies the user entered password for encryption-decryption. If the password matches, then the process to decrypt the file. If the password does not matches, then an error message is displayed on the console screen.
	3. The size of the image file will get a little increased after the encryption as well as the image would be unviewable graphically due to encrypted bytes.
	"""

	def __init__(self,filename = None, password = None, arguments = None):
		# Checking if arguments provided or just the parameters directly
		if arguments == None:
			# If the arguments are not passed to this function by the user, then we continue to use the default provided values

			self.filename = filename
			self.password = password
		else:
			# If the arguments are passed to this function by the user, then we continue to parse the arguments

			# Parsing the arguments entered to this function
			# ----
			# Setting the default value of the variables to None
			self.filename = None
			self.password = None
			self.task = None
			self.documentation = False  # Setting the documentation flag class variable to False by default

			# Iterating through each argument to filter out the values
			for index, argument in enumerate(arguments):
				# Iterating through each argument item

				if argument == '--password':
					# If the argument is for specifying the password, then we continue to parse the next argument as the entered value

					try:
						self.password = arguments[index + 1]
					except IndexError:
						# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

						continue

				if argument == '--file':
					# If the argument is for specifying the file, then we continue to parse the next argument as the entered value

					try:
						self.filename = arguments[index + 1]
					except IndexError:
						# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

						continue

				if argument == '--task':
					# If the argument is for specifying the task (encryption / decryption), then we continue to parse the next argument as the entered value

					try:
						self.task = arguments[index + 1]
					except IndexError:
						# If the next argument is out of the list index (i.e., it does not exists), then we continue for the next iteration

						continue

				if argument == '--help':
					# If the argument is for specifying the help, then we continue to mark the documentation mode to be true

					self.documentation = True
			# ----

			# Checking whether the task is to be in documentation mode or execution mode
			if self.documentation:
				# If the user specified the documentation mode, then we continue to display the help text on the console screen

				print('encrypt image\nUsage : encrypt image <arguments>\n\n"encrypt image" is a tool which serves the functionality of encryption and decryption of image files (JPG and PNG). The encryption is done using a password, also the same password will be required for the decryption of the file. This tool uses the same encryption algorithm as used by the rest of the encryption tools. This tool also provides the feature of checking the passwords before decryption.\n\nArguments are :\n--file            Used to specify the image file\n--password        Used to specify the password for encryption / decryption\n--task            Used to specify the task whether encryption / decryption\n--help            Used to display this help text\n\nThe image file name should be proper and valid. Below are some points listed for the input of the file parameter :\n* If there are whitespaces within the filename, then use the whitespace escape sequence \'\\ \' in order to make sure the filename is properly accepted into the class object.\n* The file should exists on the local machine as well as proper permission for the current user.\n\nCheck out the docs for more info.')
			else:
				# If the user specified the execution mode, then we continue to execute the task

				# Validating the user entered parameters
				# ----
				# Validating the filename parameter input (The name / location of the file that is to be encrypted using this tool)
				if self.filename == None:
					# If the filename parameter is not specified by the user (default), then we raise an error with a custom message

					raise SyntaxError('Image file name not specified.')
				else:
					# If the filename parameter is specified by the user, then we continue for further validation

					if type(self.filename) == str:
						# If the filename parameter input specified by the user is of str type, then we continue

						if path.isfile(self.filename):
							# If the file specified by the user does exists, then we continue

							if self.filename[len(self.filename) - 3:] == 'jpg' or self.filename[len(self.filename) - 3:] == 'jpeg' or self.filename[len(self.filename) - 3:] == 'png':
								# If the image file specified by the user has the extension JPG or PNG, then we continue

								pass
							else:
								# If the image file specified by the user does not have the extension JPG or PNG, then we raise an error with a custom message

								raise TypeError('Image file specified is not of valid extension. Accepted are jpg or png.')
						else:
							# If the file specified by the user does not exists, then we raise an error with a custom message

							raise FileNotFoundError('Specified image file does not exists.')
					else:
						# If the filename parameter input specified by the user is not of str type, then we raise an error on the console screen

						raise TypeError('Image file name parameter should be in str format.')

				# Validating the password parameter entered by the user
				if self.password == None:
					# If the password parameter is not specified by the user (default), then we raise an error with a custom message

					raise SyntaxError('Password not specified.')
				else:
					# If the password parameter is specified by the user, then we continue for further validation

					if type(self.password) == str:
						# If the password parameter input specified by the user is of str type, then we continue to validate further

						if len(self.password) > 4:
							# If the password parameter input specified by the user is more than 4 character length, then we continue

							pass
						else:
							# If the password parameter input specified by the user is less than 4 character length, then we raise an error with a custom message

							raise SyntaxError('Password invalid. The password input should be a string with atleast 5 character length.')
					else:
						# If the password parameter input specified by the user is not of str type, then we raise an error on the console screen

						raise TypeError('Password invalid. Password parameter should be in str format.')
				# ----

				# Checking the task specified and then continuing to execute the task
				if self.task == None:
					# If the task to be done is not specified by the user (default value), then we raise an error with a custom message

					raise SyntaxError('Task not specified. The task is needed to be specified whether encrypt / decrypt.')
				elif self.task.lower() == 'encrypt' or self.task.lower() == 'encryption':
					# If the task specified is for encryption, then we continue to encrypt

					if self.encrypt() == 0:
						# If the encrypt() method returns 0, then the file has been encrypted successfully and we display the success message on the console screen

						print(f'[ Image encrypted : {self.filename} ]')
					else:
						# If the encrypt() method does not returns 0, then the file has been failed to encrypt and we display the failure message on the console screen

						print(f'[ Image failed to encrypt : {self.filename} ]')
				elif self.task.lower() == 'decrypt' or self.task.lower() == 'decryption':
					# If the task specified is for decryption, then we continue to decrypt

					if self.decrypt() == 0:
						# If the decrypt() method returns 0, then the file has been decrypted successfully and we display the success message on the console screen

						print(f'[ Image file decrypted : {self.filename} ]')
					else:
						# If the decrypt() method does not returns 0, then the file has been failed to decrypt and we display the failure message on the console screen

						print(f'[ Image file failed to decrypt : {self.filename} ]')
				else:
					# If the task specified is not recognized, then we raise an error with a custom message

					raise ReferenceError('Task not recognized. Encrypt / decrypt are the two recognizable terms.')
				del self.task

	def generatekey(self):
		""" This method / function serves the purpose of generating a special key for the encryption and decryption using the user entered password. This function takes the value of the user entered password from the class variable self.password.
		The key is generated in such an algorithm, that the key remains possitive integer.

		This function returns the int format key back after the generation. """

		# Generating the key from the encryption using the user entered password for encryption / decryption
		key = 0
		isEven = True

		for i in self.password:
			# Iterating over each character in the encrypted key entered by the user
				
			if isEven:
				# If the current iteration is even number, then we add the char code value

				key += ord(i)
			else:
				# If the current iteration is odd number (not even), then we subtract the char code value

				key -= ord(i)
		del isEven

		# Making the key possitive
		if key < 0:
			# If the key value is less than 0, then we change the negative sign to possitive by simply multiplying it with -1

			key *= (-1)

		# Adding the length of the password to itself
		key += len(self.password)

		# Returning the generating key
		return key

	def checkpassword(self):
		""" This method / function serves the functionality of checking the user entered password against the original password stored in the image file. This function uses the value of password from the class variable self.password.

		When a image file is encrypted, the original password is also saved along with the encrypted contents of the image file. Thus, we can verify the password of the file before decrypting the file. The function returns True if the password matches, and returns False if the password does not matches. """

		# Reading the contents of the image file
		contents = open(self.filename, 'rb').read()
		contents = contents.decode()

		# Reading the password stored in the first line
		password = contents.split('\n')[0]
		del contents

		# Checking the user entered password against the original password stored in the file
		if hashlib.md5(self.password.encode()).hexdigest() == password:
			# If the hashes of user entered password and the original password matches, then we return True

			return True
		else:
			# If the hashes of user entered password and the original password matches, then we return False

			return False

	def encrypt(self):
		""" This method / function serves the feature of encrypting the contents of the image file. This function reads the filename location input stored in the class variable self.filename. """

		# Reading the contents of the image file specified by the user
		contents = open(self.filename, 'rb').read()
		contents = b64encode(contents).decode()

		# Generating the encryption key
		key = self.generatekey()

		# Converting the plain text to cipher text
		text = ''
		for character in contents:
			# Iterating through each character

			text += chr((ord(character) + key) % 256)

		# Changing the encoding of the content to base64 format
		text = b64encode(text.encode()).decode()

		# Adding the password to the contents of the image file
		text = hashlib.md5(self.password.encode()).hexdigest() + '\n' + text

		# Saving the encrypted content back to the file
		open(self.filename, 'wb').write(text.encode())

		# Deleting some of the variables declared within this function
		del text, key, contents

		# Returning 0 code (It will indicate that the function executed in success)
		return 0

	def decrypt(self):
		""" This method / function serves the feature of decrypting the contents of the image file. This function reads the filename location input stored in the class variable self.filename. """

		# Validating the password before decrypting
		if self.checkpassword():
			# If the password matches, then we continue

			# Reading the contents of the image file specified by the user
			contents = open(self.filename, 'rb').read()

			# Removing the password part from the file
			contents = contents.decode()
			contents = ' '.join(contents.split('\n')[1:])

			# Converting the base64 format text to plain text
			contents = b64decode(contents.encode()).decode()

			# Generating the encryption key
			key = self.generatekey()

			# Converting the cipher text to plain text
			text = ''
			for character in contents:
				# Iterating through each character

				text += chr((ord(character) - key) % 256)

			# Converting the contents to image file content type
			text = text.encode()
			text = decodebytes(text)

			# Saving the decrypted content back to the image file
			open(self.filename, 'wb').write(text)

			# Deleting some of the variables declared within this function
			del text, key, contents

			# Returning 0 code (It will indicate that the function executed in success)
			return 0
		else:
			# If the password does not matches, then we display the error message on the console screen

			print(f'[ Incorrect password ]')
			return 403

class VideoEncrypter:
	""" """

	def __init__(self):
		pass

	def generatekey(self):
		pass

	def checkpassword(self):
		pass

	def encrypt(self):
		pass

	def decrypt(self):
		pass

class DirectoryEncrypter:
	""" """

	def __init__(self, directory = None, password = None, arguments = None):
		self.directory = directory
		self.password = password

	def generatekey(self):
		""" This method / function serves the purpose of generating a special key for the encryption and decryption using the user entered password. This function reads the encryption password value from the class variable self.password.

		This function returns the int format key back after the generation. """

		# Generating the key from the encryption using the user entered password for encryption / decryption
		key = 0
		isEven = True

		for i in self.password:
			# Iterating over each character in the encrypted key entered by the user
				
			if isEven:
				# If the current iteration is even number, then we add the char code value

				key += ord(i)
			else:
				# If the current iteration is odd number (not even), then we subtract the char code value

				key -= ord(i)
		del isEven

		# Making the key possitive
		if key < 0:
			# If the key value is less than 0, then we change the negative sign to possitive by simply multiplying it with -1

			key *= (-1)

		# Adding the length of the password to itself
		key += len(self.password)

		# Returning the generating key
		return key

	def config(self, display = False):
		"""
		This method / function serves the functionability of checking the config file and loading all the details of the config file into the class object. This function reads the .encryption_config file at the specified folder and loads the details into class variables like

		self.password_hash			-> stores the password hash
		self.ignorefiles   			-> stores the list of files to be ignored during the encryption / decryption
		self.originalfilenames      -> stores the list of original names of the file before encryption
		self.created_on             -> stores the timestamp when the first encryption was applied on this directory
		self.last_modified           -> stores the timestamp when the encryption / decryption was executed latest
		
		The .encryption_config is a JSON file. The structure of the .encryption_config file is given below.
		{
			"password" : "...",
			"ignorefiles" : [],
			"originalfilenames" : [],
			"created_on" : ...,
			"last_modified" : ...,
		}

		This function also takes one argument 'display'. This display argument determines whether to print the config information on the console screen. If the display argument is marked true, then the config information is printed on the console screen, else nothing happens. The display argument is by default False.
		"""

		# Fetching the contents of the .encryption_config file
		# ----
		# Checking whether the config file exists or not in the user specified directory
		if path.isfile(self.directory + '.encryption_config'):
			# If the config file exist in the user specified directory, then we continue for further checking

			# Reading the contents of the config file
			contents = loads(open(f'{self.directory}.encryption_config', 'rb').open())
			contents = b64decode(contents).decode()

			# Setting the information extracted from the config file to the class variables
			self.password_hash = contents["password"]
			self.ignorefiles = contents["ignorefiles"]
			self.originalfilenames = contents["originalfilenames"]
			self.created_on = contents["created_on"]
			self.last_modified = contents["last_modified"]

			# Validating the information extracted
			if type(self.password_hash) == str and len(self.password_hash) > 5:
				# If the hash of the password is of proper length, then we continue

				pass
			else:
				# If the hash of the password is not of proper length, then we display the error message on the console screen

				print(f'password hash is invalid in the config file.')
				return 0

			if type(self.ignorefiles) == list:
				# If the data type of the ignorefiles parameter is of a list, then we continue

				pass
			else:
				# If the data type of the ignorefiles parameter is not a list, then we display the error message on the console screen

				print(f'ignorefiles is invalid in the config file. Required to be a list / array.')
				return 0

			if type(self.originalfilenames) == list:
				# If the data type of the originalfilenames parameter is of a list, then we continue

				pass
			else:
				# If the data type of the originalfilenames parameter is not a list, then we display the error message on the console screen

				print(f'originalfilenames is invalid in the config file. Required to be a list / array.')
				return 0

			if type(self.created_on) == float or type(self.created_on) == int:
				# If the data type of the created_on parameter is either int or float, then we continue

				self.created_on = datetime.fromtimestamp(self.created_on).ctime()
			else:
				# If the data type of the created_on parameter is neither int nor float, then we display the error message on the console screen

				print(f'created_on is invalid. Required to be a timestamp.')

			if type(self.last_modified) == float or type(self.last_modified) == int:
				# If the data type of the last_modified parameter is either int or float, then we continue

				if self.last_modified == 0.0:
					# If the last_modified parameter is 0.0 i.e., it is not defined, then we define the self.last_modified variable as an empty string

					self.last_modified = ''
				else:
					# If the last_modified parameter is not 0.0, then we continue to store the ctime value in the self.last_modified class variable

					self.last_modified = datetime.fromtimestamp(self.last_modified).ctime()
			else:
				# If the data type of the last_modified parameter is neither int or float, then we display the error message on the console screen

				print(f'last_modified is invalid. Required to be a timestamp.')
		else:
			# If the config file does not exists in the user specified directory, then we display the error message on the console screen

			print(f'config file not found in the specified directory "{self.directory}".')
			return 0
		# ----

		# Displaying the configs on the console screen
		# ----
		# Checking the display argument passed to this function
		if display:
			# If the display argument is marked true, then we continue to display the config information

			print(f'\nConfig for encryption on this directory ({self.directory}) : ')
			print('[#] Files to ignore : ')
			for i in self.ignorefiles:
				print(i, end = ', ')
			print('[#] Original filenames : ')
			for i in self.originalfilenames:
				print(f'{i["original_name"]} -> {i["encrypted_name"]}', end = ', ')
			print(f'[#] Created on : {self.created_on}')
			print(f'[#] Last modified : {self.last_modified}')
		# ----

	def check(self, password = False, overall = False):
		""" This method / function serves the functionalibility of checking the password and other required details of the directory. This function gets the value of the password from the class variable self.password. """

		# Running the config method in order to extract the information stored in the .encryption_config file
		self.config()

		# Checking for the task to be done (using the arguments specified for this function)
		if password:
			# If the password argument is marked true, then we continue to check for the password verification

			# Checking the password specified by the user against the hash of the password stored in the config file
			if type(self.password) == str:
				# If the password specified by the user is of str type, then we continue

				if hashlib.md5(self.password.encode()).hexdigest() == self.password_hash:
					# If the hash of the password specified by the user matches with the original password hash, then we return True

					return True
				else:
					# If the hash of the password specified by the user does not matches with the original password hash, then we return False

					return False
			else:
				# If the password specified by the user is not of str type, then we raise an error with a custom message

				raise TypeError('Password is invalid. Password specified by the user should be a string.')
		elif overall:
			# If the overall argument is marked true, then we continue to check for the overall config information verification

			# Checking for the password by matching the hashes
			if type(self.password) == str:
				# If the password specified by the user is of str type, then we continue

				if hashlib.md5(self.password.encode()).hexdigest() == self.password_hash:
					# If the hash of the password specified by the user matches with the original password hash, then we pass

					pass
				else:
					# If the hash of the password specified by the user does not matches with the original password hash, then we return False

					return False
			else:
				# If the password specified by the user is not of str type, then we raise an error with a custom message

				raise TypeError('Password is invalid. Password specified by the user should be a string.')

			# Checking for the ignorefiles and originalfilenames fields in the config informatin
			if type(self.ignorefiles) == list and type(self.originalfilenames) == list:
				# If the data type of both the ignorefiles and originalfilenames are of list, then we pass

				pass
			else:
				# If the data type of either ignorefiles or originalfilenames is not list, then we return False

				return False

			# If the code execution reached upto here, then we return True as all the validation of the config information has been passed without any errors
			return True
		else:
			# If neither the password argument not the overall argument are marked true, then we pass

			pass

	def encrypt(self):
		""" This method / function serves the functionability of encrypting the files in the user specified directory. This function reads the directory location input from the class variable self.directory. The process of the encryption / the steps of encryption are listed below :
		1. Generate the encryption key
		2. Encrypt each files in the directory one by one.
		3. Rename the filenames with the encrypted version of filenames.
		4. Create the config file in the directory.

		Some points to be noted :
		1. Each file in the directory should be properly listed as per their extensions. For no extensions, it would be considered a text file (all source code files, config files, script files are included here). The binary files with different data inside them (executable files, etc) will not be encrypted by this function, they will be marked in the ignorefiles list.
		"""

		# Creating the class variables that are not defined before encryption
		self.ignorefiles = []
		self.originalfilenames = []
		self.created_on = datetime.now().timestamp()
		self.last_modified = 0.0

		# Generating the key for the encryption
		key = self.generatekey()

		# Getting the list of the files in the user specified directory
		files = listdir(self.directory)

		# Encrypting the contents of each file
		# ----
		for file in files:
			# Iterating over the list of the files

			if file.lower()[len(file)-4:] == '.jpg' or file.lower()[len(file)-4:] == '.png' or file.lower()[len(file)-5:] == '.jpeg' or file.lower()[len(file)-4:] == '.gif':
				# If the extension of the file states that the file is a type of image, then we continue to encrypt the image file

				pass
			elif file.lower()[len(file)-4:] == '.mp4' or file.lower()[len(file)-4:] == '.mkv' or file.lower()[len(file)-4:] == '.3gp':
				# If the extension of the file states that the file is a type of video, then we continue to encrypt the video file

				pass
			else:
				# If the extension of the file is not recognized, then we consider the file being just a text document or else and encrypt it in that way

				try:
					# Reading the contents of the file
					contents = open(self.directory + file, 'rb').read()
					contents = contents.decode()

					# Encrypting the contents of the file
					text = ''
					for character in contents:
						# Iterating through each character in the plain text

						text += chr((ord(character) + key) % 256)

					# Changing the encoding of the cipher text
					contents = b64encode(text.encode())

					# Saving the contents back to the file
					open(self.directory + file, 'wb').write(contents)

					# Renaming the file with a new encrypted name
					encryptedfilename = ''
					for character in file:
						# Iterating through each character in the file's original name

						encryptedfilename += chr((ord(character) + key) % 256)
					encryptedfilename = b64encode(encryptedfilename.encode()).decode()
					rename(self.directory + file, self.directory + encryptedfilename)

					# Adding the changed name and the original name in the self.originalnames list
					self.originalfilenames.append({
						"original_name" : file,
						"encrypted_name" : encryptedfilename,
					})

					# Deleting some of variables defined under this scope
					del contents, encryptedfilename
				except Exception as e:
					# If there are any errors encountered during the process, then we skip the current file from being encrypted

					self.ignorefiles.append(file)
					print(file, e)
					print(f'[!] Skipping {file}')
					continue
				else:
					# if there are no errors encountered during the process, then we display the 'encrypted' message on the console screen

					print(f'[$] {file} : encrypted')
		# ----

		# Creating the config file in the directory
		try:
			open(self.directory + '.encryption_config', 'w+').write(dumps({
				"password" : hashlib.md5(self.password.encode()).hexdigest(),
				"ignorefiles" : self.ignorefiles,
				"originalfilenames" : self.originalfilenames,
				"created_on" : self.created_on,
				"last_modified" : self.last_modified,
				}))
		except Exception as e:
			# If there are any errors encountered during the generation of the encryption config file, then we display the error message on the console screen

			print(f'[ Error : Failed to generate the config file at {self.directory}. {e} ]')
			return 0
		else:
			# If there are no errors encountered during the generation of the encryption config file, then we display the success message on the console screen

			print(f'[ Encryption config file created at {self.directory} ]')
			return 0

	def decrypt(self):
		pass