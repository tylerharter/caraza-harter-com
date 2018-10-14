alice = 0
bob = 0

def main():
    global alice, bob

    while True:
        cmd = input('enter a cmd (type "help" for descriptions): ')
        cmd = cmd.strip().lower().split(' ')
        if cmd[0] == 'q':
            break
        if cmd[0] == 'help':
            print_help()
        if cmd[0] == 'set':
            # TODO: sanity checking
            name = cmd[1]
            score = int(cmd[2])
            if name == 'alice':
                alice = score
            elif name == 'bob':
                bob = score
            else:
                print('must be alice or bob')
        elif cmd[0] == 'get':
            # TODO: sanity checking
            name = cmd[1]
            if name == 'alice':
                print(alice)
            elif name == 'bob':
                print(bob)
            else:
                print('must be alice or bob')
        elif cmd[0] == 'high':
            if alice > bob:
                print("Alice:", alice)
            elif bob > alice:
                print("Bob:", bob)
            else:
                print("tie")

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
