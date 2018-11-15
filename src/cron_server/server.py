"""The main entrypoint for running the Flask server."""
import flask
import os
from uuid import uuid4

app = flask.Flask(__name__)
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', True)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', str(uuid4()))
app.url_map.strict_slashes = False  # allow both `get /v1/` and `get /v1`


@app.route('/', methods=['GET'])
def root():
    """Server status."""
    print('hi!')
    with open('.git/refs/heads/master', 'r') as fd:
        commit_hash = fd.read().strip()
    repo_url = 'https://github.com/kbaseIncubator/cron_server.git'
    return flask.jsonify({'commit_hash': commit_hash, 'repo_url': repo_url})
