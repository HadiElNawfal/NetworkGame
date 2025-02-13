# RTT Game

This README provides instructions on how to run the Client and Proxy Server codes.

## Table of Contents

 [RTT Game](#rtt-game)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Installation Steps](#installation-steps)
  - [Running the Codes](#running-the-codes)
  - [Description](#Description)
  - [Features](#features)
  - [Limitations and Possible Enhancements](#limitations-and-possible-enhancements)
    - [Limitations](#limitations)
    - [Enhancements](#enhancements)

## Installation

### Prerequisites

Before installing Scapy, make sure you have the following prerequisites:

1. **Python**: Scapy requires Python 3.x. Make sure you have Python installed on your system. You can download Python from the official website: [Python Downloads](https://www.python.org/downloads/).

2. **Pip**: Pip is the package manager for Python. It's usually included with Python, so you should have it available. You can check if Pip is installed by running `pip --version` in your terminal/command prompt.

### Installation Steps

1. Through your terminal or command prompt, install the requirements using pip by running the following command:
```
pip install -r requirements.txt
```

This will download and install Scapy and its dependencies.


2. You can clone both codes, once the installation is complete, using the command:
```
git clone https://github.com/HadiElNawfal/NetworkGame
```

## Running the Codes

1. Run the Server code by typing the following in a terminal in the file's directory:
```
python Server.py
```

2. Run the Client code by typing the following in a terminal in the file's directory:
```
python Client.py
```

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

## Features
* Multiple Rounds: The game runs for three rounds, allowing players to compete repeatedly.
* Real-Time RTT Calculation: Each round trip is timed to measure how quickly players respond.
* Disqualification Mechanic: If a player enters an incorrect number, they are disqualified for that round.
* Score Tracking: Scores are maintained across all rounds, providing a final ranking.
* Server-Client Architecture: Clear separation between the server (game logic) and the client (user interface).

## Limitations and Possible Enhancements
### Limitations:
The game currently supports a fixed number of rounds (three). Extending or customizing the number of rounds requires code modifications.
No database or persistent storage for game results; all scores reset once the server process ends.
Limited input validation on the client side.

### Possible Enhancements:
* Dynamic Round Configuration: Allow a variable number of rounds, configurable via command-line arguments or a settings file.
* GUI/Front-End: Replace the command-line interface with a graphical interface for better user interaction.
* Multi-Client Support: Expand the server to handle more concurrent clients or dynamic player counts.
* Persistent Scoreboard: Store game results in a database or file system for historical tracking.
* Security Improvements: Add authentication, encryption (e.g., TLS), and better error handling to prevent invalid inputs or malicious connections.
* Cross-Platform Packaging: Create executables or Docker containers for easier deployment.

## Sample Output (Client)
```
Welcome, you are now connected to the game server

Round 1:

Random Number: 9
Enter the number you received: 9

Round Results:
╒══════════╤═══════╕
│   Player │   RTT │
╞══════════╪═══════╡
│        1 │ 1.637 │
├──────────┼───────┤
│        2 │ 2.74  │
╘══════════╧═══════╛

Scores so far:
╒══════════╤═════════╕
│   Player │   Score │
╞══════════╪═════════╡
│        1 │       1 │
├──────────┼─────────┤
│        2 │       0 │
╘══════════╧═════════╛

Round 2:

Random Number: 3
Enter the number you received: 3

Round Results:
╒══════════╤═══════╕
│   Player │   RTT │
╞══════════╪═══════╡
│        1 │ 2.947 │
├──────────┼───────┤
│        2 │ 2.488 │
╘══════════╧═══════╛

Scores so far:
╒══════════╤═════════╕
│   Player │   Score │
╞══════════╪═════════╡
│        2 │       1 │
├──────────┼─────────┤
│        1 │       1 │
╘══════════╧═════════╛

Round 3:

Random Number: 3
Enter the number you received: 3

Round Results:
╒══════════╤═══════╕
│   Player │   RTT │
╞══════════╪═══════╡
│        1 │ 2.698 │
├──────────┼───────┤
│        2 │ 2.743 │
╘══════════╧═══════╛

Scores so far:
╒══════════╤═════════╕
│   Player │   Score │
╞══════════╪═════════╡
│        1 │       2 │
├──────────┼─────────┤
│        2 │       1 │
╘══════════╧═════════╛

Final Results: The winner of the game is player 1
```

## Sample Output (Server)
```
Ready to serve
A player joined
A player joined
Timeout for connection
```









