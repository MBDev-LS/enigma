
import string


class PlugboardConnection():
	def __init__(self, letter0: str, letter1: str) -> None:
		self.letter0 = letter0
		self.letter1 = letter1


	def checkForLetter(self, letterToCheck: str) -> bool:
		return letterToCheck == self.letter0 or letterToCheck == self.letter1



class Rotor():
	# Note: Rotor positions are 0-indexed. Should they be? I don't know, but they are, so deal with it.

	def __init__(self, name: str, outputMappingSequenceString: str, ringSettingOffset: int, turnoverPosition: int, startingPosition: int) -> None:
		self.name = name
		self.outputMappingSequenceString = outputMappingSequenceString
		self.ringSettingOffset = ringSettingOffset
		self.turnoverPosition = turnoverPosition
		self.currentPosition = startingPosition
	
	def turnRotor(self):
		self.currentPosition = (self.currentPosition + 1) % 26 # Note that this is 26, not 27, due to the aforementioned (and potentially ill-advised) 0-indexing.




class EngimaMachine():
	def __init__(self, plugboardList: list[PlugboardConnection], rotorList: list[str], reflector) -> None:
		self.plugboardList = plugboardList
		self.rotorList = rotorList
		self.reflector = reflector


	def transformLetter(self, letter: str) -> str:
		pass


	def __checkInputStringIsValid(self, inputString: str) -> bool:
		for char in inputString:
			if char not in string.ascii_uppercase:
				return False
		
		return True


	def processStringOfLetters(self, inputString: str) -> str:
		uppercaseInputString = inputString.upper()
		inputStringIsValid = self.__checkInputStringIsValid(uppercaseInputString)

		if inputStringIsValid != True:
			raise Exception(f"Invalid inputString '{inputString}'. Must be string containing ONLY letters in the Latin/Roman alphabet.")

		transformedOutputString = ''

		for currentLetter in uppercaseInputString:
			transformedOutputString += self.transformLetter(currentLetter)
		
		return transformedOutputString



if __name__ == '__main__':
	engimaMachine = EngimaMachine([], [], None)
	
	engimaMachine.processStringOfLetters('ABCa4D')

