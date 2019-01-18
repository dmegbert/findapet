import json
from flask import Flask

from dao import basic_query

app = Flask(__name__)


@app.route('/')
def hello_world():
    dogs = basic_query()
    return str(dogs)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
