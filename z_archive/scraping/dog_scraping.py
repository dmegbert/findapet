from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import shutil

import requests
from bs4 import BeautifulSoup

_url = "https://www.petfinder.com/{}"
_user_agent = """Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"""

_headers = {'user-agent': _user_agent}


def main_imgs():
    links = get_all_breed_links()
    get_imgs(links)


def main():
    links = get_all_breed_links()
    fieldnames = get_individual_dog_data(links[0]).keys()
    all_dogs = [get_individual_dog_data(link).values() for link in links]
    with open('dogs.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(fieldnames)
        writer.writerows(all_dogs)


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


def download_img(img_src, img_alt):
    resp = requests.get(img_src, _headers, stream=True)
    with open(f'/Users/egbert/projects/findapet/img/{img_alt}.jpg', 'wb') as file:
        resp.raw.decode_content = True
        shutil.copyfileobj(resp.raw, file)


def get_imgs(links):
    dupes = set()
    for idx, link in enumerate(links):
        print(idx, link)
        page = _get_content(link, _headers)
        for img_elem in page.find_all('img'):
            if img_elem['src'] not in dupes:
                img_src = img_elem['src'].split('?')[0]
                alt_text = img_elem.get('alt', 'no alt')
                alt_text = alt_text.replace('/', '')
                download_img(img_src, alt_text)
            dupes.add(img_elem['src'])


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
    }
    """
    dog = {}
    html_content = _get_content(breed_url, _headers)
    dog['name'] = [tag.text for tag in html_content.find_all('h1') if tag.text][0]
    print(dog['name'])
    dog['form_and_function'] = [tag.p.string for tag in html_content.find_all('div', class_='txt') if tag.find_all('p')][0]

    out_of_five_attributes = _get_out_of_five_attributes(html_content)
    dog = _set_out_of_five_attributes(dog_data=dog, out_of_five_attributes=out_of_five_attributes)

    dog = _get_type_family_other_names(dog, html_content)
    dog['other_names'] = dog.get('other_names', ' ')
    dog = _split_weight(dog)
    dog = _split_height(dog)

    # Taking Health out for now
    # dog['health'] = _get_dog_health(html_content, dog, breed_url)
    try:
        dog['history'], dog['temperament'], dog['upkeep'] = _split_out_history_temperament_upkeep(html_content)
    except ValueError:
        print(f'Not enough history, temp, upkeep values for {dog["name"]}')
        dog['history'], dog['temperament'], dog['upkeep'] = ('', '', '')
    return dog


def _split_weight(dog):
    if not dog['weight']:
        return dog
    weight = dog['weight'].replace('lb', '').strip()
    if '-' in weight:
        dog['weight_min'], dog['weight_max'] = weight.split('-')
    else:
        dog['weight_min'], dog['weight_max'] = (weight, weight)
    del dog['weight']
    return dog


def _split_height(dog):
    if not dog['height']:
        return dog
    height = dog['height'].replace('"', '').strip()
    if '-' in height:
        dog['height_min'], dog['height_max'] = height.split('-')
    else:
        dog['height_min'], dog['height_max'] = (height, height)
    del dog['height']
    return dog


def _split_out_history_temperament_upkeep(html_content):
    history_temp_up = _get_history_temperament_upkeep(html_content)
    if len(history_temp_up) > 3:
        history = ''
        while len(history_temp_up) > 2:
            history = history + history_temp_up.pop(0)
        temperament, upkeep = history_temp_up
        return history, temperament, upkeep
    else:
        return history_temp_up


def _get_dog_health(html_content, dog=None, breed_url=None):
    dog_health = {}
    for tag in html_content.find_all('div', class_='m-wysiwyg_txtLoose'):
        for inner_tag in tag.find_all('li'):
            key_and_value = inner_tag.string
            try:
                key, value = key_and_value.split(':')
            except ValueError as ex:
                print(dog['name'], ': ', breed_url)
                print('\tkey_and_value: ', key_and_value)
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


def _get_history_temperament_upkeep(html_content):
    history_temperament_upkeep = []
    for tag in html_content.find_all('div', class_='m-wysiwyg_txtLoose'):
        for inner_tag in tag.find_all('p'):
            if inner_tag.string:
                history_temperament_upkeep.append(inner_tag.string)
    return history_temperament_upkeep


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


if __name__ == '__main__':
    main()
