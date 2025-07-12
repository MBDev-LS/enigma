
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
	
	@forceOnlyLetterStringsArgs(limitLengthToOne=True)
	def getOppositeLetter(self, targetLetter: str) -> str:
		if self.checkForLetter(targetLetter) == False:
			raise ValueError(f"Failed to switch letter '{targetLetter}', not part of connection \'{self}\'")
		
		if targetLetter == self.letter0:
			return self.letter1
		else:
			return self.letter0



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


class Reflector():
	# Right, so the more observant among you may
	# notice that all of the Reflector class' code is
	# shared with Rotor class. That means that Rotor
	# Could have inheritted from Reflector instead of
	# having this code twice. This change would take
	# about a minute to make. But I haven't, because
	# I don't feel like it. It just doesn't feel right.
	def __init__(self) -> None:
		self.name = name
		self.outputMappingSequenceString = outputMappingSequenceString


class EngimaMachine():
	def __init__(self, plugboard: Plugboard, rotorList: list[Rotor], reflector) -> None:
		self.plugboard = plugboard
		self.rotorList = rotorList
		self.reflector = reflector


	def turnRotors(self) -> None:
		if len(self.rotorList) == 0:
			raise Exception('Failed to turn rotors as none are loaded into enigma machine.')
		
		currentRotorIndex = 0 
		turnNextRotor = True

		while turnNextRotor == True and currentRotorIndex < len(self.rotorList):
			turnNextRotor = self.rotorList[currentRotorIndex].turnRotor()
			currentRotorIndex += 1
	

	@forceOnlyLetterStringsArgs(limitLengthToOne=True)
	def processLetterInPlugboard(self, letterToProcess: str) -> str:
		connectionWithLetter = self.plugboard.getConnectionByLetter(letterToProcess)
		if connectionWithLetter != None:
			return connectionWithLetter.getOppositeLetter(letterToProcess)
		else:
			return letterToProcess
	
	
	@forceOnlyLetterStringsArgs(limitLengthToOne=True)
	def processLetterInRotors(self, letterToSwitch: str, reverseOrder: bool=False) -> str:
		pass



	@forceOnlyLetterStringsArgs(limitLengthToOne=True)
	def transformLetter(self, letter: str) -> str:

		self.turnRotors()
		letterFromPlugboard = self.processLetterInPlugboard(letter)
		letterFromRotors = ''




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

"""
# GERMAN ARMY WW2 ROTORS
Rotor # 	ABCDEFGHIJKLMNOPQRSTUVWXYZ		Date Introduced 	Model Name & Number
I 			EKMFLGDQVZNTOWYHXUSPAIBRCJ		1930 				Enigma I
II 			AJDKSIRUXBLHWTMCQGZNPYFVOE		1930 				Enigma I
III 		BDFHJLCPRTXVZNYEIWGAKMUSQO		1930 				Enigma I
IV 			ESOVPZJAYQUIRHXLNFTGKDCMWB		December 1938 		M3 Army
V 			VZBRGITYUPSDNHLXAWMJQOFECK		December 1938 		M3 Army 


TURNOVER NOTCH POSITIONS
Rotor 		Notch 		Effect
I 			Q 			If rotor steps from Q to R, the next rotor is advanced
II 			E 			If rotor steps from E to F, the next rotor is advanced
III 		V 			If rotor steps from V to W, the next rotor is advanced
IV 			J 			If rotor steps from J to K, the next rotor is advanced
V 			Z 			If rotor steps from Z to A, the next rotor is advanced 

Note: Turnover position numbers should be the number for the letter AFTER the one in the notch column.
"""
