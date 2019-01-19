from os import environ

# Database Config
ENDPOINT = environ.get('ENDPOINT')
PORT = environ.get('PORT')
DBUSER = environ.get('DBUSER')
PASSWORD = environ.get('DBPASSWORD')
DATABASE = environ.get('DATABASE')


class DatabaseConfig:
    @staticmethod
    def get_connection_params():
        return ENDPOINT, DATABASE, DBUSER, PASSWORD, PORT
