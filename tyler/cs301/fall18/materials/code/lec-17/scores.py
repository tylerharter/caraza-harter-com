# key: player's name
# val: player's score
scores = {}

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
            # TODO: sanity checking
            name = cmd[1]
            score = int(cmd[2])
            scores[name] = score
        elif cmd[0] == 'get':
            # TODO: sanity checking
            name = cmd[1]
            print(scores[name])
        elif cmd[0] == 'high':
            scores_list = []
            for x in scores:
                scores_list.append(scores[x])
            best = max(scores_list)
            print('max:', best)

            # TODO: loop over players again,
            # print those who tied for the max

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
