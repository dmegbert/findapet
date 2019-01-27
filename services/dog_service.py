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


def get_alexa_dog(energy_level, playfulness, affection):
    energy_level_range = _text_to_range_mapper(energy_level)
    playfulness_range = _text_to_range_mapper(playfulness)
    affection_range = _text_to_range_mapper(affection)

    dog_info = dog_dao.get_dog_by_criteria(energy_level=energy_level_range,
                                           playfulness=playfulness_range,
                                           affection=affection_range)

    random_dog_index = _get_random_index(len(dog_info))
    return {
        'breed': dog_info[random_dog_index]['name'],
        'description': dog_info[random_dog_index]['description'],
        'personality': dog_info[random_dog_index]['personality'],
        'history': dog_info[random_dog_index]['history']
    }


def _text_to_range_mapper(text_to_map):
    mapping = {
        'low': (1, 2),
        'medium': (3, 4),
        'high': (4, 5)
    }
    return mapping[text_to_map]


def _get_random_index(count_of_dogs):
    return random.randint(0, count_of_dogs-1)
