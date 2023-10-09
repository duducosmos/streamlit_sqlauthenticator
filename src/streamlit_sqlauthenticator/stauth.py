""" stauth - Authenticator for Streamlit using pydal to save user info in database.
"""
import re
import bcrypt

from .model import model


__AUTHOR = "Eduardo S. Pereira"
__EMAIL = "eduardo.spereira@sp.senai.br"
__DATE = "09/10/2023"

__version__ = "0.1.0"

REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


class STAuth:
    def __init__(self, dbinfo, folder):
        self._model = model(dbinfo, folder)
        self._logged = False

    @property
    def database(self):
        return self._model

    @property
    def logged(self):
        return self._logged

    def login(self, user: str, password: str):
        "Verify if user exist in database"
        query = self.database(self.database.users.username == user)
        user_info = query.select(self.database.users.password).first()
        if user_info is not None:
            if bcrypt.checkpw(password.encode("utf8"), user_info.password.encode("utf8")):
                if self._logged is False:
                    self._logged = True
                return True
        return False

    def logout(self):
        if self._logged is True:
            self._logged = False

    def create_user(self, username: str, password: str, email: str):
        "Create a user"
        query = self.database(self.database.users.username == username)

        user_info = query.select(self.database.users.ALL).first()
        if user_info is None:
            if re.fullmatch(REGEX, email) is False:
                return {"id": None,
                        "created": False,
                        "error": "Invalid email"
                        }

            query = self.database(self.database.users.email == email)
            user_info = query.select(self.database.users.ALL).first()
            if user_info is not None:
                return {"id": None,
                        "created": False,
                        "error": "E-mail already registered"
                        }
            hashedpass = bcrypt.hashpw(
                password.encode("utf8"), bcrypt.gensalt())
            user = self.database.users.insert(
                username=username,
                email=email,
                password=hashedpass,
            )
            self.database.commit()
            return {"id": user,
                    "created": True,
                    "error": None}

        return {"id": None,
                "created": False,
                "error": "User exist"}
