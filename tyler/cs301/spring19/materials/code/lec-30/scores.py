import json
from flask import Flask, request, jsonify

app = Flask(__name__)

scores = {}

@app.route('/')
def index():
    return "<pre>" + "\n".join([
        '# to increment a score, do the following:',
        'r = requests.post("http://localhost:5000/scores", "alice")',
        'r.raise_for_status()',
        'r.text',
        '',
        '# get the scores, do the following:',
        'r = requests.get("http://localhost:5000/scores")',
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

app.run()
