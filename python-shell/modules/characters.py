"""
characters.py - Python Shell

A module created for supplying the required functions to the shell application. The functions and classes defined in this module ease many tasks at the shell application, in general way they are used in executing the task assigned by the user via the commands. This module contains functions and classes related to directory handling and other such stuff.

Author : Rishav Das (https://github.com/rdofficial/)
Created on : May 28, 2021

Last modified by : Rishav Das (https://github.com/rdofficial/)
Last modified on : May 29, 2021

Changed made in last modification :
1. Fixed a variable error in the NumberDetails.checkPossitiveNegative().

Authors contributed to this script (Add your name below if you have contributed) :
1. Rishav Das (github:https://github.com/rdofficial/, email:rdofficial192@gmail.com)
"""

# Importing the required functions and modules
try:
	pass
except Exception as e:
	# If there are any errors during the importing of the modules, then we display the error on the console screen

	input(f'\n[ Error : {e} ]\nPress enter key to continue...')
	exit()

class NumberDetails:
	""" The class which serves the feature of the Number Details. The number details is a in-built command for the shell. The purpose of this command / utility is for analyzing the number input given to it. The functions are defined inside this class which checks for the various properties of the number ranging from posstive-negative to the existence of the square-cube roots. """

	def __init__(self, number = 0):
		# If the user does not mention the number, then the default number assigned is 0

		self.number = number

		# Displaying the analysed information on the console screen
		print(f"""
[#] Type : {self.checkNegativePossitive()}
[#] Prime / Composite : {self.checkPrimeComposite()}
[#] Even / Odd : {self.checkEvenOdd()}
[#] Square root : {self.checkSquareRoot()}
[#] Cube root : {self.checkCubeRoot()}
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
	# ----