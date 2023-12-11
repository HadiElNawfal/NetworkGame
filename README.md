# NetworkGame

This README provides instructions on how to run the Client and Proxy Server codes.

## Table of Contents

 [NetworkGame](#Network-game)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Installation Steps](#installation-steps)
  - [Running the Codes](#running-the-codes)
  - [Description](#Description)

## Installation

### Prerequisites

Before installing Scapy, make sure you have the following prerequisites:

1. **Python**: Scapy requires Python 3.x. Make sure you have Python installed on your system. You can download Python from the official website: [Python Downloads](https://www.python.org/downloads/).

2.   **Pip**: Pip is the package manager for Python. It's usually included with Python, so you should have it available. You can check if Pip is installed by running `pip --version` in your terminal/command prompt.

### Installation Steps

1. Through your terminal or command prompt, install Scapy using pip by running the following command: `pip install scapy`. This will download and install Scapy and its dependencies.


2. You can clone both codes, once the installation is complete, using the command: git clone https://github.com/HadiElNawfal/NetworkGame


## Running the Codes

1. Run the Server code by typing `python Server.py` in a command prompt in the file's directory.

2. Run the Client code by typing `python Client.py` in a command prompt in the file's directory.

## Description
* A server should be set up and waiting for player connections to initiate the game.
* The server establishes a protocol for client-server communication to meet the game conditions.
* Upon connection, the server sends a welcome message to the client, confirming the successful connection to the game server.
* The game logic is implemented on the server side.
*  When all players are connected, the server generates a random number from 0 to 9 and sends it to player 1.
* Player 1 receives the number and must type it as fast as possible, then press send.
* The server checks the received number's correctness and calculates the Round Trip Time (RTT) from sending the number to receiving the echo back.
* This process repeats for all players.
* Players who enter the wrong number are disqualified from the current round.
* This sequence repeats over three rounds.
* After each round, the server displays detailed results, including individual round scores and cumulative scores for each player, in descending order.
* After three rounds, the server declares the winner based on cumulative scores and closes the connection.








