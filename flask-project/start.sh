source env/bin/activate
export FLASK_CONFIG=config.TestingConfig
export FLASK_DEBUG=1
export FLASK_APP=run.py
flask run
