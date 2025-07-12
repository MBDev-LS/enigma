
import string


from utils import forceOnlyLetterStringsArgs


class PlugboardConnection():
	@forceOnlyLetterStringsArgs(limitLengthToOne=True)
	def __init__(self, letter0: str, letter1: str) -> None:
		self.letter0 = letter0
		self.letter1 = letter1
	
	
	def __str__(self) -> str:
		return f'<PlugboardConnection {self.letter0}-{self.letter1}>'

	@forceOnlyLetterStringsArgs(limitLengthToOne=True)
	def checkForLetter(self, letterToCheck: str) -> bool:
		return letterToCheck == self.letter0 or letterToCheck == self.letter1
	

	def getLettersInTuple(self) -> tuple:
		return (self.letter0, self.letter1)


class Plugboard():
	def __init__(self, connectionsList: list[PlugboardConnection] | None=None) -> None:
		self.connectionsList = connectionsList if connectionsList != None else []

		if self.validateconnectionsList() != True:
			raise Exception(f"Invalid connectionsList '{connectionsList}'. Must not contain two or more PlugboardConnections with the same letter.")
	

	def __str__(self) -> str:
		return f'<Plugboard [{", ".join([str(connection) for connection in self.connectionsList])}]>'

	
	def validateconnectionsList(self, targetconnectionsList: list[PlugboardConnection] | None=None) -> bool:
		targetList = targetconnectionsList if targetconnectionsList != None else self.connectionsList

		lettersWithConnections = []
		for plugboardConnection in targetList:
			if plugboardConnection.letter0 in lettersWithConnections or plugboardConnection.letter1 in lettersWithConnections:
				return False
			
			lettersWithConnections.append(plugboardConnection.letter0)
			lettersWithConnections.append(plugboardConnection.letter1)
	
		return True
	

	@forceOnlyLetterStringsArgs(limitLengthToOne=True)
	def getConnectionByLetter(self, targetLetter: str) -> PlugboardConnection | None:
		for currentConnection in self.connectionsList:
			if currentConnection.checkForLetter(targetLetter) == True:
				return currentConnection
		
		return None
	

	def addConnection(self, newPlugboardConnection: PlugboardConnection) -> None:
		proposedconnectionsList = self.connectionsList + [newPlugboardConnection]
		if self.validateconnectionsList(proposedconnectionsList) != True:
			raise Exception(f"Cannot add PlugboardConnections '{newPlugboardConnection}', contains letter already used in active connection.")
		else:
			self.connectionsList.append(newPlugboardConnection)
	
	
	def removeConnection(self, plugboardConnectionToRemove: PlugboardConnection) -> None:
		numberOfConnectionInstancesInList = self.connectionsList.count(plugboardConnectionToRemove)
		if numberOfConnectionInstancesInList  == 0:
			raise ValueError(f"Tried to remove connection '{plugboardConnectionToRemove}', not in connectionsList '{self.connectionsList}'.")
		elif numberOfConnectionInstancesInList > 1:
			raise Exception(f"Failed to remove connection '{plugboardConnectionToRemove}' from connectionsList '{self.connectionsList}'. Too many instances of connection, must not be more than one.")
		else:
			self.connectionsList.remove(plugboardConnectionToRemove)
	

	@forceOnlyLetterStringsArgs(limitLengthToOne=True)
	def removeConnectionByLetter(self, targetLetter: str) -> bool:
		"""
		Removes connection involving
		targetLetter if it exists.

		Returns True if connection is
		found and removed, otherwise
		returns False.
		"""

		connectionToDelete = self.getConnectionByLetter(targetLetter)
		if connectionToDelete != None:
			self.removeConnection(connectionToDelete)
			return True
		
		return False



class Rotor():
	# Note: Rotor positions are 0-indexed. Should they be? I don't know, but they are, so deal with it.

	def __init__(self, name: str, outputMappingSequenceString: str, ringSettingOffset: int, turnoverPosition: int, startingPosition: int) -> None:
		self.name = name
		self.outputMappingSequenceString = outputMappingSequenceString
		self.ringSettingOffset = ringSettingOffset
		self.turnoverPosition = turnoverPosition
		self.currentPosition = startingPosition
	
	def turnRotor(self) -> bool:
		self.currentPosition = (self.currentPosition + 1) % 26 # Note that this is 26, not 27, due to the aforementioned (and potentially ill-advised) 0-indexing.

		turnoverTriggered = self.currentPosition == self.turnoverPosition
		return turnoverTriggered
	





class EngimaMachine():
	def __init__(self, plugboard: Plugboard, rotorList: list[str], reflector) -> None:
		self.plugboard = plugboard
		self.rotorList = rotorList
		self.reflector = reflector


	@forceOnlyLetterStringsArgs(limitLengthToOne=True)
	def transformLetter(self, letter: str) -> str:
		pass

	"""
	- Turn rotors
		- Turn rotor, check for turnover triger
		- If there is another rotor loaded, set to current and repeat from last step
	- Check switchboard for switch and perform if neccessary
	- Send switchboard result through rotors (and reflector)
		- Map letter via current rotor
		- Check for next rotor, if found, repeat. If not, passthrough reflectors and repeat mappings IN REVERSE
	- Check switchboard withj result and switch if neccessaary
	- Return transformed letter
	"""


	@forceOnlyLetterStringsArgs()
	def processStringOfLetters(self, inputString: str) -> str:
		uppercaseInputString = inputString.upper()

		transformedOutputString = ''

		for currentLetter in uppercaseInputString:
			transformedOutputString += self.transformLetter(currentLetter)
		
		return transformedOutputString



if __name__ == '__main__':
	# engimaMachine = EngimaMachine([], [], None)
	
	# engimaMachine.processStringOfLetters('HELLOWORLD')

	plugboard = Plugboard([PlugboardConnection('A', 'D')])
	connection0 = PlugboardConnection('A', 'E')
	connection0.checkForLetter('B')

	# print(plugboard, connection0)

	# plugboard.addConnection(connection0)

	# print(plugboard)


