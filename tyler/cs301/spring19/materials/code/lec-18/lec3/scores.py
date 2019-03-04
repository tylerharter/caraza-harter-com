#alice = 0
#bob = 0

scores = {"alice": 0, "bob": 0}
# instead of alice variable
# scores["alice"]

def main():
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
                print(scores[name])
            else:
                print("not found")

        elif cmd[0] == 'high':
            best_key = None
            for key in scores:
                if best_key == None or scores[key] > scores[best_key]:
                    best_key = key
            print("winner", best_key)

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
