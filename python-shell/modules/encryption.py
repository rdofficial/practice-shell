"""
encryption.py - Python Shell

A module created for supplying the required functions to the shell application. The functions and classes defined in this module ease many tasks at the shell application, in general way they are used in executing the task assigned by the user via the commands. This module contains functions and classes related to directory handling and other such stuff.

Author : Rishav Das (https://github.com/rdofficial/)
Created on : June 13, 2021

Last modified by : Rishav Das (https://github.com/rdofficial/)
Last modified on : June 24, 2021

Changes made in the last modification :
1. In the 'Hash' class, added the code for the verify() method. Now, it verifies even if the user didnt specified the hashing algorithm.
2. The extent would be only for the hashing algorithms supported by our Hash class.

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
	"""
	This class serves the funcionality of encryption / decryption of user specified directory. The process of encryption is done using the user specified password. The same password which was used for encryption is used for decryption as well. The encryption algorithm used by this class is close to same as other encryption classes defined in this module file.

	The encryption process here is a bit long and more organised. Each files of the user specified directory are encrypted one by one. Also, there are options for ignoring specific files during the encryption / decryption. The structure and information related to the encryption of a directory are stored in a config file in the user specified directory. The file is named '.encryption_config'.

	The structure of the config file is shown below.
	{
		"password" : "...",
		"ignorefiles" : [],
		"created_on" : ...,
		"last_modified" : ...,
	}

	The config file stores the password hash, thus when the user decrypts the directory, the password verification process is done. The user entered password is verified against the original password hash stored in the config file. There are also information stored there like, date of creation, last modfiied, etc.

	The class object when created, some of the information are required to be entered by the user. There are two ways of entering the information by the user. The ways are listed below.

	1. Via argument tokens

		In this mode,
		The argument tokens entered by the user at the shell (command line) are passed to this class object at the 'arguments' parameters. The syntax is shown below.

		DirectoryEncrypter(arguments = [<argument-list>])

		The arguments that are recognized by this class / tool are listed below.
		--password            Used to specify the password for the encryption / decryption
		--directory           Used to specify the directory for the encryption / decryption
		--task                Used to specify whether to encrypt / decrypt
		--ignore              Used to launch the ignore files mode (the user can mention the files to ignore)
		--help                Used to launch the documentation mode (the help section is displayed on the console screen)

		If there are any whitespaces in the inputs, then use the backslash (\). Below are some examples for the usage of this tool.

		# Command for encryption of a directory with password 'somehardpassword123'
		encrypt directory --directory /location/to/directory --password somehardpassword123 --task encrypt

		# Command for decryption of a directory with password 'somehardpassword123'
		encrypt directory --directory /location/to/directory --password somehardpassword123 --task decrypt

		# Command for encryption of a directory + ignoring some specific files
		encrypt directory --directory /location/to/directory --password somehardpassword123 --task encrypt --ignore

		# Command for displaying the help section for the tool
		encrypt directory --help

	2. Directly passing parameters

		In this mode,
		The parameters are passed directly into the class object. The syntax for the usage is listed below.

		DirectoryEncrypter(
			directory = '/location/to/directory',
			password = '<password>',
		)

		There are two parameters to be specified when launching the class object / declaring the class object. The parameters are : directory, password.
		The 'directory' parameter is used to specify the location of the directory which is needed to be encrypted / decrypted.
		The 'password' parameter is used to specify the password for the encryption / decryption.

		Further processes are listed below in the form of examples.

		# Declaring the class object
		enc = DirectoryEncrypter(directory = '/location/to/directory', password = 'somehardpassword123')

		# Specifying the ignorefiles (The files to be ignored while encryption / decryption)
		enc.ignorefiles = ['filename1.txt', 'filename2.docx', 'filename3.jpeg']

		# Encrypting the directory
		enc.encrypt()

		# Checking the password before decryption
		enc.check(password = True)

		# Checking the complete configuration of the encrypted directory before decrypting
		enc.check(all = True)

		# Decrypting the encrypted directory
		enc.decrypt()

	Some of the points to be noted about this class are listed below :
	* The sub-folders in the specified directory are skipped, just the files are encrypted.

	* The complete process of encryption and decryption might have some flaws. There might occur some errors related to key generation, discontinuity, etc, that could lead to serious loss of the data.

	* Security is not ensured by us. If there are situations like the data is completly corrupted during the process, then the authors are not responsible for the loss of the data. The authors are responsible for the bugs, not the mistakes commited by the users / clients. Thus, use this tool / class object safely and with your own risk.

	* For any bugs and errors, kindly create an issue on the github mirror of this repository or contact the author of this module file (Contact address / email addres listed at the top of the document).

	CUSTOM CONFIG

	This class also accepts custom configuration from the user. Using the --use-config flag while launching the command for this, we command this tool to use a custom config file that too is specified by the user. Before encryption / decryption, we then ask the user for entering custom config in two different ways. The ways are listed below.
	1. .encryption_config at the directory

		In this mode, if there exists a file named '.encryption_config' already present in the user specified directory. Then, the tool loads the config file information from that file only. If the user wants to load information from any other way then there must not exists any file in that directory. This file is loaded in the same way the default config file is loaded in this tool (class object).

	2. Custom config file location

		In this mode, the user is asked to enter the file location which directs the tool to a file which contains the contents of the configuration of the encrypted directory. The file that the user will specify should have proper read permissions and the contents should be valid.

	3. Custom config hash

		In this mode, the user is asked to enter the hash code of the config file. Entering the complete string will be used to extract the configuration of the encrypted directory. The hash code looks something like this, as shown below.

		eyJwYXNzd29yZCI6ICJiOGU5NDZlNmY2NWU3M2Q1MDlkMzlkNzBkOTYzZWNlMyIsICJpZ25vcmVmaWxlcyI6IFsidGVzdDEucG5nIiwgInRlc3QzLmJmIiwgInRlc3QyLnR4dCIsICJ0ZXN0NC5weSJdLCAiY3JlYXRlZF9vbiI6IDE2MjQzMzIxNDMuMDcyNTMzLCAibGFzdF9tb2RpZmllZCI6IDAuMH0=

	This custom config feature might be a little different and odd, below are some points that will explain how it makes a difference.
	1. Even if we specify a custom config file, we still have to specify the password for encryption and decryption.
	2. The configuration for an encrypted directory stores other properties like ignorefiles, etc. The ignorefiles property is a list of files that are to be ignored during the encryption and decryption process.
	"""

	def __init__(self, directory = None, password = None, useconfig = False, arguments = None):
		# Checking if arguments provided or just the parameters directly
		if arguments == None:
			# If the arguments are not passed to this function by the user, then we continue to use the default provided values

			self.directory = directory
			self.password = password
			self.useconfig = useconfig
		else:
			# If the arguments are passed to this function by the user, then we continue to parse the arguments

			# Parsing the arguments entered to this function
			# ----
			# Setting the default value of the variables to None
			self.directory = None
			self.password = None
			self.ignore = False
			self.useconfig = False
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

				if argument == '--directory':
					# If the argument is for specifying the directory for encryption, then we continue to parse the next argument as the entered value

					try:
						self.directory = arguments[index + 1]
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

				if argument == '--ignore':
					# If the argument is for specifying the ignore flag, then we continue to mark the ignore mode to true in order to ask the user for the files to be ignored

					self.ignore = True

				if argument == '--use-config':
					# If the argument is for specifying the use-config flag, then we continue to mark the useconfig mode to true in order to further fetch the information from the configuration file

					self.useconfig = True

				if argument == '--help':
					# If the argument is for specifying the help, then we continue to mark the documentation mode to be true

					self.documentation = True
			# ----

			# Checking whether the task is to be in documentation mode or execution mode
			if self.documentation:
				# If the user specified the documentation mode, then we continue to display the help text on the console screen

				print('encrypt directory\nUsage : encrypt <arguments>\n\n"encrypt directory" is a tool which serves the functionality of encryption / decryption of user specified directories. This tool encrypts an entire directory with a password. There are also features like ignoring certain files while encryption / decryption process. All such properties of the encryption are stored in the config file (.encryption_config). This file is necessary for the proper decryption of an already encrytped directory.\n\nArguments are :\n--password            Used to specify the password for encryption / decryption\n--directory  Used to specify the directory for encryption / decryption\n--task  Used to specify whether to encrypt / decrypt\n--ignore \t\t\t  Used to specify certain files to ignore when encrypting\n--use-config  Used to specify a custom config for the encryption / decryption\n--help(\t\t\t  Used to display this help te\n\nPoints to be noted :\n1. The sub-folders in the specified directory are skipped, just the files are encrypted.\n2. The complete process of encryption and decryption might have some flaws. There might occur some errors related to key generation, discontinuity, etc, that could lead to serious loss of the data.\n3. Security is not ensured by us. If there are situations like the data is completly corrupted during the process, then the authors are not responsible for the loss of the data. The authors are responsible for the bugs, not the mistakes commited by the users / clients. Thus, use this tool / class object safely and with your own risk.s\n\nCheck out the docs for more info.')
			else:
				# If the user specified the execution mode, then we continue to execute the task

				# Validating the user entered directory location
				# ----
				# Checking the directory location input type
				if type(self.directory) == str:
					# If the directory's value as per entered by the user is a string type variable, then we continue for further validation

					# Checking whether the directory exists or not
					if path.isdir(self.directory):
						# If the user specified directory exists in the local machine, then we continue for further validation

						# Adding a / at the end of the directory location (path) if not present
						if self.directory[len(self.directory)-1] != '/':
							# If the '/' is not present at the end of the directory location (path), then we continue to add it

							self.directory += '/'
					else:
						# If the user specified directory does not exists in the local machine, then we raise an error with a custom message

						raise ValueError(f'No such directory found "{self.directory}".')
				else:
					# If the user entered directory's value is a non string variable, then we raise an error with a custom message

					raise SyntaxError('Directory input is invalid. Requires to be an alphanumeric string.')
				# ----

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

					# Creating the class variable self.ignorefiles before starting the process of the encryption
					self.ignorefiles = []

					# Checking for the ignore and config flag
					# ----
					if self.useconfig:
						# If the useconfig flag is marked true, then we continue to fetch the custom config file

						# Launching the customconfigloader() method in order to fetch for the custom config file
						self.customconfigloader()
					elif self.ignore:
						# If the ignore flag is marked true, then we continue to ask the user for the files for ignoring

						files = input('\nEnter the files to be ignored during the encryption (seperate with ;)\n> ')
						files = files.split(';')

						# Inserting all the files into the ignorefiles list after validating each one of them
						for file in files:
							# Iterating through each file specified by the user

							if path.isfile(self.directory + file):
								# If the currently iterated file does exists, then we continue to append it to the ignorefiles list

								self.ignorefiles.append(file)
							else:
								# If the currently iterated file does not exists, then we skip it after displaying the not found message on the console screen

								print(f'[!] File skipped (not added to ignore list), not found : {file}')
								continue
						del files
					# ----

					# Launching the encrypt() method in order to start the encryption process
					if self.encrypt() == 0:
						# If the encrypt() method returns 0, it means that the encryption proces is completed and thus we display the message on the console screen

						print(f'\n[$] Encryption process completed')
					else:
						# If the encrypt() method does not returns 0, it means there are some errors in the encryption process and thus we display the message on the console screen

						print(f'\n[!] Encryption process might have encountered some errors, please check the directory for finding them out.')
				elif self.task.lower() == 'decrypt' or self.task.lower() == 'decryption':
					# If the task specified is for decryption, then we continue to decrypt

					# Checking for the config flag
					# ----
					if self.useconfig:
						# If the useconfig flag is marked true, then we continue to fetch the custom config file

						# Launching the customconfigloader() method in order to fetch for the custom config file
						self.ignore = False  # Marking the ignore flag as True in order to avoid any errors
						self.customconfigloader()
					# ----

					# Launching the decrypt() method in order to start the decryption process
					if self.decrypt() == 0:
						# If the decrypt() method returns 0, it means that the decryption proces is completed and thus we display the message on the console screen

						print(f'\n[$] Decryption process completed')
					else:
						# If the decrypt() method does not returns 0, it means there are some errors in the decryption process and thus we display the message on the console screen

						print(f'\n[!] Decryption process might have encountered some errors, please check the directory for finding them out.')
				else:
					# If the task specified is not recognized, then we raise an error with a custom message

					raise ReferenceError('Task not recognized. Encrypt / decrypt are the two recognizable terms.')
				del self.task

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
		This method / function serves the funcionality of checking the config file and loading all the details of the config file into the class object. This function reads the .encryption_config file at the specified folder and loads the details into class variables like

		self.password_hash			-> stores the password hash
		self.ignorefiles   			-> stores the list of files to be ignored during the encryption / decryption
		self.created_on             -> stores the timestamp when the first encryption was applied on this directory
		self.last_modified           -> stores the timestamp when the encryption / decryption was executed latest
		
		The .encryption_config is a JSON file. The structure of the .encryption_config file is given below.
		{
			"password" : "...",
			"ignorefiles" : [],
			"created_on" : ...,
			"last_modified" : ...,
		}

		This function also takes one argument 'display'. This display argument determines whether to print the config information on the console screen. If the display argument is marked true, then the config information is printed on the console screen, else nothing happens. The display argument is by default False.
		"""

		# Fetching the contents of the .encryption_config file
		# ----
		# Checking whether the config file exists or not in the user specified directory
		if self.useconfig:
			# If the useconfig flag is marked true, then it means the user requested to load a custom config file, and we skip it

			pass
		elif path.isfile(self.directory + '.encryption_config'):
			# If the config file exist in the user specified directory, then we continue for further checking

			# Reading the contents of the config file
			contents = open(f'{self.directory}.encryption_config', 'rb').read()
			contents = b64decode(contents).decode()
			contents = loads(contents)

			# Setting the information extracted from the config file to the class variables
			self.password_hash = contents["password"]
			self.ignorefiles = contents["ignorefiles"]
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

			if type(self.created_on) == float or type(self.created_on) == int:
				# If the data type of the created_on parameter is either int or float, then we continue

				self.created_on = datetime.fromtimestamp(self.created_on).ctime()
			else:
				# If the data type of the created_on parameter is neither int nor float, then we display the error message on the console screen

				print(f'created_on is invalid. Required to be a timestamp.')
				return 0

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
				return 0
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
		""" This method / function serves the funcionality of checking the password and other required details of the directory. This function gets the value of the password from the class variable self.password. """

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
			if type(self.ignorefiles) == list:
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
		""" This method / function serves the funcionality of encrypting the files in the user specified directory. This function reads the directory location input from the class variable self.directory. The process of the encryption / the steps of encryption are listed below :
		1. Generate the encryption key.
		2. Encrypt each files in the directory one by one.
		3. Rename the filenames with the encrypted version of filenames.
		4. Create the config file in the directory.
		"""

		# Printing the encryption message on the console screen
		print(f'\n[ Encrypting {self.directory} ]\n')

		# Creating the class variables that are not defined before encryption
		self.created_on = datetime.now().timestamp()
		self.last_modified = 0.0

		# Generating the key for the encryption
		key = self.generatekey()

		# Getting the list of the files in the user specified directory
		files = listdir(self.directory)

		# Checking whether the encryption config file is already present in the user specified directory or not
		if '.encryption_config' in files:
			# If the encryption_config is already present in the directory, then we continue to ask the user whether to parse information from the config file or not

			choice = input('A config file is already present at {self.directory}. Should we parse information from it? (y/n) : ')
			if choice.lower() == 'y' or choice.lower() == 'yes':
				# If the user choosed the option for loading the information from the existsing config file, then we continue

				# Reading the contents of the encryption config
				contents = open(self.directory + '.encryption_config', 'rb').read()
				contents = b64decode(contents).decode()
				contents = loads(contents)

				# Setting the information extracted from the config file to the class variables
				self.password_hash = contents["password"]
				self.created_on = contents["created_on"]
				self.last_modified = contents["last_modified"]
				
				# Adding the ignorefiles item from the config file to class variable list
				for file in contents["ignorefiles"]:
					if file not in self.ignorefiles:
						# If the file is not already listed on the ignorefiles list, then we continue to append it

						self.ignorefiles.append(contents["ignorefiles"])

				# Checking the user entered password against the password hash extracted from the config file
				if hashlib.md5(self.password.encode()).hexdigest() == self.password_hash:
					# If the user entered password matches with the original password hash, then we continue

					pass
				else:
					# If the user entered password does not matches with the original password hash, then we display the warning to the user about the password discontinuity

					print(f'[!] Password match failed with the original password hash')
					return 1
			else:
				# If the user choosed the option for skipping the loading process, then we continue to delete the config file present at the directory

				remove(self.directory + '.encryption_config')
			del choice

		# Encrypting the contents of each file
		# ----
		for file in files:
			# Iterating over the list of the files

			try:
				# Ignoring the file if marked in the ignorefiles list
				if file in self.ignorefiles:
					# If the file is marked at the ignore file list, then we skip the encryption part for the currently iterated file

					print(f'[#] Ignored : {file}')
					continue

				# Reading the contents of the file
				contents = open(self.directory + file, 'rb').read()
				contents = b64encode(contents).decode()

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

				# Deleting some of variables defined under this scope
				del contents, encryptedfilename
			except Exception as e:
				# If there are any errors encountered during the process, then we skip the current image file from being encrypted

				self.ignorefiles.append(file)
				print(f'[!] Skipping : {file}')
				continue
			else:
				# if there are no errors encountered during the process, then we display the 'encrypted' message on the console screen

				print(f'[$] Encrypted : {file}')
		# ----

		# Creating the config file in the directory
		try:
			open(self.directory + '.encryption_config', 'wb').write(b64encode(dumps({
				"password" : hashlib.md5(self.password.encode()).hexdigest(),
				"ignorefiles" : self.ignorefiles,
				"created_on" : self.created_on,
				"last_modified" : self.last_modified,
				}).encode()))
		except Exception as e:
			# If there are any errors encountered during the generation of the encryption config file, then we display the error message on the console screen

			print(f'[ Error : Failed to generate the config file at {self.directory}. {e} ]')
			return 0
		else:
			# If there are no errors encountered during the generation of the encryption config file, then we display the success message on the console screen

			print(f'[ Encryption config file created at {self.directory} ]')
			return 0

	def decrypt(self):
		""" This method / function serves the funcionality of decrypting the files in the user specified directory. This function reads the directory location input from the class variable self.directory. The process of the decryption / the steps of decryption are listed below :
		1. Check the password specified by the user against the original password hash.
		2. Generate the decryption key.
		3. Decrypt all the files except the ones which are listed in the ignorefiles list.
		4. Delete the .encryption_config file present in the user specified directory.
		"""

		# Printing the decryption message on the console screen
		print(f'\n[ Decrypting {self.directory} ]\n')

		# Launching the check() method in order to read the config file as well as check the password as well
		if self.check(overall = True):
			# If the check() methods returns True, then we continue

			pass
		else:
			# If the check() method returns False, then we assume password error or config file error, we display the error message on the console screen

			print(f'[ Error : Either incorrect password or errors in the config file. ]')
			return 1

		# Generating the key for the encryption
		key = self.generatekey()

		# Getting the list of the files in the user specified directory
		files = listdir(self.directory)

		# Removing the config file from the list (ignoring it by default)
		files.remove('.encryption_config')

		# Decrypting the contents of each file
		# ----
		for file in files:
			# Iterating over the list of files

			try:
				# Checking whether the file is mentioned in the ignorefiles list or not
				if file in self.ignorefiles:
					# If the currently iterated file is mentioned in the ignorefiles list, then we skip the current iteration

					print(f'[#] Ignored : {file}')

				# Decrypting the file names
				filename = b64decode(file.encode()).decode()
				decryptedfilename = ''
				for character in filename:
					# Iterating over each characters in the filename

					decryptedfilename += chr((ord(character) - key) % 256)

				# Renaming the currently iterated file with their decrypted version
				rename(self.directory + file, self.directory + decryptedfilename)
				file = decryptedfilename

				# Reading the contents of the file
				contents = open(self.directory + file, 'rb').read()
				contents = b64decode(contents).decode()

				# Converting the contents of the file from cipher code to plain text
				text = ''
				for character in contents:
					# Iterating over each character in the file contents

					text += chr((ord(character) - key) % 256)

				# Saving the contents back to the file
				contents = decodebytes(text.encode())
				open(self.directory + file, 'wb').write(contents)

				# Deleting the variables declared under this scope
				del filename, decryptedfilename, contents, text
			except Exception as e:
				# If there are any errors encountered during the process, then we skip the current image file from being decrypted

				print(f'[!] Skipping : {file}')
				continue
			else:
				# if there are no errors encountered during the process, then we display the 'decrypted' message on the console screen

				print(f'[$] Decrypted : {file}')
		# ----

		# Removing the config file from the directory after confirming from the user
		choice = input('\nRemove the config file? (y/n) : ')
		if choice.lower() == 'yes' or choice.lower() == 'y':
			# If the user entered the choice to delete the config file at the directory, then we continue to do so

			remove(self.directory + '.encryption_config')
			print(f'[$] Removed config file')
			del choice
			return 0
		else:
			# If the user entered the choice to not delete the config file at the directory, then we skip the process

			del choice
			return 0

	def customconfigloader(self):
		"""
		This method / function serves the functionality of fetching the information of encryption config file for encryption / decryption of a directory. This function loads many information from the class variables like self.directory, etc. Some additional information is attached below. 

		This class also accepts custom configuration from the user. Using the --use-config flag while launching the command for this, we command this tool to use a custom config file that too is specified by the user. Before encryption / decryption, we then ask the user for entering custom config in two different ways. The ways are listed below.
		1. .encryption_config at the directory

			In this mode, if there exists a file named '.encryption_config' already present in the user specified directory. Then, the tool loads the config file information from that file only. If the user wants to load information from any other way then there must not exists any file in that directory. This file is loaded in the same way the default config file is loaded in this tool (class object).

		2. Custom config file location

			In this mode, the user is asked to enter the file location which directs the tool to a file which contains the contents of the configuration of the encrypted directory. The file that the user will specify should have proper read permissions and the contents should be valid.

		3. Custom config hash

			In this mode, the user is asked to enter the hash code of the config file. Entering the complete string will be used to extract the configuration of the encrypted directory. The hash code looks something like this, as shown below.

			eyJwYXNzd29yZCI6ICJiOGU5NDZlNmY2NWU3M2Q1MDlkMzlkNzBkOTYzZWNlMyIsICJpZ25vcmVmaWxlcyI6IFsidGVzdDEucG5nIiwgInRlc3QzLmJmIiwgInRlc3QyLnR4dCIsICJ0ZXN0NC5weSJdLCAiY3JlYXRlZF9vbiI6IDE2MjQzMzIxNDMuMDcyNTMzLCAibGFzdF9tb2RpZmllZCI6IDAuMH0=

		This custom config feature might be a little different and odd, below are some points that will explain how it makes a difference.
		1. Even if we specify a custom config file, we still have to specify the password for encryption and decryption.
		2. The configuration for an encrypted directory stores other properties like ignorefiles, etc. The ignorefiles property is a list of files that are to be ignored during the encryption and decryption process.
		"""

		# Checking whether the '.encryption_config' file is present at the user specified directory
		if '.encryption_config' in listdir(self.directory):
			# If a config file is already present at the user specified directory, then we continue to fetch for it

			try:
				# Reading the .encryption_config file present at the user specified directory
				print(f'[$] Config file found at {self.directory}')
				contents = open(self.directory + '.encryption_config', 'rb').read()
				contents = decodebytes(contents).decode()
				contents = loads(contents)

				# Filtering out the information from the contents
				self.password_hash = contents["password"]
				self.ignorefiles = contents["ignorefiles"]
				del contents
			except Exception as e:
				# If there are any errors during the extraction of information from the config file, then we continue to skip it and do manuall information entry from the user

				# Displaying the error message on the console screen
				print(f'[!] Failed to parse the config file at {self.directory}')

				# Checking if the ignore flag is marked true or not
				if self.ignore:
					# If the ignore flag is marked true, then we continue to ask the user for specifying the files to be ignored during the encryption / decryption

					# Asking the user to enter the files that are to be ignored during the encryption / decryption process
					files = input('\nEnter the files to be ignored during the encryption (seperate with ;)\n> ')
					files = files.split(';')

					# Inserting all the files into the ignorefiles list after validating each one of them
					for file in files:
						# Iterating through each file specified by the user

						if path.isfile(self.directory + file):
							# If the currently iterated file does exists, then we continue to append it to the ignorefiles list

							self.ignorefiles.append(file)
						else:
							# If the currently iterated file does not exists, then we skip it after displaying the not found message on the console screen

							print(f'[!] File skipped (not added to ignore list), not found : {file}')
							continue
					del files
			else:
				# If there are no errors encounted during the process, then we continue further with the fetched information from the config file

				# Matching the user entered password from the original password hash
				if hashlib.md5(self.password.encode()).hexdigest() == self.password_hash:
					# If the user entered password matches with the original password hash, then we continue to validate the ignorefiles list

					if type(self.ignorefiles) == list:
						# If the data type of the ignorefiles class variable is list, then we continue

						return 0
					else:
						# If the data type of the ignorefiles class variable is not a list, then we raise an error with a custom message

						raise TypeError(f'The ignorefiles list is invalid in the config file at {self.directory}.')
				else:
					# If the user entered password does not matches with the original password hash, then we raise an error with a custom message

					raise ValueError(f'Failed to match the entered password against the password hash in the config file at {self.directory}.')
		else:
			# If there are no config files found at the user specified directory, then we continue to ask the user for the config file manually

			# Asking the user for the choice whether to enter the config file hash code or enter the file location for a config file that is to be used by this tool
			choice = input(f'\n[!] Config file not found at {self.directory}\nChoose :\n1. Enter location for another config file\n2. Enter the config hash code manually\nEnter your choice : ')

			# Checking the option choosed by the user
			if choice == '1':
				# If the user choosed the option for entering the location of another config file manually, then we continue to ask the user for the file location

				choice = input('Enter the config file location : ')
				if path.isfile(choice):
					# If the file location specified by the user exists on the local machine, then we continue to fetch information out of it

					try:
						# Reading the .encryption_config file present at the user specified directory
						contents = open(choice, 'rb').read()
						contents = decodebytes(contents).decode()
						contents = loads(contents)

						# Filtering out the information from the contents
						self.password_hash = contents["password"]
						self.ignorefiles = contents["ignorefiles"]
					except Exception as e:
						# If there are any errors during the extraction of information from the config file, then we continue to skip it and do manuall information entry from the user

						# Displaying the error message on the console screen
						print(f'[!] Failed to parse the config file "{choice}"')

						# Checking if the ignore flag is marked true or not
						if self.ignore:
							# If the ignore flag is marked true, then we continue to ask the user for specifying the files to be ignored during the encryption / decryption

							# Asking the user to enter the files that are to be ignored during the encryption / decryption process
							files = input('\nEnter the files to be ignored during the encryption (seperate with ;)\n> ')
							files = files.split(';')

							# Inserting all the files into the ignorefiles list after validating each one of them
							for file in files:
								# Iterating through each file specified by the user

								if path.isfile(self.directory + file):
									# If the currently iterated file does exists, then we continue to append it to the ignorefiles list

									self.ignorefiles.append(file)
								else:
									# If the currently iterated file does not exists, then we skip it after displaying the not found message on the console screen

									print(f'[!] File skipped (not added to ignore list), not found : {file}')
									continue
								del files
					else:
						# If there are no errors encounted during the process, then we continue further with the fetched information from the config file

						# Matching the user entered password from the original password hash
						if hashlib.md5(self.password.encode()).hexdigest() == self.password_hash:
							# If the user entered password matches with the original password hash, then we continue to validate the ignorefiles list

							if type(self.ignorefiles) == list:
								# If the data type of the ignorefiles class variable is list, then we continue

								return 0
							else:
								# If the data type of the ignorefiles class variable is not a list, then we raise an error with a custom message

								raise TypeError(f'The ignorefiles list is invalid in the config file at {self.directory}.')
						else:
							# If the user entered password does not matches with the original password hash, then we raise an error with a custom message

							raise ValueError(f'Failed to match the entered password against the password hash in the config file at {self.directory}.')
			elif choice == '2':
				# If the user choosed to enter the config file hash code, then we continue to ask the user to enter manually

				# Asking the user to enter the hash code of the config file
				choice = input('\nEnter the config file hash code : ')

				try:
					# Decoding the hash code to plain contents
					contents = decodebytes(choice.encode()).decode()
					contents = loads(contents)

					# Filtering out the information from the contents
					self.password_hash = contents["password"]
					self.ignorefiles = contents["ignorefiles"]
					del contents
				except Exception as e:
					# If there are any errors during the extraction of information from the config file, then we continue to skip it and do manuall information entry from the user

					# Displaying the error message on the console screen
					print(f'[!] Failed to parse the config file at {self.directory}')

					# Checking if the ignore flag is marked true or not
					if self.ignore:
						# If the ignore flag is marked true, then we continue to ask the user for specifying the files to be ignored during the encryption / decryption

						# Asking the user to enter the files that are to be ignored during the encryption / decryption process
						files = input('\nEnter the files to be ignored during the encryption (seperate with ;)\n> ')
						files = files.split(';')

						# Inserting all the files into the ignorefiles list after validating each one of them
						for file in files:
							# Iterating through each file specified by the user

							if path.isfile(self.directory + file):
								# If the currently iterated file does exists, then we continue to append it to the ignorefiles list

								self.ignorefiles.append(file)
							else:
								# If the currently iterated file does not exists, then we skip it after displaying the not found message on the console screen

								print(f'[!] File skipped (not added to ignore list), not found : {file}')
								continue
						del files
				else:
					# If there are no errors encounted during the process, then we continue further with the fetched information from the config file

					# Matching the user entered password from the original password hash
					if hashlib.md5(self.password.encode()).hexdigest() == self.password_hash:
						# If the user entered password matches with the original password hash, then we continue to validate the ignorefiles list

						if type(self.ignorefiles) == list:
							# If the data type of the ignorefiles class variable is list, then we continue

							return 0
						else:
							# If the data type of the ignorefiles class variable is not a list, then we raise an error with a custom message

							raise TypeError(f'The ignorefiles list is invalid in the config file at {self.directory}.')
					else:
						# If the user entered password does not matches with the original password hash, then we raise an error with a custom message

						raise ValueError(f'Failed to match the entered password against the password hash in the config file at {self.directory}.')
			else:
				# If the user entered an unrecognized option, then we raise an error with custom message

				raise ValueError('No such options recognized. Failed to fetch the custom config for the encryption directory.')

class Hash:
	""" """

	def __init__(self, text = None, algorithm = None, original = None, arguments = None):
		self.text = text
		self.algorithm = algorithm
		self.original = original

		# Setting some class properties
		self._algorithms_supported = [
			'md5',
			'sha1',
			'sha224',
			'sha256',
			'sha378',
			'sha512',
			'sha3_224',
			'sha3_256',
			'shake_128',
			'shake_256',
			'sha3_384',
			'sha3_512',
			'blake2b',
			'blake2s',
			'fuck',
		]

		if type(self.text) == str:
			self.text = self.text.encode()
		elif type(self.text) == bytes:
			pass
		else:
			raise TypeError('The input should be a string.')

	def make(self):
		""" This method / function serves the functionality of conversion of a plain string into hashed format using the specified algorithm. The values of the text, and algorithm are fetched from the class variables self.text, self.algorithm. """

		# Checking the algorithm as per specified by the user and then executing the proper algorithm
		if self.algorithm == 'md5':
			# If the user specified algorithm is md5, then we continue

			hash = hashlib.md5(self.text).hexdigest()
		elif self.algorithm == 'sha1':
			# If the user specified algorithm is sha1, then we continue

			hash = hashlib.sha1(self.text).hexdigest()
		elif self.algorithm == 'sha224':
			# If the user specified algorithm is sha224, then we continue

			hash = hashlib.sha224(self.text).hexdigest()
		elif self.algorithm == 'sha256':
			# If the user specified algoritm is sha256, then we continue

			hash = hashlib.sha256(self.text).hexdigest()
		elif self.algorithm == 'sha378':
			# If the user specified algorithm is sha378, then we continue

			hash = hashlib.sha256(self.text).hexdigest()
		elif self.algorithm == 'sha512':
			# If the user specified algorithm is sha512, then we continue

			hash = hashlib.sha256(self.text).hexdigest()
		elif self.algorithm == 'sha3_224':
			# If the user specified algorithm is sha3_224, we continue

			hash = hashlib.sha3_224(self.text).hexdigest()
		elif self.algorithm == 'sha3_256':
			# If the user specified algorithm is sha3_256, we continue

			hash = hashlib.sha3_256(self.text).hexdigest()
		elif self.algorithm == 'shake_128':
			# If the user specified algorithm is shake_128, we continue

			hash = hashlib.shake_128(self.text).hexdigest()
		elif self.algorithm == 'shake_256':
			# If the user specified algorithm is shake_256, we continue

			hash = hashlib.shake_256(self.text).hexdigest()
		elif self.algorithm == 'sha3_384':
			# If the user specified algorithm is sha3_384, we continue

			hash = hashlib.sha3_384(self.text).hexdigest()
		elif self.algorithm == 'sha3_512':
			# If the user specified algorithm is sha3_512, we continue

			hash = hashlib.sha3_512(self.text).hexdigest()
		elif self.algorithm == 'blake2b':
			# If the user specified algorithm is blake2b, we continue

			hash = hashlib.blake2b(self.text).hexdigest()
		elif self.algorithm == 'blake2s':
			# If the user specified algorithm is blake2s, we continue

			hash = hashlib.blake2s(self.text).hexdigest()
		elif self.algorithm == 'fuck':
			# If the user specified algorithm is fuck, we continue

			# CUSTOM ALGORITHM
			# NAME : fuck
			# ----
			# Generating an hash encryption key
			key = 0
			isEven = True
			self.text = self.text.decode()
			for i in self.text:
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

			# Adding the length of the text to itself
			key += len(self.text)

			# Creating the cipher text from the plain text
			text = ''
			for character in self.text:
				# Iterating through each character in the plain text

				text += chr((ord(character) + key) % 256)

			# Encoding into the base64 format
			text = b64encode(text.encode()).decode()

			# Making the 'fuck' string out of the semi encrypted text
			hash = ''
			for index, character in enumerate(text):
				# Iterating through each character in the text

				hash += f'fuck{ord(character)}'
				if index != len(text) - 1:
					hash += '-' 
			del text
			# ----

		# Finally after completing the process, we return the already formed hash back to the user
		print(f'[$] Hash : {hash}')  # Displaying the generated hash on the console screen
		return hash

	def verify(self):
		""" This method / function serves the functionality of verifying a plain with a hash. The plain string, the hashing algorithm and the original string is fetched from the class variables self.text, self.algorithm, self.original.

		If the hashing algorithm is specified by the user, then we just check for the specific hashing algorithm.
		Otherwise, this function checks for all the functions one by one and verifies the plain text with the original hash.

		This function can be used when we are verifying the user entered plain password against the hash of the password stored in the database. This is one of the implementation of this password in a Login System.
		"""

		# Checking the self.original class variable before executing any process further
		if self.original == None:
			# If the self.original variable is not defined / specified by the user, then we display the error message on the console screen

			print(f'[ Error : The original hash is not specified. ]')
			return 0
		else:
			# If the self.original class variable is defined, then we proceed for further validation

			if type(self.original) == str:
				# If the type of the variable self.original is string, then we continue for further validation

				if len(self.original) == 0:
					# If the length of the string stored in self.original variable is 0, then we display the error message on the console screen

					print(f'[ Error : The original hash specified is invalid. ]')
					return 0
				else:
					# If the length of the string stored in self.original variable is not 0, then we continue

					pass
			else:
				# If the type of the variable self.original is not string, then we display the error message on the console screen

				print(f'[ Error : The original hash specified is invalid. ]')
				return 0

		# Checking if the hashing algorithm is specified by the user or not
		if self.algorithm == None:
			# If the hashing algorithm is not specified by the user, then we continue to check with all available hashing algorithms

			# Checking for all the algorithms supported by his tool / class one by one
			# ----
			# Checking for the md5 hashing algorithm
			hash = hashlib.md5(self.text).hexdigest()
			if hash == self.original:
				# If the md5 hash of the plain text matches with the original hash, then we continue

				return True
			
			# Checking for the sha1 hashing algorithm
			hash = hashlib.sha1(self.text).hexdigest()
			if hash == self.original:
				# If the sha1 hash of the plain text matches with the original hash, then we continue

				return True

			# Checking for the sha224 hashing algorithm
			hash = hashlib.sha224(self.text).hexdigest()
			if hash == self.original:
				# If the sha224 hash of the plain text matches with the original hash, then we continue

				return True

			# Checking for the sha256 hashing algorithm
			hash = hashlib.sha256(self.text).hexdigest()
			if hash == self.original:
				# If the sha256 hash of the plain text matches with the original hash, then we continue

				return True

			# Checking for the sha378 hashing algorithm
			hash = hashlib.sha378(self.text).hexdigest()
			if hash == self.original:
				# If the sha378 hash of the plain text matches with the original hash, then we continue

				return True

			# Checking for the sha512 hashing algorithm
			hash = hashlib.sha512(self.text).hexdigest()
			if hash == self.original:
				# If the sha512 hash of the plain text matches with the original hash, then we continue

				return True

			# Checking for the sha3_224 hashing algorithm
			hash = hashlib.sha3_224(self.text).hexdigest()
			if hash == self.original:
				# If the sha3_224 hash of the plain text matches with the original hash, then we continue

				return True

			# Checking for the sha3_256 hashing algorithm
			hash = hashlib.sha3_256(self.text).hexdigest()
			if hash == self.original:
				# If the sha3_256 hash of the plain text matches with the original hash, then we continue

				return True

			# Checking for the sha3_384 hashing algorithm
			hash = hashlib.sha3_384(self.text).hexdigest()
			if hash == self.original:
				# If the sha3_384 hash of the plain text matches with the original hash, then we continue

				return True

			# Checking for the sha3_512 hashing algorithm
			hash = hashlib.sha3_512(self.text).hexdigest()
			if hash == self.original:
				# If the sha3_512 hash of the plain text matches with the original hash, then we continue

				return True

			# Checking for the shake_128 hashing algorithm
			hash = hashlib.shake_128(self.text).hexdigest()
			if hash == self.original:
				# If the shake_128 hash of the plain text matches with the original hash, then we continue

				return True

			# Checking for the shake_256 hashing algorithm
			hash = hashlib.shake_256(self.text).hexdigest()
			if hash == self.original:
				# If the shake_256 hash of the plain text matches with the original hash, then we continue

				return True

			# Checking for the blake2b hashing algorithm
			hash = hashlib.blake2b(self.text).hexdigest()
			if hash == self.original:
				# If the blake2b hash of the plain text matches with the original hash, then we continue

				return True

			# Checking for the blake2s hashing algorithm
			hash = hashlib.blake2s(self.text).hexdigest()
			if hash == self.original:
				# If the blake2s hash of the plain text matches with the original hash, then we continue

				return True

			# Checking for the fuck hashing algorithm
			# CUSTOM ALGORITHM
			# NAME : fuck
			# ----
			# Generating an hash encryption key
			key = 0
			isEven = True
			self.text = self.text.decode()
			for i in self.text:
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

			# Adding the length of the text to itself
			key += len(self.text)

			# Creating the cipher text from the plain text
			text = ''
			for character in self.text:
				# Iterating through each character in the plain text

				text += chr((ord(character) + key) % 256)

			# Encoding into the base64 format
			text = b64encode(text.encode()).decode()

			# Making the 'fuck' string out of the semi encrypted text
			hash = ''
			for index, character in enumerate(text):
				# Iterating through each character in the text

				hash += f'fuck{ord(character)}'
				if index != len(text) - 1:
					hash += '-' 
			del text
			# ----
			if hash == self.original:
				# If the fuck hash of the plain text matches with the original hash, then we continue

				return True

			# If none of the hashing algorithms are matched till now, then we return False
			return False
		else:
			# If the hashing algorithm is specified by the user, then we continue to generate the hash out of the plain text and verify it against the orignal hash

			# Checking the algorithm as per specified by the user and then executing the proper algorithm
			if self.algorithm == 'md5':
				# If the user specified algorithm is md5, then we continue

				hash = hashlib.md5(self.text).hexdigest()
			elif self.algorithm == 'sha1':
				# If the user specified algorithm is sha1, then we continue

				hash = hashlib.sha1(self.text).hexdigest()
			elif self.algorithm == 'sha224':
				# If the user specified algorithm is sha224, then we continue

				hash = hashlib.sha224(self.text).hexdigest()
			elif self.algorithm == 'sha256':
				# If the user specified algoritm is sha256, then we continue

				hash = hashlib.sha256(self.text).hexdigest()
			elif self.algorithm == 'sha378':
				# If the user specified algorithm is sha378, then we continue

				hash = hashlib.sha256(self.text).hexdigest()
			elif self.algorithm == 'sha512':
				# If the user specified algorithm is sha512, then we continue

				hash = hashlib.sha256(self.text).hexdigest()
			elif self.algorithm == 'sha3_224':
				# If the user specified algorithm is sha3_224, we continue

				hash = hashlib.sha3_224(self.text).hexdigest()
			elif self.algorithm == 'sha3_256':
				# If the user specified algorithm is sha3_256, we continue

				hash = hashlib.sha3_256(self.text).hexdigest()
			elif self.algorithm == 'shake_128':
				# If the user specified algorithm is shake_128, we continue

				hash = hashlib.shake_128(self.text).hexdigest()
			elif self.algorithm == 'shake_256':
				# If the user specified algorithm is shake_256, we continue

				hash = hashlib.shake_256(self.text).hexdigest()
			elif self.algorithm == 'sha3_384':
				# If the user specified algorithm is sha3_384, we continue

				hash = hashlib.sha3_384(self.text).hexdigest()
			elif self.algorithm == 'sha3_512':
				# If the user specified algorithm is sha3_512, we continue

				hash = hashlib.sha3_512(self.text).hexdigest()
			elif self.algorithm == 'blake2b':
				# If the user specified algorithm is blake2b, we continue

				hash = hashlib.blake2b(self.text).hexdigest()
			elif self.algorithm == 'blake2s':
				# If the user specified algorithm is blake2s, we continue

				hash = hashlib.blake2s(self.text).hexdigest()
			elif self.algorithm == 'fuck':
				# If the user specified algorithm is fuck, we continue

				# CUSTOM ALGORITHM
				# NAME : fuck
				# ----
				# Generating an hash encryption key
				key = 0
				isEven = True
				self.text = self.text.decode()
				for i in self.text:
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

				# Adding the length of the text to itself
				key += len(self.text)

				# Creating the cipher text from the plain text
				text = ''
				for character in self.text:
					# Iterating through each character in the plain text

					text += chr((ord(character) + key) % 256)

				# Encoding into the base64 format
				text = b64encode(text.encode()).decode()

				# Making the 'fuck' string out of the semi encrypted text
				hash = ''
				for index, character in enumerate(text):
					# Iterating through each character in the text

					hash += f'fuck{ord(character)}'
					if index != len(text) - 1:
						hash += '-' 
				del text
				# ----

			# Checking the hash generated from the plain text with the original hash
			print(hash, self.original)
			if hash == self.original:
				# If the hash generated from the plain text matches with the original hash, then we return True

				return True
			else:
				# If the hash generated from the plain text does not matches with the original hash, then we return False

				return False