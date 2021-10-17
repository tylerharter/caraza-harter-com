#KEY: player name VALUE: player score
scores = {"bob":0, "alice"    :   0}

def main():
    global scores

    while True:
        cmd = input('enter a cmd (type "help" for descriptions): ')
        cmd = cmd.strip().lower().split(' ')

        if cmd[0] == 'q':
            break
        
        elif cmd[0] == 'help':
            print_help()
            
        elif cmd[0] == 'set':
            name = cmd[1]
            score = int(cmd[2])
            scores[name] = score

        elif cmd[0] == 'get':
            name = cmd[1]
            if name in scores:
                print(scores[name])
            else:
                print("unknown name")
        
        elif cmd[0] == 'high':
            # PASS 1: find the best score
            best_player = None
            for player in scores:
                if best_player == None or scores[player] > scores[best_player]:
                    best_player = player

            # PASS 2: find all players with the best score
            winners = []
            for player in scores:
                if scores[player] == scores[best_player]:
                    winners.append(player)

            if len(winners) == 1:
                print ("Only winner is:", winners[0])
            else:
                tie = ", ".join(winners)
                print("Tie for win between:", tie)

    print('exiting')


def print_help():
    print('Commands:')
    print('help')
    print('  print list of commands')
    print('set <name> <score>')
    print('  updates score of player with given name')
    print('get <name>')
    print('  updates score of player with given name')    
    print('high')
    print('  print high score')
    print('q')
    print('  quit program')


main()
