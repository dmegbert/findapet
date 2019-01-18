import psycopg2
from psycopg2.extras import RealDictCursor

import logging
from os import environ

endpoint = environ.get('ENDPOINT')
port = environ.get('PORT')
dbuser = environ.get('DBUSER')
password = environ.get('DBPASSWORD')
database = environ.get('DATABASE')

query = """SELECT * FROM public.dog where playfulness = %(playfulness)s"""

log = logging.getLogger()
log.setLevel(logging.INFO)


def get_connection(conn_str=None):
    if not conn_str:
        conn_str = "host={0} dbname={1} user={2} password={3} port={4}".format(
            endpoint, database, dbuser, password, port)
    conn = psycopg2.connect(conn_str)
    conn.autocommit = True
    return conn


def get_cursor():
    connection = get_connection()
    return connection.cursor(cursor_factory=RealDictCursor)


def basic_query():
    with get_cursor() as cursor:
        cursor.execute(query, {'playfulness': 5})
        return cursor.fetchall()
