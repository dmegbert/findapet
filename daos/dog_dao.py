import logging

import psycopg2
from psycopg2.extras import RealDictCursor

from config import DatabaseConfig


log = logging.getLogger()
log.setLevel(logging.INFO)


def _get_connection(conn_str=None):
    if not conn_str:
        endpoint, database, dbuser, password, port = DatabaseConfig.get_connection_params()
        conn_str = "host={0} dbname={1} user={2} password={3} port={4}".format(
            endpoint, database, dbuser, password, port)
    conn = psycopg2.connect(conn_str)
    conn.autocommit = True
    return conn


def _get_cursor():
    connection = _get_connection()
    return connection.cursor(cursor_factory=RealDictCursor)


def hello_world_query():
    query = """SELECT * FROM dog where playfulness = %(playfulness)s"""

    with _get_cursor() as cursor:
        cursor.execute(query, {'playfulness': 5})
        return cursor.fetchall()


def get_dog_by_name(dog_name):
    query = """
    SELECT *
    FROM dog
    WHERE LOWER(name) = %(dog_name)s
    """

    with _get_cursor() as cursor:
        cursor.execute(query, {'dog_name': dog_name})
        return cursor.fetchone()


def get_dog_by_id(dog_id):
    query = """
    SELECT id, name, description, history, personality
    FROM dog
    WHERE id = %(dog_id)s
    """

    with _get_cursor() as cursor:
        cursor.execute(query, {'dog_id': dog_id})
        return cursor.fetchone()


def get_dog_by_criteria(energy_level, playfulness, affection, training, weight_min, weight_max):
    query = """
        SELECT *
        FROM dog
        WHERE energy_level IN %(energy_level)s
            AND playfulness IN %(playfulness)s
            AND affection_level IN %(affection)s
            AND ease_of_training IN %(training)s
            AND weight_max >= %(weight_min)s
            AND weight_max <= %(weight_max)s
        """

    params = {
        'energy_level': energy_level,
        'playfulness': playfulness,
        'affection': affection,
        'training': training,
        'weight_min': weight_min,
        'weight_max': weight_max
    }

    with _get_cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()


def get_breeds_by_criteria(energy_level, playfulness, friendliness_to_dogs, affection, training, weight_min, weight_max):
    query = """
        SELECT *
        FROM dog
        WHERE energy_level IN %(energy_level)s
            AND playfulness IN %(playfulness)s
            AND friendliness_to_dogs IN %(friendliness_to_dogs)s
            AND affection_level IN %(affection)s
            AND ease_of_training IN %(training)s
            AND weight_max >= %(weight_min)s
            AND weight_max <= %(weight_max)s
        """

    params = {
        'energy_level': energy_level,
        'playfulness': playfulness,
        'friendliness_to_dogs': friendliness_to_dogs,
        'affection': affection,
        'training': training,
        'weight_min': weight_min,
        'weight_max': weight_max
    }

    with _get_cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()
