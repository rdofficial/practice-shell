"""
characters.py - Python Shell

A module created for supplying the required functions to the shell application. The functions and classes defined in this module ease many tasks at the shell application, in general way they are used in executing the task assigned by the user via the commands. This module contains functions and classes related to directory handling and other such stuff.

Author : Rishav Das (https://github.com/rdofficial/)
Created on : May 28, 2021

Last modified by : Rishav Das (https://github.com/rdofficial/)
Last modified on : June 1, 2021

Changed made in last modification :
1. Added the code for the class 'RandomGenerator' which executes all the tasks of the 'random-string' command of the shell.

Authors contributed to this script (Add your name below if you have contributed) :
1. Rishav Das (github:https://github.com/rdofficial/, email:rdofficial192@gmail.com)
"""

# Importing the required functions and modules
try:
	from random import choices
except Exception as e:
	# If there are any errors during the importing of the modules, then we display the error on the console screen

	input(f'\n[ Error : {e} ]\nPress enter key to continue...')
	exit()

class NumberDetails:
	""" The class which serves the feature of the Number Details. The number details is a in-built command for the shell. The purpose of this command / utility is for analyzing the number input given to it. The functions are defined inside this class which checks for the various properties of the number ranging from posstive-negative to the existence of the square-cube roots. """

	def __init__(self, number = 0, execute = False):
		# If the user does not mention the number, then the default number assigned is 0

		self.number = number

		if execute:
			# If the object created via this class is called out with execute flag marked True, then we display the below fetched and calculated details

			# Displaying the analysed information on the console screen
			print(f"""
[#] Type : {self.checkNegativePossitive()}
[#] Prime / Composite : {self.checkPrimeComposite()}
[#] Even / Odd : {self.checkEvenOdd()}
[#] Square root : {self.checkSquareRoot()}
[#] Cube root : {self.checkCubeRoot()}
[#] Armstrong number : {self.checkArmstrongNumber()}
				""")

	def checkNegativePossitive(self):
		""" This method / function checks whether the number is a possitive or a negative number, and then returns the string values 'possitive' or 'negative' or '0' as per the calculations. This function checks for the class variable self.number. """

		if self.number > 0:
			# If the number is a possitive number, then we return 'possitive'

			return 'possitive'
		elif self.number == 0:
			# If the number is zero, then we return '0'

			return '0'
		else:
			# If the number is neither possitive nor zero, then it is probably negative. Thus, we return 'negative'

			return 'negative'

	def checkPrimeComposite(self):
		""" The method / function which checks whether the number is a prime number or a composite number. The method checks for the class variable self.number and then returns 'prime' or 'composite' as per the calculation results. """

		# Checking for factors of the number
		factorsCount = 0
		for i in range (1, self.number + 1):
			# Iterating through numbers from 1 to the mentioned number

			if self.number % i == 0:
				# If the number is divisible for the current iteration, then it is a factor

				factorsCount += 1

		if factorsCount > 2:
			# If the number of factors is more than 2, then we mark the number as composite number

			return 'composite'
		else:
			# If the number of factors is equal or less than 2, then we mark the number as prime number

			return 'prime'

	def checkEvenOdd(self):
		""" The method / function which checks whether the number is an odd number or an even number. The method checks for the class variable self.number and then returns 'even' or 'odd' as per the calculations results. """

		if self.number % 2 == 0:
			# If the number is divisible by 2, then we return 'even'

			return 'even'
		else:
			# If the number is not divisible by 2, then we return 'odd'

			return 'odd'

	def checkSquareRoot(self):
		""" This method / function checks whether the square root of the number is a whole number or not, else returns false. This function checks for the class variable self.number. If the square root exists, then the function returns a string '{square-root}', else returns the string '[ Square root is not a possitive whole number ]'. """

		if self.number > 0:
			# If the number is possitive, then we continue to check

			if (self.number ** (1/2)) == int(self.number ** (1/2)):
				# If the square root of the number is a whole number, then we return the answer

				return f'{int(self.number ** (1/2))}'
			else:
				# If the square root of the number is not a whole number, then we return a message stating no whole number

				return f'[ Square root is not a possitive whole number ]'
		elif self.number == 0:
			# If the number is 0, then we return '0'

			return '0'
		else:
			# If the number is a negative number, then we return the error string

			return '[ The number is a negative number ]'

	def checkCubeRoot(self):
		""" This method / function checks whether the cube root of the number is a whole number or not, else returns false. This function checks for the class variable self.number. If the cube root exists, then the function returns a string '{cube-root}', else returns the string '[ Cube root is not a possitive whole number ]'. """

		if self.number > 0:
			# If the number is possitive, then we continue to check

			if (self.number ** (1/3)) == int(self.number ** (1/3)):
				# If the cube root of the number is a whole number, then we return the answer

				return f'{int(self.number ** (1/3))}'
			else:
				# If the cube root of the number is not a whole number, then we return a message stating no whole number

				return f'[ Cube root is not a possitive whole number ]'
		elif self.number == 0:
			# If the number is 0, then we return '0'

			return '0'
		else:
			# If the number is a negative number, then we return the error string

			return '[ The number is a negative number ]'

	def checkArmstrongNumber(self):
		""" This method / function checks whether the number is an armstrong number or not. This function checks the number (numeric value) stored in the class variable self.number. The function returns true and false string depending upon the calculations.
		Armstrong number : A number whose value is equal to the sum of the cubes of its digits.
		e.g., 153 -> 1 + 125 + 27 """

		if self.number > 0:
			# If the number is a possitive number, then we continue to check

			number1 = 0
			for i in str(self.number):
				# Iterating through each of the digits of the number

				number1 += (int(i) ** 3)

			if number1 == self.number:
				# If the sum of cubes of each digits matches the original number, then we return 'True'

				return 'True'
			else:
				# If the sum of cubes of each digits does not matches the original number, then we return 'False'

				return 'False'
		elif self.number == 0:
			# If the number is 0, then we return '0'

			return '0'
		else:
			# If the number is a negative number, then we return the error string

			return '[ The number is a negative number ]'

	def checkNumber(self):
		""" The function checks for the number stored in the class variable self.number. """

		characters = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',]
		decimal = False
		for i in str(self.number):
			# Iterating through each character stored in the self.number value

			if i == '.':
				# If the currently iterated character is a decimal point

				if decimal:
					# If one decimal point is already recognized, then we return error (False)

					return False
				else:
					# If the decimal point is not recognized until this iteration, then we mark the decimal variable as True

					decimal = True
			elif i in characters:
				# If the currently iterated character is a number in the character set

				continue
			else:
				# If the currently iterated character is neither the decimal point nor any number in the character set, then we return error (False)

				return False

		# After all if the function runs till now, then we return True
		return True

	# Below funtions are not used by the self.__init__() method in particular. We need to call these functions directly in order to the execute the tasks served by them. The functions uses the same number stored at the class variable self.number
	# ----
	def table(self):
		""" This method / function prints the entire table for the number upto 10th iteration. """

		print(f'Table for {self.number} :')
		for i in range(1, 11):
			print(f'{self.number} x {i} = {self.number * i}')

	def factors(self):
		""" This method / function prints the factors of the number. """

		print(f'Factors of {self.number} are : ', end = '')
		for i in range(1, self.number + 1):
			if self.number % i == 0:
				print(f'{i},', end = '')
		print()

	def printPattern(self):
		""" This method / function prints a numeric pattern using the number (the numeric value stored in the class variable self.number). The number pattern works as per the number specified at the self.number. For 0 as the numeric value of self.number, this function prints the default pattern which is as per specified below :

		0
		0 0
		0 0 0
		0 0 0 0
		0 0 0 0 0
		0 0 0 0
		0 0 0
		0 0
		0
		"""

		if self.number > 0:
			# If the number is posstive, then we continue

			# Validating the self.number value to possible below 10 number (below 2 digit number)
			number1 = self.number % 10
			if number1 == 0 or number1 == 1	:
				# If the number reduces to 0, then we return the default pattern design

				for i in range(1, 6):
					print(f'{self.number} ' * i)
				for i in range(4, 1, -1):
					print(f'{self.number} ' * i)
			else:
				# If the number reduces to any number rather than 0, then we print the custom patten

				for i in range(0, number1):
					print(f'{self.number} ' * i)
				for i in range(number1, 0, -1):
					print(f'{self.number} ' * i)
		elif self.number == 0:
			# If the number is 0, then we return the default pattern for 0

			for i in range(1, 6):
				print('0 ' * i)
			for i in range(4, 1, -1):
				print('0 ' * i)
		else:
			# If the number is a negative number, then we make it possitive and then print the pattern

			# Making the number possitive version of itself
			number1 = self.number * (-1)

			# Validating the self.number value to possible below 10 number (below 2 digit number)
			number1 = self.number % 10
			if number1 == 0:
				# If the number reduces to 0, then we return the default pattern design

				for i in range(1, 6):
					print(f'{self.number} ' * i)
				for i in range(4, 1, -1):
					print(f'{self.number} ' * i)
			else:
				# If the number reduces to any number rather than 0, then we print the custom patten

				for i in range(0, number1):
					print(f'{self.number} ' * i)
				for i in range(number1, 1, -1):
					print(f'{self.number} ' * i)
	# ----

class RandomGenerator:
	""" This class which serves the feature of the Random Characters Generator. The Random Generator creates combination of random characters (alphabets, numbers, and special characters). This tool / class takes in the parameters : mode, length. The mode paramter specifies the type of the random string generated, exampe - Alphabets only, numbers only, special characters only, alphanumeric, alphaspecial, numericspecial, alphanumericspecial. The length parameter is used to specify the length of the characters to be generated. """

	def __init__(self, mode = None, length = None):

		self.length = length
		self.result = ''

		if mode == None:
			# If the mode is None (default), then we continue

			pass
		elif mode == 'alpha':
			# If the mode is alphabetic, then we continue

			self.alpha()
		elif mode == 'num':
			# If the mode is numeric, then we continue

			self.num()
		elif mode == 'special':
			# If the mode is special characters, then we continue

			self.special()
		elif mode == 'alphanum':
			# If the mode is alphanumeric, then we continue

			self.alphanum()
		elif mode == 'alphaspecial':
			# If the mode is alphabets + special characters, then we continue

			self.alphaspecial()
		elif mode == 'numspecial':
			# If the mode is numeric + special characters, then we continue

			self.numspecial()
		elif mode == 'alphanumspecial':
			# If the mode is alphanumeric + special characters, then we continue

			self.alphanumspecial()
		else:
			# If the mode is not recognized, then we raise the error

			raise SyntaxError(f'Mode for the RandomGenerator is not recognized - "{mode}"')

		# Finally, displaying the result of the random strings generation on console screen
		print(self.result)

	def alpha(self):
		""" This method / function serves the feature of the generation of the random characters created out of alphabets only. This function checks out for the length of the to be generated string from the class variable self.length. The function returns the generated by just assigning the generated string to the class variable self.result. """

		characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
		self.result = ''
		while len(self.result) != self.length:
			# Iterating to complete the string until the required length is hitted

			self.result += choices(characters)[0]
		return self.result

	def num(self):
		""" This method / function serves the feature of the generation of the random characters created out of numbers only. This function checks out for the length of the to be generated string from the class variable self.length. The function returns the generated by just assigning the generated string to the class variable self.result. """

		characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
		self.result = ''
		while len(self.result) != self.length:
			# Iterating to complete the string until the required length is hitted

			self.result += choices(characters)[0]
		return self.result

	def special(self):
		""" This method / function serves the feature of the generation of the random characters created out of special characters only. This function checks out for the length of the to be generated string from the class variable self.length. The function returns the generated by just assigning the generated string to the class variable self.result. """

		characters = ['~', '`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=', '|', '\\', '{', '[', '}', ']', ':', ';', '"', "'", '<', ',', '>', '.', '?', '/']
		self.result = ''
		while len(self.result) != self.length:
			# Iterating to complete the string until the required length is hitted

			self.result += choices(characters)[0]
		return self.result

	def alphanum(self):
		""" This method / function serves the feature of the generation of the random characters created out of alphabets and numbers. This function checks out for the length of the to be generated string from the class variable self.length. The function returns the generated by just assigning the generated string to the class variable self.result. """

		characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
		self.result = ''
		while len(self.result) != self.length:
			# Iterating to complete the string until the required length is hitted

			self.result += choices(characters)[0]
		return self.result

	def alphaspecial():
		""" This method / function serves the feature of the generation of the random characters created out of alphabets and special characters. This function checks out for the length of the to be generated string from the class variable self.length. The function returns the generated by just assigning the generated string to the class variable self.result. """

		characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '~', '`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=', '|', '\\', '{', '[', '}', ']', ':', ';', '"', "'", '<', ',', '>', '.', '?', '/']
		self.result = ''
		while len(self.result) != self.length:
			# Iterating to complete the string until the required length is hitted

			self.result += choices(characters)[0]
		return self.result

	def numspecial(self):
		""" This method / function serves the feature of the generation of the random characters created out of numbers and special characters. This function checks out for the length of the to be generated string from the class variable self.length. The function returns the generated by just assigning the generated string to the class variable self.result. """

		characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '~', '`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=', '|', '\\', '{', '[', '}', ']', ':', ';', '"', "'", '<', ',', '>', '.', '?', '/']
		self.result = ''
		while len(self.result) != self.length:
			# Iterating to complete the string until the required length is hitted

			self.result += choices(characters)[0]
		return self.result

	def alphanumspecial(self):
		""" This method / function serves the feature of the generation of the random characters created out of alphabets, numbers, and special characters. This function checks out for the length of the to be generated string from the class variable self.length. The function returns the generated by just assigning the generated string to the class variable self.result. """
		
		characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '~', '`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=', '|', '\\', '{', '[', '}', ']', ':', ';', '"', "'", '<', ',', '>', '.', '?', '/']
		self.result = ''
		while len(self.result) != self.length:
			# Iterating to complete the string until the required length is hitted

			self.result += choices(characters)[0]
		return self.result