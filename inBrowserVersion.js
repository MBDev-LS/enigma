
class PlugboardConnection {
	constructor(letter0, letter1) {
		this.letter0 = letter0
		this.letter1 = letter1
	}


	toString() {
		return `<PlugboardConnection ${this.letter0}-${this.letter1}>`;
	};


	checkForLetter(letterToCheck) {
		return letterToCheck == this.letter0 || letterToCheck == this.letter1;
	};


	getLettersInArray() { // FKA getLettersInTuple
		return [self.letter0, self.letter1];
	};


	getOppositeLetter(targetLetter) {
		if (this.checkForLetter(targetLetter) === false) {
			throw new Error(`Failed to switch letter '${targetLetter}', not part of connection \'${this}\'`);
		};

		if (targetLetter === this.letter0) {
			return this.letter1;
		} else {
			return this.letter0;
		};
	};
};


class Plugboard {
	constructor(connectionsList) {
		this.connectionsList = connectionsList ?? [];

		if (this.validateconnectionsList() !== true) {
			throw new Error(`Invalid connectionsList '${connectionsList}'. Must not contain two or more PlugboardConnections with the same letter.`)
		};
	};


	toString() {
		throw new Error(`<Plugboard [${this.connectionsList.map(c => String(c)).join(", ")}]>`);
	}


	validateconnectionsList(targetconnectionsList) {
		let targetList = targetconnectionsList ?? this.connectionsList;

		let lettersWithConnections = [];
		for (const plugboardConnection in targetList) {
			if (lettersWithConnections.includes(plugboardConnection.letter0) || lettersWithConnections.includes(plugboardConnection.letter1)) {
				return false;
			};

			lettersWithConnections.push(plugboardConnection.letter0);
			lettersWithConnections.push(plugboardConnection.letter1);

			return true;
		};
	};

	
	getConnectionByLetter(targetLetter) {
		for (const currentConnection in this.connectionsList) {
			if (currentConnection.checkForLetter(targetLetter) === true) {
				return currentConnection;
			};
		};

		return null;
	};


	addConnection(newPlugboardConnection) {
		let proposedconnectionsList = [...this.connectionsList, newPlugboardConnection];
		
		if (this.validateconnectionsList(proposedconnectionsList) !== true) {
			throw new Error(`Cannot add PlugboardConnections '${newPlugboardConnection}', contains letter already used in active connection.`);
		} else {
			this.connectionsList.push(newPlugboardConnection);
		};
	};

	
	removeConnection(plugboardConnectionToRemove) {
		numberOfConnectionInstancesInList = this.connectionsList.reduce((a, v) => (v === plugboardConnectionToRemove ? a + 1 : a), 0);

		if (numberOfConnectionInstancesInList === 0) {
			throw new Error(`Tried to remove connection '${plugboardConnectionToRemove}', not in connectionsList '${self.connectionsList}'.`);
		} else if (numberOfConnectionInstancesInList > 1) {
			throw new Error(`Failed to remove connection '${plugboardConnectionToRemove}' from connectionsList '${self.connectionsList}'. Too many instances of connection, must not be more than one.`);
		} else {
			this.connectionsList.split(plugboardConnectionToRemove);
		};
	};


	removeConnectionByLetter(targetLetter) {
		connectionToDelete = this.getConnectionByLetter(targetLetter)
		if (connectionToDelete !== None) {
			this.removeConnection(connectionToDelete);
			return true;
		} else {
			return false;
		};
	}
};

let testPlugboardConnection = new PlugboardConnection('A', 'B');
console.log(testPlugboardConnection.checkForLetter('A'));

