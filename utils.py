
import string



def forceOnlyLetterStringsArgs(limitLengthToOne: bool=False):
	"""
	Forces all string arguments to
	contain only strings

	:limitLengthToOne: Whether to limit string arguments to a length of one.
	"""
	def inner_forceCharOnlyInput(furnishedFunction):
		def wrapper(*args, **kwargs):
			argumentsToCheck = list(args)[1:] + list(kwargs.values())
			
			for currentArgument in argumentsToCheck:
				if type(currentArgument) == str:
					if currentArgument not in string.ascii_uppercase:
						raise ValueError(f'String must contain ONLY letters in the Latin/Roman alphabet, not \'{argumentsToCheck[0]}\'.')
					elif len(currentArgument) > 1 and limitLengthToOne:
						raise ValueError(f'String must have a length no greater than 1.')

			functionResult = furnishedFunction(*args, **kwargs)
			
			return functionResult
		
		return wrapper
	return inner_forceCharOnlyInput


