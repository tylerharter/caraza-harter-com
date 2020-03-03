scores = {"alice": 0, "bob": 0}

def main():
    while True:
        cmd = input('cmd: ')
        cmd = cmd.lower().strip().split(' ')
        print("CMD", cmd)

        if cmd[0] == 'q':
            break

        elif cmd[0] == 'high':
            # PASS 1: Find the best score
            best_key = None
            for key in scores:
                if best_key == None or scores[key] > scores[best_key]:
                    best_key = key

            # PASS 2: Find all players with the best score
            winners = []
            for key in scores:
                val = scores[key]
                if val == scores[best_key]:
                    winners.append(key)
                    
            if len(winners) == 1:
                print("the only winner is", winners[0])
            else:
                tie_str = ", ".join(winners)
                print("tie for win between", tie_str)

        
        elif cmd[0] == 'help':
            print_help()
            
        elif cmd[0] == 'set':
            name = cmd[1]
            score = int(cmd[2])
            scores[name] = score
            print("DICT:", scores)

        elif cmd[0] == 'get':
            name = cmd[1]
            print(scores[name])

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
