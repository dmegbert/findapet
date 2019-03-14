import logging

from flask import Flask, jsonify, request
from flask_cors import CORS

from daos import dog_dao
from services import dog_service

app = Flask(__name__)
CORS(app)

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
    logging.info('url params are: {}'.format(request.args))
    dog_info = dog_service.get_alexa_dog(
        energy_level=request.args.get('energy_level'),
        playfulness=request.args.get('playfulness'),
        affection=request.args.get('affection'),
        training=request.args.get('training'),
        weight=request.args.get('weight')
    )
    return jsonify(dog_info)


@app.route('/dog/breed_count', methods=['POST'])
def breed_count():
    logging.info('Data is {}'.format(request.json['data']))
    answers = request.json['data']['answers']
    weights = (request.json['data']['weight']['minimum'], request.json['data']['weight']['maximum'])
    breeds = dog_service.get_breeds(answers=answers, weights=weights)
    logging.info('Breeds are: {}'.format(breeds))
    return jsonify(breeds)


@app.route('/dog/<int:dog_id>')
def single_dog_info(dog_id):
    return jsonify(dog_dao.get_dog_by_id(dog_id=dog_id))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
