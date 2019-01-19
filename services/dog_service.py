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
