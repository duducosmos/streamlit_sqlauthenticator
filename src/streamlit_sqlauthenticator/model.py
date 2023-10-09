from pydal import DAL, Field
import os

__AUTHOR = "Eduardo S. Pereira"
__EMAIL = "eduardo.spereira@sp.senai.br"
__DATE = "09/10/2023"

__version__ = "0.1.0"


def model(dbinfo, folder):
    """Model Initialization"""

    os.makedirs(folder, exist_ok=True)

    database = DAL(dbinfo, db_codec='UTF-8',
                   folder=folder, pool_size=1)

    if 'users' in database.tables:
        print('Users Table Exist...')
    else:
        create_user_table(database)

    return database


def create_user_table(database):
    database.define_table("users",
                          Field("username", "string", unique=True),
                          Field("email", "string", unique=True),
                          Field("password", "string"),
                          Field("role", "string", default="guest")
                          )
