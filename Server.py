#Server Code

import socket
import random
import time
import tabulate
disqualified = 1000
no_input = 1001

def server(host,port):

    players = [] #list for score at each round
    cum_scores = {} #dictionary for cumulative score
    player_sockets = []#list for players' sockets
    score = 0
    nb_player = 1

    # Create welcoming socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to specified port
    serversocket.bind((host, port))

    # server listening to incoming requests
    print("Ready to serve")
    serversocket.listen(1000)#The game supports any number of players (if they join before the timeout period expires)
    serversocket.settimeout(10)#sets a ten second timer for the players to connect to the game
    while True:
        try:
            connectionsocket, addr = serversocket.accept()
            connectionsocket.sendall("Welcome, you are now connected to the game server".encode())#prints a welcome message on the players' screens
            players.append([addr,score, nb_player])#append with each player's address, score(initialized to zero) and their number(in order of whoever joins first)
            cum_scores[nb_player] = 0
            player_sockets.append(connectionsocket)
            nb_player += 1#increment the number assigned to the player
            print("A player joined")#a message is printed whenever a new player joins the game
        except socket.timeout:
            print("Timeout for connection")#prints when the timeout expires
            break

    if nb_player<3:#if either one or less players connected
        string = "no game"
        if nb_player == 2:#if only one player is connected
            player_sockets[0].send(string.encode())#string "no game" is sent to the one player connected
            player_sockets[0].close()#close socket
    else:#in case there are a sufficient number of players connected
        for i in range(3):#creates a loop for the three rounds of the game
            for j in range(len(players)):#loop for each player separately
                players[j][1] = 0 # reset the player's round score(RTT) to 0
                x=str(random.randint(0,9))#generate a random number
                #The code was sending the random number and the previous results of the round together in the same send statement
                #so we added a small 1 second delay between each round
                time.sleep(0.1)
                try:
                    player_sockets[j].send(x.encode())#the random number is sent to the player
                    send_time_ms = time.time() #start timer to calculate RTT
                except socket.error:#exception in case the player disconnects
                    player_sockets.pop(j)
                    players.pop(j)
                    string = "disconnected"
                    for x in range(len(players)):#loop to send each player that player j has disconnected and close connections
                        player_sockets[x].send(string.encode())
                        time.sleep(0.1)
                        player_sockets[x].send(str(j).encode())
                        player_sockets[x].close()
                    serversocket.close()#game stops
                    exit()
                player_sockets[j].settimeout(10)#timeout for players to send back the number
                try:
                    playernb=str(player_sockets[j].recv(2048).decode())#number received from player
                    if playernb:
                        recv_time_ms = time.time()
                        rtt_in_ms = round(recv_time_ms - send_time_ms, 3)
                        if playernb.strip() == x:
                            players[j][1] += rtt_in_ms #add rtt of player i
                        else:
                            players[j][1] += disqualified #The player is disqualified
                    else:
                        players[j][1] += disqualified

                except socket.timeout:#exception in case the player did not send back the number before the timout expires
                    players[j][1] += no_input#"no input" would appeasr in the player's score fragment of the round

                except socket.error:#exception if player disconnects
                    player_sockets.pop(j)
                    players.pop(j)
                    string = "disconnected"
                    for x in range(len(players)):
                        player_sockets[x].send(string.encode())
                        time.sleep(0.1)
                        player_sockets[x].send(str(j).encode())
                        player_sockets[x].close()
                    serversocket.close()
                    exit()

            round_score = sorted(players, key = lambda players: (players[1]))#sort the players according to their scores
            nb_disqualified = 0

            for z in range(len(players)):#loop to count number of disqualified players
                if players[z][1] == disqualified or players[z][1] == no_input:
                    nb_disqualified += 1

            #if not all players are disqualified
            if nb_disqualified != len(players):
                cum_scores[round_score[0][2]] += 1
            results = []
            for z in range(len(players)):#print current round scores
                if players[z][1] == disqualified:
                    results.append([players[z][2], "Wrong Input!"])
                elif players[z][1] == no_input:
                    results.append([players[z][2], "No Input!"])
                else:
                    results.append([players[z][2],players[z][1]])


            for z in range(len(players)):
                try:
                    time.sleep(0.1)
                    results = str(results)
                    player_sockets[z].sendall(results.encode())#send results to players
                except socket.error:#exception if player disconnects
                    player_sockets.pop(z)
                    players.pop(z)
                    string = "disconnected"
                    for x in range(len(players)):
                        player_sockets[x].send(string.encode())
                        time.sleep(0.1)
                        player_sockets[x].send(str(z).encode())
                        player_sockets[x].close()
                    serversocket.close()
                    exit()
            #append cumulative scores into a list and sort it in descending order
            results1 = []
            for z in range(1,len(players)+1):
                results1.append([z,cum_scores[z]])
            results1.sort(key = lambda results1: (results1[1]))
            results1=str(results1[::-1])
            for z in range(len(players)):
                try:
                    player_sockets[z].send(results1.encode())#sends cumulative scores
                except socket.error:#exception if player disconnects
                    player_sockets.pop(z)
                    players.pop(z)
                    string = "disconnected"
                    for x in range(len(players)):
                        player_sockets[x].send(string.encode())
                        time.sleep(0.1)
                        player_sockets[x].send(str(z).encode())
                        player_sockets[x].close()
                    serversocket.close()
                    exit()

        #When all rounds are finished, puts all the winners in an array
        winners = [k for k, v in cum_scores.items() if v == max(cum_scores.values())]

        y = str(len(winners))
        w = '-1'
        for i in range(len(players)):
            time.sleep(0.1)
            try:
                if players[i][2] in winners:
                    player_sockets[i].send(y.encode()) #sending the number of winners to the clients
                else:
                    player_sockets[i].send(w.encode())
            except socket.error:
                player_sockets.pop(i)
                players.pop(i)
                string = "disconnected"
                for x in range(len(players)):
                    player_sockets[x].send(string.encode())
                    time.sleep(0.1)
                    player_sockets[x].send(str(i).encode())
                    player_sockets[x].close()
                serversocket.close()
                exit()

        if len(winners) == 1:#if there is only one winner (no draw)
            string = f'The winner of the game is player {winners[0]}'
            #send the final results
            time.sleep(0.1)
            for z in range(len(players)):
                try:
                    player_sockets[z].send(string.encode())
                except socket.error:
                    player_sockets.pop(z)
                    players.pop(z)
                    string = "disconnected"
                    for x in range(len(players)):
                        player_sockets[x].send(string.encode())
                        time.sleep(0.1)
                        player_sockets[x].send(str(z).encode())
                        player_sockets[x].close()
                    serversocket.close()
                    exit()
        #in case there is a draw, we can find all the winners. Make the winners play a tie breaker round.

        else:
            for i in range(len(winners)):
                winners[i] = str(winners[i])
            string = 'There is a draw between the following players: '
            string += ','.join(winners)
            string += '\nWe are going to have a final round with the players that drew.\nThe winner takes it all!'
            time.sleep(0.1)

            for z in range(len(players)):
                try:
                    player_sockets[z].send(string.encode())
                except socket.error:
                    player_sockets.pop(z)
                    players.pop(z)
                    string = "disconnected"
                    for x in range(len(players)):
                        player_sockets[x].send(string.encode())
                        time.sleep(0.1)
                        player_sockets[x].send(str(z).encode())
                        player_sockets[x].close()
                    serversocket.close()
                    exit()

    ######################################################################################
            for i in range(len(winners)):
                winners[i] = int(winners[i])


            # temp1 = []
            # temp1 = players
            # temp2 = []
            # temp2 = player_sockets

            for k in range(len(players)):
                if players[k][2] not in winners:
                    player_sockets[k].close()
                    players.remove(k)
                    player_sockets.remove(k)

            for j in range(len(players)):
                players[j][1] = 0
                x2=str(random.randint(0,9))
                #The code was sending the random number and the previous results of the round together in the same send statement
                #so we added a small 1 second delay between each round
                time.sleep(0.1)
                try:
                    player_sockets[j].send(x2.encode())
                    send_time_ms = time.time() #start timer to calculate RTT
                except socket.error:
                    player_sockets.pop(z)
                    players.pop(z)
                    string = "disconnected"
                    for x in range(len(players)):
                        player_sockets[x].send(string.encode())
                        time.sleep(0.1)
                        player_sockets[x].send(str(z).encode())
                        player_sockets[x].close()
                    serversocket.close()
                    exit()

                player_sockets[j].settimeout(10)
                try:
                    playernb=str(player_sockets[j].recv(2048).decode())#number recieved from player
                    if playernb:
                        recv_time_ms = time.time()
                        rtt_in_ms = round(recv_time_ms - send_time_ms, 3)
                        if playernb.strip() == x2:
                            players[j][1] += rtt_in_ms #add rtt of player i
                        else:
                            players[j][1] += disqualified #The player is disqualified
                    else:
                        players[j][1] += disqualified

                except socket.timeout:
                    players[j][1] += no_input

                except socket.error:
                    player_sockets.pop(z)
                    players.pop(z)
                    string = "disconnected"
                    for x in range(len(players)):
                        player_sockets[x].send(string.encode())
                        time.sleep(0.1)
                        player_sockets[x].send(str(z).encode())
                        player_sockets[x].close()
                    serversocket.close()
                    exit()

            round_score = sorted(players, key = lambda players: (players[1]))
            nb_disqualified = 0

            for z in range(len(players)):
                if players[z][1] == disqualified or players[z][1] == no_input:
                    nb_disqualified += 1

            if nb_disqualified != len(players):
                cum_scores[round_score[0][2]] += 1
            results=[]
            for z in range(len(players)):#print current round scores
                if players[z][1] == disqualified:
                    results.append([players[z][2], "Wrong Input!"])
                elif players[z][1] == no_input:
                    results.append([players[z][2], "No Input!"])
                else:
                    results.append([players[z][2],players[z][1]])

            for z in range(len(players)):
                try:
                    results = str(results)
                    player_sockets[z].sendall(results.encode())
                except socket.error:
                    player_sockets.pop(z)
                    players.pop(z)
                    string = "disconnected"
                    for x in range(len(players)):
                        player_sockets[x].send(string.encode())
                        time.sleep(0.1)
                        player_sockets[x].send(str(z).encode())
                        player_sockets[x].close()
                    serversocket.close()
                    exit()
            results1=[]

            for z in range(1,len(players)+1):
                results1.append([z,cum_scores[z]])

            results1.sort(key = lambda results1: (results1[1]))
            results1=str(results1[::-1])

            for z in range(len(players)):
                try:
                    player_sockets[z].send(results1.encode())
                except socket.error:
                    player_sockets.pop(z)
                    players.pop(z)
                    string = "disconnected"
                    for x in range(len(players)):
                        player_sockets[x].send(string.encode())
                        time.sleep(0.1)
                        player_sockets[x].send(str(z).encode())
                        player_sockets[x].close()
                    serversocket.close()
                    exit()
            #Add all winners of tie breaker round in list winner2
            winner2 = [k for k, v in cum_scores.items() if v == max(cum_scores.values())]
            if len(winner2) == 1:
                string = f'The winner of the game is player {winner2[0]}'
            elif len(winner2) > 1:#In case there was another tie, declare that the game ended with a tie
                for i in range(len(winner2)):
                    winner2[i] = str(winner2[i])
                string = 'There is a draw between the following players: '
                string += ','.join(winner2)
                string += '\nThank you for playing!'
            if nb_disqualified != len(players):
                for z in range(len(players)):
                    time.sleep(0.1)
                    try:
                        player_sockets[z].send(string.encode())
                    except socket.error:
                        player_sockets.pop(z)
                        players.pop(z)
                        string = "disconnected"
                        for x in range(len(players)):
                            player_sockets[x].send(string.encode())
                            time.sleep(0.1)
                            player_sockets[x].send(str(z).encode())
                            player_sockets[x].close()
                        serversocket.close()
                        exit()
            else:#If all players were disqualified, the game ends with a draw.
                string = "Everyone was disqualified, so the game ends in a draw."
                for z in range(len(players)):
                    time.sleep(0.1)
                    try:
                        player_sockets[z].send(string.encode())
                    except socket.error:
                        player_sockets.pop(z)
                        players.pop(z)
                        string = "disconnected"
                        for x in range(len(players)):
                            player_sockets[x].send(string.encode())
                            time.sleep(0.1)
                            player_sockets[x].send(str(z).encode())
                            player_sockets[x].close()
                        serversocket.close()
                        exit()


        for z in range(len(players)):
            player_sockets[z].close()
    #################################################################################################

    serversocket.close()

server('localhost',8080)
