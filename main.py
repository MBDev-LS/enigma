
import string
import json

from utils import forceOnlyLetterStringsArgs

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent



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


class MappingComponent():
	def __init__(self, name: str, rightMappingSequence: str, leftMappingSequence: str=string.ascii_uppercase) -> None:
		self.name = name
		self.leftMappingSequence = leftMappingSequence
		self.rightMappingSequence = rightMappingSequence
	
	# @forceOnlyLetterStringsArgs(limitLengthToOne=True) # ISSUE WITH INPUT MAPPING, FIX
	def mapLetter(self, signalToMap: int, reverseMap: bool=False) -> int:
		if reverseMap == False:
			mappedLetter = self.rightMappingSequence[signalToMap]

			return self.leftMappingSequence.find(mappedLetter)
		else:
			mappedLetter = self.leftMappingSequence[signalToMap]

			return self.rightMappingSequence.find(mappedLetter)

class Rotor(MappingComponent):
	# Note: Rotor positions are 0-indexed. Should they be? I don't know, but they are.

	@staticmethod
	@forceOnlyLetterStringsArgs(limitLengthToOne=True, allowSpaceCharacter=False, ignoreFirstArgument=False)
	def convertLetterToNumericTurnoverPosition(letterToConvert: str) -> int:
		uppercaseLetterToConvert = letterToConvert.upper()

		numericalTurnoverPrimeingPosition = string.ascii_uppercase.index(uppercaseLetterToConvert)

		return numericalTurnoverPrimeingPosition


	def __init__(self, name: str, rightMappingSequence: str, turnoverPositionLetter: str, ringSettingOffset: int, startingPosition: int, leftMappingSequence: str=string.ascii_uppercase, turnWhenRotorToLeftTurns: bool=False) -> None:
		super().__init__(name, rightMappingSequence, leftMappingSequence)

		self.ringSettingOffset = ringSettingOffset
		# self.numericalTurnoverPrimeingPosition = turnoverPosition
		# self.currentPosition = startingPosition

		numericalTurnoverPosition = self.convertLetterToNumericTurnoverPosition(turnoverPositionLetter)
		self.numericalTurnoverPosition = (numericalTurnoverPosition - ringSettingOffset) % 26
		self.currentPosition = (startingPosition - ringSettingOffset) % 26

		self.turnWhenRotorToLeftTurns = turnWhenRotorToLeftTurns
	

	@classmethod
	def loadRotorListFromJson(cls, jsonFilePath: str | Path, ringSettingOffsets: list[int], startingPositions: list[int], leftMappingSequences: list[str] | None=None, turnWhenRotorToLeftTurns: list[bool] | None=None) -> list:
		with open(jsonFilePath, 'r') as jsonRotorFile:
			rotorDictsList = json.loads(jsonRotorFile.read())

		leftMappingSequences = leftMappingSequences if leftMappingSequences != None else [string.ascii_uppercase] * len(rotorDictsList)
		turnWhenRotorToLeftTurns = turnWhenRotorToLeftTurns if turnWhenRotorToLeftTurns != None else [False] * len(rotorDictsList)

		if len(rotorDictsList) != len(ringSettingOffsets):
			errorDescriptor = 'few' if len(ringSettingOffsets) < len(ringSettingOffsets) else 'many'

			raise IndexError(f"Failed to load rotors from JSON, too {errorDescriptor} ring setting offsets provided in ringSettingOffsets tuple '{ringSettingOffsets}'. ({len(ringSettingOffsets)} provided for {len(rotorDictsList)} rotors.)")
		elif len(rotorDictsList) != len(startingPositions):
			errorDescriptor = 'few' if len(startingPositions) < len(rotorDictsList) else 'many'

			raise IndexError(f"Failed to load rotors from JSON, too {errorDescriptor} starting positions provided in startingPositions tuple '{startingPositions}'. ({len(startingPositions)} provided for {len(rotorDictsList)} rotors.)")
		elif len(rotorDictsList) != len(leftMappingSequences):
			errorDescriptor = 'few' if len(leftMappingSequences) < len(rotorDictsList) else 'many'

			raise IndexError(f"Failed to load rotors from JSON, too {errorDescriptor} left mapping sequences provided in leftMappingSequences tuple '{leftMappingSequences}'. ({len(leftMappingSequences)} provided for {len(rotorDictsList)} rotors.)")
		elif len(rotorDictsList) != len(turnWhenRotorToLeftTurns):
			errorDescriptor = 'few' if len(turnWhenRotorToLeftTurns) < len(rotorDictsList) else 'many'

			raise IndexError(f"Failed to load rotors from JSON, too {errorDescriptor} left mapping sequences provided in leftMappingSequences tuple '{turnWhenRotorToLeftTurns}'. ({len(turnWhenRotorToLeftTurns)} provided for {len(rotorDictsList)} rotors.)")
		
		outputRotorList = []

		for rotorIndex, rotorDict in enumerate(rotorDictsList):

			newRotor = cls(rotorDict['name'], rotorDict['mapping_string'], rotorDict['turnover_notch_position'], ringSettingOffsets[rotorIndex], startingPositions[rotorIndex], leftMappingSequences[rotorIndex], turnWhenRotorToLeftTurns[rotorIndex])

			outputRotorList.append(newRotor)
		
		return outputRotorList


	def turnRotor(self) -> None:
		self.currentPosition = (self.currentPosition + 1) % 26 # Note that this is 26, not 27, due to the aforementioned (and potentially ill-advised) 0-indexing.


	def checkForTurnoverState(self) -> bool:
		turnoverTriggered = self.currentPosition + 1 == self.numericalTurnoverPosition

		return turnoverTriggered
	

	# Overwrites inhereted method of the same name.
	# @forceOnlyLetterStringsArgs(limitLengthToOne=True) # gonna cause issues, FIX THIS LATER
	def mapLetter(self, signalToMap: int, reverseMap: bool=False) -> int:
		if reverseMap == False:
			mappedLetter = self.rightMappingSequence[(signalToMap + self.currentPosition) % 26]

			return (self.leftMappingSequence.find(mappedLetter) - self.currentPosition) % 26
		else:
			mappedLetter = self.leftMappingSequence[(signalToMap + self.currentPosition) % 26]

			return (self.rightMappingSequence.find(mappedLetter) - self.currentPosition) % 26


class Reflector(MappingComponent):
	pass


class EngimaMachine():
	def __init__(self, plugboard: Plugboard, rotorList: list[Rotor], reflector: Reflector, outputOnlyUppercase: bool=True, spaceOutputCharacter: str=' ') -> None:
		self.plugboard = plugboard
		self.rotorList = rotorList
		self.reflector = reflector
		
		self.outputOnlyUppercase = outputOnlyUppercase
		self.spaceOutputCharacter = spaceOutputCharacter


	def turnRotors(self) -> None:
		if len(self.rotorList) == 0:
			raise Exception('Failed to turn rotors as none are loaded into enigma machine.')
		
		oldRotorPositons = ''.join([string.ascii_uppercase[rotor.currentPosition] for rotor in self.rotorList])

		turnoverStatesAtStartOfTurn = [rotor.checkForTurnoverState() for rotor in self.rotorList]

		self.rotorList[0].turnRotor()

		# For loop does not include the left most rotor
		# index, as there's no need to check its turnover
		# state. 

		for currentRotorIndex in range(1, len(self.rotorList)): 
			currentRotor = self.rotorList[currentRotorIndex]
			previousRotorToRight = self.rotorList[currentRotorIndex - 1]

			if turnoverStatesAtStartOfTurn[currentRotorIndex - 1] == True: # do that thing and -1 to the turnover state?
				currentRotor.turnRotor()

				if previousRotorToRight.turnWhenRotorToLeftTurns == True:
					previousRotorToRight.turnRotor()
				
				# print(f"Rotor: {rotorToTurn.name}\n Current Position: {rotorToTurn.currentPosition}\n Turnover Position: {rotorToTurn.numericalTurnoverPrimeingPosition}")
				# print(' Next Rotor Primed?', primeNextRotorToTurn, '\n')

		newRotorPositons = ''.join([string.ascii_uppercase[rotor.currentPosition] for rotor in self.rotorList])

		print(f'Turned wheel from {oldRotorPositons[::-1]} to {newRotorPositons[::-1]}')
		print()


	@forceOnlyLetterStringsArgs(limitLengthToOne=True)
	def processLetterInPlugboard(self, letterToProcess: str) -> str:
		connectionWithLetter = self.plugboard.getConnectionByLetter(letterToProcess)
		if connectionWithLetter != None:
			return connectionWithLetter.getOppositeLetter(letterToProcess)
		else:
			return letterToProcess
	
	
	# @forceOnlyLetterStringsArgs(limitLengthToOne=True)
	def processLetterSignalInRotors(self, signalToProcess: int, reverseOrder: bool=False) -> int:
		currentSignal = signalToProcess

		startingRotorIndex = 0 if reverseOrder != True else len(self.rotorList) - 1
		endingRotorIndex =  len(self.rotorList) if reverseOrder != True else -1
		changeInIndex =  1 if reverseOrder != True else -1 

		for currentRotorIndex in range(startingRotorIndex, endingRotorIndex, changeInIndex):
			oldLetter = currentSignal
			currentSignal = self.rotorList[currentRotorIndex].mapLetter(currentSignal, reverseOrder)
			print(f'Rotor: {self.rotorList[currentRotorIndex].name}, Input: {string.ascii_uppercase[oldLetter]}, Output: {string.ascii_uppercase[currentSignal]}')
		
		return currentSignal


	@forceOnlyLetterStringsArgs(limitLengthToOne=True)
	def transformLetter(self, letter: str) -> str:

		self.turnRotors()
		letterFromPlugboard0 = self.processLetterInPlugboard(letter)

		signalFromPlugboard = string.ascii_uppercase.find(letterFromPlugboard0)
		letterSignalFromRotors0 = self.processLetterSignalInRotors(signalFromPlugboard)
		reflectedLetter = self.reflector.mapLetter(letterSignalFromRotors0)
		print('Reflected letter:', string.ascii_uppercase[reflectedLetter])
		letterSignalFromRotors1 = self.processLetterSignalInRotors(reflectedLetter, reverseOrder=True)
		letterFromRotorProcess = string.ascii_uppercase[letterSignalFromRotors1]


		letterFromPlugboard1 = self.processLetterInPlugboard(letterFromRotorProcess)

		return letterFromPlugboard1


	@forceOnlyLetterStringsArgs(allowLowerCase=True, allowSpaceCharacter=True)
	def processStringOfLetters(self, inputString: str) -> str:

		transformedOutputString = ''

		debugIndex = 0
		for currentCharacter in inputString:
			print()
			print()
			print('####### ' + inputString + ' #######')
			print('        ' + ' '*debugIndex + '^')
			print(f"Current character: '{currentCharacter}'\nPosition: {debugIndex}")
			print()

			debugIndex += 1
			
			if currentCharacter != ' ':
				transformedLetter = self.transformLetter(currentCharacter.upper())
			else:
				transformedLetter = self.spaceOutputCharacter

			if self.outputOnlyUppercase == False and currentCharacter in string.ascii_lowercase:
				transformedLetter = transformedLetter.lower()

			transformedOutputString += transformedLetter
		
		return transformedOutputString



if __name__ == '__main__':
	plugboard = Plugboard([])
	
	# The turnover values are 0-indexed
	rotor1 = Rotor('I', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'R', 0, 0) # 16, as primed at before R
	rotor2 = Rotor('II', 'AJDKSIRUXBLHWTMCQGZNPYFVOE', 'F', 0, 0, turnWhenRotorToLeftTurns=True)
	rotor3 = Rotor('III', 'BDFHJLCPRTXVZNYEIWGAKMUSQO', 'W', 0, 0)

	# rotorList = [rotor1, rotor2, rotor3]

	rotorList = Rotor.loadRotorListFromJson(BASE_DIR / 'rotors1.json', [0, 0, 0], [0, 0, 0], None, [False, True, False])

	reflector = Reflector('Reflector B', 'YRUHQSLDPXNGOKMIEBFZCWVJAT')
	engimaMachine = EngimaMachine(plugboard, rotorList, reflector, True)
	output = engimaMachine.processStringOfLetters('MyfatherhadasmallestateinNottinghamshireIwasthethirdoffivesonsHesentmetoEmmanuelCollegeinCambridgeatfourteenyearsoldwhereIresidedthreeyears') # MyfatherhadasmallestateinNottinghamshireIwasthethirdoffivesonsHesentmetoEmmanuelCollegeinCambridgeatfourteenyearsoldwhereIresidedthreeyears
	print(output)

	n=5
	print(' '.join([output[i:i+n] for i in range(0, len(output), n)]))

	import pyperclip
	pyperclip.copy(output)
