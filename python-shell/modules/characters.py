"""
characters.py - Python Shell

A module created for supplying the required functions to the shell application. The functions and classes defined in this module ease many tasks at the shell application, in general way they are used in executing the task assigned by the user via the commands. This module contains functions and classes related to directory handling and other such stuff.

Author : Rishav Das (https://github.com/rdofficial/)
Created on : May 28, 2021

Last modified by : -
Last modified on : -

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
	""""""

	def __init__(self, number = 0):
		# If the user does not mention the number, then the default number assigned is 0

		self.number = number

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
		""" The method / function which checks whether the number is an odd number or an even number. The method checks fr the class variable self.number and then returns 'even' or 'odd' as per the calculations results. """

		if self.number % 2 == 0:
			# If the number is divisible by 2, then we return 'even'

			return 'even'
		else:
			# If the number is not divisible by 2, then we return 'odd'

			return 'odd'

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