"""
encryption.py - Python Shell

A module created for supplying the required functions to the shell application. The functions and classes defined in this module ease many tasks at the shell application, in general way they are used in executing the task assigned by the user via the commands. This module contains functions and classes related to directory handling and other such stuff.

Author : Rishav Das (https://github.com/rdofficial/)
Created on : June 13, 2021

Last modified by : Rishav Das (https://github.com/rdofficial/)
Last modified on : June 14, 2021

Changes made in the last modification :
<<<<<<< HEAD
1. Added the code to serve the functionality to check password of the encryption / decryption in the 'FileEncrypter' class.
=======
1. Created the class 'FileEncrypter' which serves the feature of encrypting text files, and other r+w files too.
>>>>>>> fdd6b572e45618d5127462aaa4f8476769900282

Authors contributed to this script (Add your name below if you have contributed) :
1. Rishav Das (github:https://github.com/rdofficial/, email:rdofficial192@gmail.com)
"""

# Importing the required functions and modules
try:
	from base64 import b64encode, b64decode
	from io import TextIOWrapper
<<<<<<< HEAD
	from os import path
=======
>>>>>>> fdd6b572e45618d5127462aaa4f8476769900282
	import hashlib
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

				print('<-- help for StringEncrypter -->')
			else:
				# If the user specified the execution mode, then we continue to execute the task

				# Validating the user entered password
				# ----
				# Checking the password input type
				if type(self.password) == str:
					# If the password's value as per entered by the user is a string type variable, then we continue for further validation
<<<<<<< HEAD

					# Checking for string length
					if len(self.password) > 4:
						# If the user specified password has character length more than 4, then we continue

						pass
					else:
						# If the user specified password has character length less than 4 charcters, then we raise an error with a custom message

=======

					# Checking for string length
					if len(self.password) > 4:
						# If the user specified password has character length more than 4, then we continue

						pass
					else:
						# If the user specified password has character length less than 4 charcters, then we raise an error with a custom message

>>>>>>> fdd6b572e45618d5127462aaa4f8476769900282
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

					self.encrypt()
					print(f'Output :\n{self.text}')
				elif self.task.lower() == 'decrypt' or self.task.lower() == 'decryption':
					# If the task specified is for decryption, then we continue to decrypt

					self.decrypt()
					print(f'Output :\n{self.text}')
				else:
					# If the task specified is not recognized, then we raise an error with a custom message

					raise ReferenceError('Task not recognized. Encrypt / decrypt are the two recognizable terms.')
<<<<<<< HEAD
				del self.task
=======
>>>>>>> fdd6b572e45618d5127462aaa4f8476769900282

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
	""" """

<<<<<<< HEAD
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

				print('<-- help for StringEncrypter -->')
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
=======
	def __init__(self, filename = None, password = None):
		# Validating the user entered parameters
		# ----
		# Validating the filename parameter input (The name / location of the file that is to be encrypted using this tool)
		if filename == None:
			# If the filename parameter is not specified by the user (default), then we raise an error with a custom message

			raise SyntaxError('File name not specified.')
		else:
			# If the filename parameter is specified by the user, then we continue for further validation

			if type(filename) == str:
				# If the filename parameter input specified by the user is of str type, then we continue

				self.contents = open(filename, 'r').read()
				self.contents = self.contents.decode()
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
>>>>>>> fdd6b572e45618d5127462aaa4f8476769900282

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

<<<<<<< HEAD
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
=======
	def encrypt(self):
		pass

	def decrypt(self):
		pass
>>>>>>> fdd6b572e45618d5127462aaa4f8476769900282
