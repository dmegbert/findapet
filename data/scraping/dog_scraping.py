import requests
from bs4 import BeautifulSoup

_url = "https://www.petfinder.com/{}"
_user_agent = """Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"""

_headers = {'user-agent': _user_agent}


def _get_content(url, headers, url_param=None):
    resp = requests.get(url.format(url_param), headers=headers)
    return BeautifulSoup(resp.content, 'html.parser')


def get_all_breed_links():
    """
    Scrapes the petfinder site and returns a list of strings of each individual breed's url

    :return: ['https://www.petfinder.com/dog-breeds/{breed}']
    """
    html_content = _get_content(_url, _headers, url_param='dog-breeds/?page=1')
    all_breed_links = []
    for link in html_content.find_all('a'):
        if link.get('href') and 'https://www.petfinder.com/dog-breeds' in link.get('href'):
            all_breed_links.append(link.get('href'))
    return sorted(set(all_breed_links))


def get_individual_dog_data(breed_url):
    """
    Gets a dictionary of data on a specific dog breed. Takes a url as a required parameter.

    :param breed_url: str https://www.petfinder.com/dog-breeds/{breed}

    :return: {
                name: str,
                form_and_function: str,
                energy_level: int,
                exercise_requirements: int,
                playfulness: int,
                affection_level: int,
                friendliness_to_dogs: int,
                friendliness_to_other_pets: int,
                friendliness_to_strangers: int,
                watchfulness: int,
                ease_of_training: int,
                grooming_requirements: int,
                heat_sensitivity: int,
                vocality: int,

                type: str,
                weight: {min: float, max float},
                height: {min: float, max float},
                family: str,
                area_of_origin: str,
                date_of_origin: str,
                other_names: str,

                history: str,
                temperament: str,
                upkeep: str
                health: {
                            major_concerns: [],
                            minor_concerns: [],
                            occasionally_seen: [],
                            suggested_tests: [],
                            life_span: {min: int, max int},
                            note: str
                        }
    }
    """
    dog = {}
    html_content = _get_content(breed_url, _headers)
    dog['name'] = [tag.text for tag in html_content.find_all('h1') if tag.text][0]
    dog['form_and_function'] = [tag.p.string for tag in html_content.find_all('div', class_='txt') if tag.find_all('p')][0]

    out_of_five_attributes = _get_out_of_five_attributes(html_content)
    dog = _set_out_of_five_attributes(dog_data=dog, out_of_five_attributes=out_of_five_attributes)

    dog = _get_type_family_other_names(dog, html_content)
    dog['health'] = _get_dog_health(html_content)

    # TODO Fix history and add temperament and upkeep
    deog['history'] = _get_history(html_content)
    dog['temperament'] = None
    dog['upkeep'] = None



    return dog


def _get_dog_health(html_content):
    dog_health = {}
    for tag in html_content.find_all('div', class_='m-wysiwyg_txtLoose'):
        for inner_tag in tag.find_all('li'):
            key_and_value = inner_tag.string
            key, value = key_and_value.split(':')
            key = key.replace(' ', '_').lower()
            value = value.strip()
            dog_health[key] = value
    return dog_health


def _get_type_family_other_names(dog, html_content):
    family_keys = []
    family_values = []
    for tag in html_content.find_all('div', class_="card-section"):
        for inner_tag in tag.find_all('h3', class_='m-txt_sm'):
            family_key = inner_tag.string.lower().replace(' ', '_')
            family_keys.append(family_key)
        for inner_tag_2 in tag.find_all('p', class_='m-txt_lg'):
            family_values.append(inner_tag_2.string)

    for idx, key in enumerate(family_keys):
        dog[key] = family_values[idx]
    return dog


def _get_history(html_content):
    history = ''
    for tag in html_content.find_all('div', class_='m-wysiwyg_txtLoose'):
        for inner_tag in tag.find_all('p'):
            if inner_tag.string:
                history = history + inner_tag.string
    return history

def _get_out_of_five_attributes(html_content):
    out_of_five_attributes = []
    for tag in html_content.find_all('span', class_='u-isVisuallyHidden'):
        if '5' in tag.string:
            out_of_five_attributes.append(int(tag.string.strip()[0]))
    return out_of_five_attributes


def _set_out_of_five_attributes(dog_data, out_of_five_attributes):
    if len(out_of_five_attributes) == 12:
        dog_data['energy_level'] = out_of_five_attributes[0]
        dog_data['exercise_requirements'] = out_of_five_attributes[1]
        dog_data['playfulness'] = out_of_five_attributes[2]
        dog_data['affection_level'] = out_of_five_attributes[3]
        dog_data['friendliness_to_dogs'] = out_of_five_attributes[4]
        dog_data['friendliness_to_other_pets'] = out_of_five_attributes[5]
        dog_data['friendliness_to_strangers'] = out_of_five_attributes[6]
        dog_data['watchfulness'] = out_of_five_attributes[7]
        dog_data['ease_of_training'] = out_of_five_attributes[8]
        dog_data['grooming_requirements'] = out_of_five_attributes[9]
        dog_data['heat_sensitivity'] = out_of_five_attributes[10]
        dog_data['vocality'] = out_of_five_attributes[11]
    elif len(out_of_five_attributes) == 11:
        # Watchfulness is missing on American Eskimo Dog and maybe others...
        dog_data['energy_level'] = out_of_five_attributes[0]
        dog_data['exercise_requirements'] = out_of_five_attributes[1]
        dog_data['playfulness'] = out_of_five_attributes[2]
        dog_data['affection_level'] = out_of_five_attributes[3]
        dog_data['friendliness_to_dogs'] = out_of_five_attributes[4]
        dog_data['friendliness_to_other_pets'] = out_of_five_attributes[5]
        dog_data['friendliness_to_strangers'] = out_of_five_attributes[6]
        dog_data['ease_of_training'] = out_of_five_attributes[7]
        dog_data['grooming_requirements'] = out_of_five_attributes[8]
        dog_data['heat_sensitivity'] = out_of_five_attributes[9]
        dog_data['vocality'] = out_of_five_attributes[10]
    return dog_data
