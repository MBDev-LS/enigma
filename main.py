
import string


class PlugboardConnection():
	def __init__(self, letter0: str, letter1: str) -> None:
		self.letter0 = letter0
		self.letter1 = letter1


	def checkForLetter(self, letterToCheck: str) -> bool:
		return letterToCheck == self.letter0 or letterToCheck == self.letter1
	

	def getListOfLetters(self) -> tuple:
		return (self.letter0, self.letter1)


class Plugboard():
	def __init__(self, plugboardList: list[PlugboardConnection] | None=None) -> None:
		self.plugboardList = plugboardList if plugboardList != None else []

		if self.validatePlugboardList() != True:
			raise Exception(f"Invalid plugboardList '{plugboardList}'. Must not contain two or more PlugboardConnections with the same letter.")

	
	def validatePlugboardList(self, targetPlugboardList: list[PlugboardConnection] | None=None) -> bool:
		targetList = targetPlugboardList if targetPlugboardList != None else self.plugboardList

		lettersWithConnections = []
		for plugboardConnection in targetList:
			if plugboardConnection.letter0 in lettersWithConnections or plugboardConnection.letter1 in lettersWithConnections:
				return False
			
			lettersWithConnections.append(plugboardConnection.letter0)
			lettersWithConnections.append(plugboardConnection.letter1)
	
		return True
	

	def addConnection(self, newPlugboardConnection: PlugboardConnection) -> None:
		proposedPlugboardList = self.plugboardList + [newPlugboardConnection]
		if self.validatePlugboardList(proposedPlugboardList) != True:
			raise Exception(f"Cannot add PlugboardConnections '{newPlugboardConnection}', contains letter already used in active connection.")
		else:
			self.plugboardList.append(newPlugboardConnection)
	



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
	def __init__(self, plugboard: Plugboard, rotorList: list[str], reflector) -> None:
		self.plugboard = plugboard
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
	
	engimaMachine.processStringOfLetters('HELLOWORLD')

