import logging

from flask import Flask, jsonify, request

from daos import dog_dao
from services import dog_service

app = Flask(__name__)

log = logging.getLogger()
log.setLevel(logging.INFO)


@app.route('/')
def hello_world():
    dogs = dog_dao.hello_world_query()
    return str(dogs[0])


@app.route('/dog/<string:dog_name>')
def dog_description(dog_name):
    return dog_service.get_dog_description(dog_name)


@app.route('/dog/random')
def random_dog():
    return jsonify(dog_service.get_random_dog_and_description())


@app.route('/dog/alexa')
def alexa_dog():
    logging.info('url params are: {}'.format(request.args.get('energy_level')))
    dog_info = dog_service.get_alexa_dog(energy_level=request.args.get('energy_level'))
    return jsonify(dog_info)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
