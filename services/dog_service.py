import random
import re

from daos import dog_dao


def sanitize_string(user_string):
    user_string = user_string.lower().strip()
    user_string = re.sub('[^a-zA-Z ]+', '', user_string)
    return user_string


def get_dog_description(dog_name):
    dog_name = sanitize_string(dog_name)
    dog_information = dog_dao.get_dog_by_name(dog_name)
    return dog_information['description']


def get_random_dog_and_description():
    random_dog_id = random.randint(1,182)
    dog_info = dog_dao.get_dog_by_id(random_dog_id)
    return {'breed': dog_info['name'], 'description': dog_info['description']}


def get_alexa_dog(energy_level):
    energy_level_range = _text_to_range_mapper(energy_level)
    dog_info = dog_dao.get_dog_by_criteria(energy_level=energy_level_range)
    return {'breed': dog_info[0]['name'], 'description': dog_info[0]['description']}


def _text_to_range_mapper(energy_level):
    mapping = {
        'low': (1, 2),
        'medium': (3, 4),
        'high': (4, 5)
    }
    return mapping[energy_level]
