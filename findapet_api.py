from flask import Flask

from daos import dog_dao
from services import dog_service

app = Flask(__name__)


@app.route('/')
def hello_world():
    dogs = dog_dao.hello_world_query()
    return str(dogs[0])


@app.route('/dog/<string:dog_name>')
def dog_description(dog_name):
    return dog_service.get_dog_description(dog_name)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
