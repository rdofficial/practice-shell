"""
encryption.py - Python Shell

A module created for supplying the required functions to the shell application. The functions and classes defined in this module ease many tasks at the shell application, in general way they are used in executing the task assigned by the user via the commands. This module contains functions and classes related to directory handling and other such stuff.

Author : Rishav Das (https://github.com/rdofficial/)
Created on : June 13, 2021

Last modified by : Rishav Das (https://github.com/rdofficial/)
Last modified on : June 13, 2021

Changes made in the last modification :
1. Added the code which serve the functionality of argument parsing, task executing, etc to the class 'StringEncrypter'.

Authors contributed to this script (Add your name below if you have contributed) :
1. Rishav Das (github:https://github.com/rdofficial/, email:rdofficial192@gmail.com)
"""

# Importing the required functions and modules
try:
	from base64 import b64encode, b64decode
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

				self.encrypt()
				print(f'Output :\n{self.text}')
			elif self.task.lower() == 'decrypt' or self.task.lower() == 'decryption':
				# If the task specified is for decryption, then we continue to decrypt

				self.decrypt()
				print(f'Output :\n{self.text}')
			else:
				# If the task specified is not recognized, then we raise an error with a custom message

				raise ReferenceError('Task not recognized. Encrypt / decrypt are the two recognizable terms.')

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