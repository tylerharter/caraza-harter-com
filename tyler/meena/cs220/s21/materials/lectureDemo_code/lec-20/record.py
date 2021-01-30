# STEP 1: Copy and paste code for reading JSON file.

import json
import sys

def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f) # dict, list, etc

 
# STEP 2: Copy and paste code for writing JSON file. 
#         Eliminate duplicate import.

# data is a dict, list, etc
def write_json(path, data):
    with open(path, 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# STEP 3: Process player name, player score as a command line
#         arguments using sys module.
player_name = sys.argv[1]
player_score = float(sys.argv[2])

# STEP 4: Define an empty "scores" dictionary to keep track of players'
#         scores.
#         KEY: player name VALUE: player scores list

inputFile = "score_history.json"
scores = read_json(inputFile)

# STEP 5: Check if player name is a key in the scores dictionary.
#         If not, create a new key for player name and value as empty list
#         to keep track of that player's scores.

if player_name not in scores:
    scores[player_name] = []

# STEP 6: Add player's score to the player's list in scores dictionary
scores[player_name].append(player_score)
print(scores)

# STEP 7: Create a "score_history.json" file and popluate that file with
#         empty dictionary {}

# STEP 8: Read "score_history.json" to populate initial "scores" dict, 
#         instead of the empty dict created in STEP 4.

# STEP 9: Calculate average score for that player
print(sum(scores[player_name]) / len(scores[player_name]))

# STEP 10: At the end of the program, write the updated scores from dict
#         into the "scores_history.json" file

write_json(inputFile, scores)

# STEP 11: That's it, now you have a program that helps you keep track 
#          of player scores permanently.
