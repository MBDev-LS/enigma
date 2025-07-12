
import string

def forceSingleCharInput(func):
	def wrapper(*args, **kwargs):
		argumentsToCheck = list(args)[1:] + list(kwargs.values())
		print(argumentsToCheck, func.__name__)

		if len(argumentsToCheck) > 1:
			result = func(*args, **kwargs) # Should error.
		else:
			if argumentsToCheck[0].upper() in string.ascii_uppercase and len(argumentsToCheck[0]):
				result = func(*args, **kwargs)
			else:
				raise ValueError(f'Must be single letter, not \'{argumentsToCheck[0]}\'')

		return result
	return wrapper