source .venv/bin/activate
export PYTHONPATH=/home/deploy/
FLASK_APP=/home/deploy/api/src/nlp_api/run.py FLASK_DEBUG=1 flask run --host=0.>
deactivate
