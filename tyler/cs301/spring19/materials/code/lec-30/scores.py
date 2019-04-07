import json, sys
from flask import Flask, request, jsonify

app = Flask(__name__)

scores = {}

@app.route('/')
def index():
    return "<pre>" + "\n".join([
        '# replace PORT below',
        '',
        '# to increment a score, do the following:',
        'r = requests.post("http://localhost:PORT/scores", "alice")',
        'r.raise_for_status()',
        'r.text',
        '',
        '# get the scores, do the following:',
        'r = requests.get("http://localhost:PORT/scores")',
        'r.raise_for_status()',
        'r.json()',
    ]) + "</pre>"

@app.route('/scores', methods=['GET', 'POST'])
def scores_handler():
    if request.method == 'GET':
        return json.dumps(scores)
    elif request.method == 'POST':
        player = str(request.get_data(), encoding="utf-8")
        if player == "":
            return "fail"
        if player in scores:
            scores[player] += 1
        else:
            scores[player] = 1
        return "success"

    return "fail"

port = 8080
if len(sys.argv) == 2:
    port = int(sys.argv[1])
app.run(port=port)
