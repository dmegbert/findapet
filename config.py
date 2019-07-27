from os import environ
from dotenv import load_dotenv


# Database Config
ENDPOINT = environ.get('ENDPOINT')
PORT = environ.get('PORT')
DBUSER = environ.get('DBUSER')
PASSWORD = environ.get('DBPASSWORD')
DATABASE = environ.get('DATABASE')


class DatabaseConfig:
    @staticmethod
    def get_connection_params():
        load_dotenv()
        return ENDPOINT, DATABASE, DBUSER, PASSWORD, PORT
