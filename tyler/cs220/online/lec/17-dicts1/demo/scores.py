# key: a player's name, val: their score
scores = {}

def main():
    global alice, bob

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
            print(scores)

        elif cmd[0] == 'get':
            name = cmd[1]
            if name in scores:
                score = scores[name]
                print(score)
            else:
                print("unknown name")

        elif cmd[0] == 'high':
            # STEP 1: find the highest score
            highest = 0
            for name in scores:
                score = scores[name]
                if score > highest:
                    highest = score

            # STEP 2: find all people that had that score
            print("Winner(s):")
            for name in scores:
                score = scores[name]
                if score == highest:
                    print(name)

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
