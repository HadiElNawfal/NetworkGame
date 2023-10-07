# NetworkGame
## Server
* A server should be set up and waiting for player connections to initiate the game.
* The server establishes a protocol for client-server communication to meet the game conditions.
* Upon connection, the server sends a welcome message to the client, confirming the successful connection to the game server.
* The game logic is implemented on the server side.
** When all players are connected, the server generates a random number from 0 to 9 and sends it to player 1.
* Player 1 receives the number and must type it as fast as possible, then press send.
* The server checks the received number's correctness and calculates the Round Trip Time (RTT) from sending the number to receiving the echo back.
* This process repeats for all players.
* Players who enter the wrong number are disqualified from the current round.
* This sequence repeats over three rounds.
* After each round, the server displays detailed results, including individual round scores and cumulative scores for each player, in descending order.
* After three rounds, the server declares the winner based on cumulative scores and closes the connection.

## Client
Clients connect to the server and wait for the welcome message.

The game's logic is implemented on the server side. When all players are connected, the server generates a random number (ranging from 0 to 9) and transmits it to player 1, displaying the number on their screen. Player 1 must swiftly input the same number and send it back. Upon receiving the response, the server checks its accuracy and calculates the Round-Trip Time (RTT) from the moment the number was sent until the echo is received. This process is repeated for all players. The detailed outcomes are then showcased on the screen in descending order. Players entering the wrong number are disqualified from the round. This procedure recurs over three rounds.

At the conclusion of each round, the results for that specific round and the cumulative scores of all players (in descending order) are displayed. After three rounds, the server announces the winner and terminates the connection.






