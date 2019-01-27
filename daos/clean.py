from daos import dog_dao


def _get_all_description(column):
    query = """
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


weight_mins = [7, 50, 55, 65, 75, 24, 6, 40, 57, 25, 80, 35, 40, 12, 22, 40, 18, 45, 65, 17, 60, 40, 40, 70, 10, 55, 80,
               80, 45, 100, 30, 11.5, 60, 10, 69, 50, 25, 50, 30, 8, 50, 40, 110, 13, 35, 90, 25, 13, 55, 6, 5, 45, 50,
               45, 18, 55, 50, 8, 60, 16, 40, 18, 65, 99, 26, 45, 55, 45, 50, 40, 8, 45, 35, 33, 23, 60, 28, 25, 75, 45,
               45, 65, 35, 55, 45, 110, 85, 85, 60, 35, 7, 45, 20, 60, 25, 45, 105, 7, 4, 35, 33, 70, 70, 55, 17, 100,
               13, 8, 4, 12, 175, 25, 11, 8, 12, 13, 110, 100, 11, 26, 48, 13, 12, 35, 60, 80, 4, 13, 14, 27, 25, 45,
               40, 30, 3, 45, 9, 35, 14, 25, 15, 8, 45, 70, 80, 120, 35, 35, 10, 75, 18, 23, 20, 17, 9, 35, 8, 25, 15,
               30, 31, 62, 24, 35, 35, 22, 80, 9, 18, 3.5, 6, 45, 45, 55, 35, 20, 15, 20, 15, 50, 9, 7]

weight_maxs = [9, 60, 55, 115, 85, 28, 40, 65, 67, 45, 150, 45, 65, 14, 24, 60, 30, 55, 85, 23, 65, 75, 65, 120, 16, 75,
               145, 90, 80, 180, 45, 15.5, 105, 25, 90, 80, 40, 100, 40, 10, 70, 50, 130, 14, 55, 130, 38, 18, 80, 6,
               12, 60, 90, 70, 26, 85, 75, 15, 70, 32, 60, 24, 90, 110, 34, 65, 75, 75, 65, 50, 14, 65, 50, 53, 36, 70,
               28, 35, 95, 70, 75, 90, 35, 75, 80, 180, 115, 140, 70, 60, 13, 50, 40, 70, 27, 65, 120, 14, 7, 45, 40,
               80, 115, 80, 17, 170, 15, 18, 6, 22, 190, 33, 11, 10, 18, 15, 150, 150, 12, 40, 55, 16, 12, 52, 90, 115,
               9, 17, 14, 27, 35, 55, 60, 35, 7, 65, 13, 60, 18, 35, 30, 25, 65, 85, 135, 200, 65, 65, 16, 110, 22, 24,
               20, 23, 16, 60, 11, 40, 19, 40, 48, 82, 38, 45, 45, 35, 150, 15, 24, 7, 8, 65, 65, 90, 50, 20, 21, 40,
               19, 60, 35, 7]

height_mins = [9.5, 25, 23, 23, 23, 13.5, 9, 21, 17, 15, 27, 17, 18, 10, 16, 14, 13, 20, 24, 15.5, 22, 22, 22, 23, 9.5,
               23, 26, 23, 21, 22, 18, 10, 28, 15, 23.5, 21, 14, 22, 17.5, 9, 21, 12, 24, 9.5, 19, 23.5, 10.5, 12, 21,
               6, 11, 18, 22, 17, 17.5, 17, 22, 9, 23, 8, 19, 8, 24, 23, 15, 23, 23, 23, 24, 18, 10, 16, 17, 18, 15.5,
               22, 11, 17, 22, 21, 24, 23.5, 12.5, 21.5, 23, 21, 25, 23.5, 26, 19, 8.5, 22.5, 16.5, 25, 18, 21, 30, 13,
               8, 16, 17.5, 25.5, 26, 21.5, 13.5, 25.5, 10, 12, 9, 15, 27.5, 10, 5, 10, 10, 12, 24, 26, 9, 16, 19.5, 12,
               10, 17, 21, 24, 8, 12, 6, 10, 13, 21, 20, 17, 8, 21, 8, 17, 10, 16, 15, 10, 21, 24, 22, 25.5, 23, 19, 10,
               30, 10, 10.5, 13, 13.5, 8, 20, 9, 9.5, 15.5, 17.19, 15.75, 22, 14, 17.5, 13, 11.5, 24, 10, 15, 8.5, 10,
               20, 21, 23, 17, 15, 10, 18, 15.5, 20, 10, 8]

height_maxs = [11.5, 27, 23, 28, 25, 15.5, 19, 25, 19, 18, 29, 20, 23, 11, 17, 14, 13, 22, 27.5, 16.5, 26, 26, 26, 27.5,
               11.5, 25, 30, 27, 27, 27, 23, 11, 30, 17, 27.5, 25, 18, 27, 20.5, 11, 22, 15, 27, 10, 24, 27.5, 12.5, 13,
               26, 9, 13, 20, 26, 20, 19.5, 20, 26, 11, 27, 9, 23, 11, 28, 27, 17, 26, 27, 28, 25, 21, 11, 21, 18, 21,
               20, 24.5, 13, 20, 26, 25, 26, 27.5, 14, 24, 27, 35, 32, 28.5, 29, 21, 11.5, 27.5, 18, 27, 18, 24, 32, 15,
               11, 19, 19.5, 27.5, 30, 24.5, 14.5, 31.5, 11, 14, 11, 16, 30, 14, 6, 12.5, 15, 14, 31, 28, 10, 18.5,
               20.5, 15, 10, 21, 22, 27, 11, 14, 9, 12, 15, 25, 25, 20, 11, 21, 12, 23, 11, 17, 20.5, 18, 27, 27, 27,
               27.5, 28, 23.5, 13, 32, 10, 10.5, 16, 16.5, 11, 23.5, 10, 10, 15.5, 17.19, 19.75, 27, 16, 19.5, 15, 13.5,
               26, 10, 16, 11, 12, 27, 24, 27, 19, 15.5, 11, 22, 15.5, 24, 23, 9]


def add_wt_ht():
    dumb_list = [('weight_max', weight_maxs), ('height_min', height_mins), ('height_max', height_maxs)]

    for col_name, list_of_values in dumb_list:
        print('\nstarting: ', col_name)

        query = """
            UPDATE dog
            SET {weight_or_height} = %(wt_ht_value)s
            WHERE id = %(dog_id)s;
            """.format(weight_or_height=col_name)

        for idx, value in enumerate(list_of_values):
            dog_id = idx + 1
            print('updating dog_id: {}'.format(dog_id))
            with dog_dao._get_cursor() as cursor:
                cursor.execute(query, {'wt_ht_value': value, 'dog_id': dog_id})
