from flask import Flask

from daos.dog_dao import basic_query

app = Flask(__name__)


@app.route('/')
def hello_world():
    dogs = basic_query()
    return str(dogs[0])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
