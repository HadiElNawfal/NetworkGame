#Client Code

import socket
import select
import time
from inputimeout import inputimeout, TimeoutOccurred
import tabulate


server = 'localhost'
#equivalent to setting sever='localhost'
#we need to run client and server on the same machine
#if on different machines, server=ip of that machine
port = 8080

#connect to server
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((server,port))

#recv welcome message
welcomeMessage = clientSocket.recv(2048).decode()
print(welcomeMessage)

#loop for 3 rounds
for round in range(1,4):
    try:
        #receive random nb
        time.sleep(0.1)
        randNumb = clientSocket.recv(2048).decode()
        print(f"\nRound {round}:")#print the round number
        if randNumb == "no game":#sent by server if there are not enough players
            print("Not enough players")
            clientSocket.close()
            exit()
        print(f"\nRandom Number: {randNumb}")
    except socket.error as error:
            print("An error occurred:",error)
            clientSocket.close()
            exit()
    try:
        #input answer and send it
        roundAnswer = inputimeout("Enter the number you received: ",10)
        # Send the input to the server
        clientSocket.send(roundAnswer.encode())


    except TimeoutOccurred:#print message if timeout expires before the player sends back the number
        print("Oops! You ran out of time. Try to be faster next time!")

    except socket.error as error:
            print("An error occurred:",error)
            clientSocket.close()
            exit()
    try:
        #receive result
        col_names = ["Player", "RTT"]
        roundResults = clientSocket.recv(2048).decode('utf-8')
        if roundResults == "disconnected":
            disconnected_player = clientSocket.recv(2048).decode()#receive a message that a player has disconnected
            disconnected_player = int(disconnected_player)+1
            print(f"Player {disconnected_player} has disconnected")
            clientSocket.close()#game ends in that case
            exit()
        roundResults = eval(roundResults)
        print(f"\nRound Results:")
        print(tabulate.tabulate(roundResults,col_names,tablefmt="fancy_grid"))#print table with RTT of current round
        scores_so_far = clientSocket.recv(2048).decode('utf-8')
        if roundResults == "disconnected":
            disconnected_player = clientSocket.recv(2048).decode()
            disconnected_player = int(disconnected_player)+1
            print(f"Player {disconnected_player} has disconnected")
            exit()
        scores_so_far = eval(scores_so_far)
        print(f"\nScores so far:")
        col_names1 = ["Player", "Score"]
        print(tabulate.tabulate(scores_so_far,col_names1,tablefmt="fancy_grid"))#print table with scores
    except socket.error as error:
            print("An error occurred:",error)
            clientSocket.close()
            exit()

try:
    nbWinners = clientSocket.recv(2048).decode() #receive number of winners
    if roundResults == "disconnected":
            disconnected_player = clientSocket.recv(2048).decode()
            disconnected_player = int(disconnected_player)+1
            print(f"Player {disconnected_player} has disconnected")
            clientSocket.close()
            exit()
except socket.error as error:
    print("An error occured:",error)
    clientSocket.close()
    exit()

if int(nbWinners) == 1:
    try:
        #receive final result
        finalResults = clientSocket.recv(2048).decode()
        if roundResults == "disconnected":
            disconnected_player = clientSocket.recv(2048).decode()
            disconnected_player = int(disconnected_player)+1
            print(f"Player {disconnected_player} has disconnected")
            clientSocket.close()
            exit()
        print(f"\nFinal Results: {finalResults}")
    except socket.error as error:
            print("An error occurred:",error)

elif int(nbWinners) > 1:#in case of a draw

    try:
        drawMsg = clientSocket.recv(2048).decode()
        if roundResults == "disconnected":
            disconnected_player = clientSocket.recv(2048).decode()
            disconnected_player = int(disconnected_player)+1
            print(f"Player {disconnected_player} has disconnected")
            clientSocket.close()
            exit()
        print(drawMsg)
    except socket.error as error:
        print("An error occurred:",error)

    try:
        #receive random nb
        time.sleep(0.1)
        randNumb = clientSocket.recv(2048).decode()
        if roundResults == "disconnected":
            disconnected_player = clientSocket.recv(2048).decode()
            disconnected_player = int(disconnected_player)+1
            print(f"Player {disconnected_player} has disconnected")
            clientSocket.close()
            exit()
        print("\nFinal Round:")
        print(f"\nRandom Number: {randNumb}")
    except socket.error as error:
            print("An error occurred:",error)
            clientSocket.close()
            exit()
    try:
        #input answer and send it
        roundAnswer = inputimeout("Enter the number you received: ",10)
        clientSocket.sendall(roundAnswer.encode())
    except TimeoutOccurred:
        print("Timeout")
    except socket.error as error:
            print("An error occurred:",error)
            clientSocket.close()
            exit()
    try:
        #receive result
        col_names = ["Player", "RTT"]
        roundResults = clientSocket.recv(2048).decode('utf-8')
        if roundResults == "disconnected":
            disconnected_player = clientSocket.recv(2048).decode()
            disconnected_player = int(disconnected_player)+1
            print(f"Player {disconnected_player} has disconnected")
            clientSocket.close()
            exit()
        roundResults = eval(roundResults)
        print(f"\nRound Results:")
        col_names1 = ["Player", "Score"]
        print(tabulate.tabulate(roundResults,col_names1,tablefmt="fancy_grid"))
        scores_so_far = clientSocket.recv(2048).decode('utf-8')
        if roundResults == "disconnected":
            disconnected_player = clientSocket.recv(2048).decode()
            disconnected_player = int(disconnected_player)+1
            print(f"Player {disconnected_player+1} has disconnected")
            clientSocket.close()
            exit()
        scores_so_far = eval(scores_so_far)
        print(f"\nScores so far:")
        print(tabulate.tabulate(scores_so_far,col_names,tablefmt="fancy_grid"))
    except socket.error as error:
            print("An error occurred:",error)
            clientSocket.close()
            exit()

    try:
        #receive final result
        finalResults = clientSocket.recv(2048).decode()
        if roundResults == "disconnected":
            disconnected_player = clientSocket.recv(2048).decode()
            disconnected_player = int(disconnected_player)+1
            print(f"Player {disconnected_player} has disconnected")
            clientSocket.close()
            exit()
        print(f"\nFinal Results: {finalResults}")
    except socket.error as error:
            print("An error occurred:",error)

else:
    print("You lost!")

#close connection with server
clientSocket.close()
