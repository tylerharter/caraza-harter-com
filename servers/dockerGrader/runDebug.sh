. venv/bin/activate
export FLASK_APP=testServer.py
export FLASK_ENV=development
python -m flask run --host=0.0.0.0
deactivate
