scores = {"alice": 0, "bob": 0}

def main():
    global scores

    while True:
        cmd = input('your cmd: ')
        cmd = cmd.strip().lower().split(' ')

        if cmd[0] == 'q':
            break

        elif cmd[0] == 'high':
            # PASS 1: find one best player
            best_key = None
            for key in scores:
                val = scores[key]
                if best_key == None or scores[key] > scores[best_key]:
                    best_key = key

            # PASS 2: find everybody who tied with them
            winners = []
            for key in scores:
                val = scores[key]
                if val == scores[best_key]:
                    winners.append(key)

            if len(winners) == 1:
                print("Winner is", winners[0])
            else:
                winner_str = ", ".join(winners)
                print("Tie between ", winner_str)

        elif cmd[0] == 'help':
            print_help()
            
        elif cmd[0] == 'set':
            name = cmd[1]
            score = int(cmd[2])
            scores[name] = score
            print(scores)

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
