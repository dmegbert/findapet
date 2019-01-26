from daos import dog_dao


def _get_all_description(column):
    query="""
    SELECT name, {}
    FROM dog;
    """.format(column)

    with dog_dao._get_cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()

    return {result['name']: result[column] for result in results}

    # giant_string = ''
    # for text in all_text:
    #     giant_string = giant_string + text[column]
    # return giant_string


def get_bad_chars(column):
    query_dict = _get_all_description(column)
    bad_chars_and_dogs = {}
    for id, text in query_dict.items():
        all_bad_chars = [letter for letter in text if ord(letter) > 128]
        if all_bad_chars:
            bad_chars_and_dogs[id] = set(all_bad_chars)
    return bad_chars_and_dogs


bad_chars = {
    '¬†': ' ',
    '‚Äô': "'",
    '‚Äú': '"',
    '¬æ': '.75',
    '‚Ä≥': '"',
    '‚Äî': '--',
    '√∂': 'ö',
    '‚Äù': '"',
    '‚Äì': '--',
    '√©': 'é',
    '√≠': 'í',
    '√®': 'è',
    '‚Äò': "'",
    '√§': 'ä',
    '√≥': 'ó',
    '‚Ä¢': ''
}


def replace_bad(desc):
    for bad_char, good_char in bad_chars.items():
        desc = desc.replace(bad_char, good_char)
    return desc


def fix_description():
    select_query = """
    SELECT description
    FROM dog WHERE id = %(dog_id)s
    """

    update_query = """
    UPDATE dog 
    SET description = %(updated_description)s
    WHERE id = %(dog_id)s
    """

    for dog_id in range(1, 183):
        bad_description = ''
        with dog_dao._get_cursor() as cursor:
            cursor.execute(select_query, {'dog_id': dog_id})
            bad_description = cursor.fetchone()['description']

        fixed_desc = replace_bad(bad_description)
        print(dog_id, ' ', fixed_desc, '\n')

        with dog_dao._get_cursor() as cursor:
            cursor.execute(update_query, {'dog_id': dog_id, 'updated_description': fixed_desc})

    print('Hooray!')


def fix_history():
    select_query = """
    SELECT history
    FROM dog WHERE id = %(dog_id)s
    """

    update_query = """
    UPDATE dog 
    SET history = %(updated_description)s
    WHERE id = %(dog_id)s
    """

    for dog_id in range(1, 183):
        bad_description = ''
        with dog_dao._get_cursor() as cursor:
            cursor.execute(select_query, {'dog_id': dog_id})
            bad_description = cursor.fetchone()['history']

        fixed_desc = replace_bad(bad_description)
        print(dog_id, ' ', fixed_desc, '\n')

        with dog_dao._get_cursor() as cursor:
            cursor.execute(update_query, {'dog_id': dog_id, 'updated_description': fixed_desc})

    print('Hooray!')


def fix_care_overview():
    select_query = """
    SELECT care_overview
    FROM dog WHERE id = %(dog_id)s
    """

    update_query = """
    UPDATE dog 
    SET care_overview = %(updated_description)s
    WHERE id = %(dog_id)s
    """

    for dog_id in [66, 105]:
        bad_description = ''
        with dog_dao._get_cursor() as cursor:
            cursor.execute(select_query, {'dog_id': dog_id})
            bad_description = cursor.fetchone()['care_overview']

        fixed_desc = replace_bad(bad_description)
        print(dog_id, ' ', fixed_desc, '\n')

        with dog_dao._get_cursor() as cursor:
            cursor.execute(update_query, {'dog_id': dog_id, 'updated_description': fixed_desc})

    print('Hooray!')
