# NetworkGame
## Server
* There must be a server waiting for user to request to play the game (the choice of
how many players is up to you (at least 2). Also, the protocol to connect to the
server is kept up to you, as long as you meet all the conditions). Once a connection
is established, the server should send a welcome message to the client, telling
them that they've connected to the game server.
* The clients should connect to the server and wait for the welcome message.
* The game logic should be implemented on the server side. When all players
connect, the server will create a random number (from 0 to 9) and send it to player
1; the number will be displayed on his/her screen. Player 1 must type the same
number and press send as fast as possible. Upon receipt, the server will check if it
is correct and calculate the total RTT from the time it sent the number until it
receives the echo back. This will be repeated to all players. The detailed results
will be displayed on the screen in descending order. Players pressing the wrong
number are disqualified from this round. This will be repeated over three rounds.
After each round, the results of the current round and the cumulative scores of
each player in descending order must be displayed. After the three rounds, the
server should declare the winner and close the connection.

## Client
Clients connect to the server and wait for the welcome message.

The game's logic is implemented on the server side. When all players are connected, the server generates a random number (ranging from 0 to 9) and transmits it to player 1, displaying the number on their screen. Player 1 must swiftly input the same number and send it back. Upon receiving the response, the server checks its accuracy and calculates the Round-Trip Time (RTT) from the moment the number was sent until the echo is received. This process is repeated for all players. The detailed outcomes are then showcased on the screen in descending order. Players entering the wrong number are disqualified from the round. This procedure recurs over three rounds.

At the conclusion of each round, the results for that specific round and the cumulative scores of all players (in descending order) are displayed. After three rounds, the server announces the winner and terminates the connection.






