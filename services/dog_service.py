import logging
import random
import re

from daos import dog_dao

log = logging.getLogger()
log.setLevel(logging.INFO)


def sanitize_string(user_string):
    user_string = user_string.lower().strip()
    user_string = re.sub('[^a-zA-Z ]+', '', user_string)
    return user_string


def get_dog_description(dog_name):
    dog_name = sanitize_string(dog_name)
    log.info('dog name is: {}'.format(dog_name))
    dog_information = dog_dao.get_dog_by_name(dog_name)
    return dog_information['description']


def get_random_dog_and_description():
    random_dog_id = random.randint(1,182)
    dog_info = dog_dao.get_dog_by_id(random_dog_id)
    return {'breed': dog_info['name'], 'description': dog_info['description']}


def get_alexa_dog(energy_level, playfulness, affection, training, weight):
    energy_level_range = _text_to_range_mapper(energy_level)
    playfulness_range = _text_to_range_mapper(playfulness)
    affection_range = _text_to_range_mapper(affection)
    # Flip training for better phrasing in alexa
    if training == 'low':
        training = 'high'
    elif training == 'high':
        training = 'low'
    training_range = _text_to_range_mapper(training)
    weight_min, weight_max = _get_weight_range(weight)

    dog_info = dog_dao.get_dog_by_criteria(energy_level=energy_level_range,
                                           playfulness=playfulness_range,
                                           affection=affection_range,
                                           training=training_range,
                                           weight_min=weight_min,
                                           weight_max=weight_max)
    if not dog_info:
        return {
            'breed': 'None',
            'description': 'None',
            'personality': 'None',
            'history': 'None'
        }

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
        'medium': (2, 3, 4),
        'high': (4, 5)
    }
    return mapping[text_to_map]


def _get_weight_range(weight):
    mapping = {
        'small': (0, 20),
        'medium': (20, 60),
        'large': (60, 100),
        'jumbo': (100, 5000)
    }
    return mapping[weight]


def _get_random_index(count_of_dogs):
    return random.randint(0, count_of_dogs-1)


def _get_params_from_react_data(answers):
    params = []
    for param_dict in answers:
        temp_params = []
        for param, isActive in param_dict.items():
            if isActive:
                temp_params.append(param)
        if not temp_params:
            temp_params = [1, 2, 3, 4, 5]
        params.append(tuple(temp_params))
    return params


def get_breeds(answers):
    energy_params, playful_params, friendliness_to_dogs_params = _get_params_from_react_data(answers)
    raw_dog_info = dog_dao.get_breeds_by_criteria(energy_level=energy_params,
                                                  playfulness=playful_params,
                                                  friendliness_to_dogs=friendliness_to_dogs_params,
                                                  affection=(1, 2, 3, 4, 5),
                                                  training=(1, 2, 3, 4, 5),
                                                  weight_min=0,
                                                  weight_max=300)
    dog_info = {dog['id']: dog['name'] for dog in raw_dog_info}
    return dog_info


fake_data = [
  {
    "1": False,
    "2": False,
    "3": False,
    "4": True,
    "5": True
  },
  {
    "1": False,
    "2": True,
    "3": False,
    "4": True,
    "5": True
  }
]
