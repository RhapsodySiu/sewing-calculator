import json
from flask import Flask

env = 'development'

config_path = f"../config/{env}.json"
with open(config_path) as f:
    config = json.load(f)

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True, host=config['apiHost'], port=config['apiPort'])
