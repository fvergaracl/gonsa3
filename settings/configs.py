
# -*- coding: utf-8 -*-
import datetime, re
from settings.variables import _jwt_secret_key, _db_user, _db_pass, _db_host, _db_databasename, _email_sender, \
    _email_passw, config_host, config_port


class Config:

    def __init__(self):
        self.api_debug = True
        self.api_port = config_port
        self.api_host = config_host

        self.jwt_secret_key = _jwt_secret_key
        self.api_jwt_time = datetime.timedelta(days=30)

    def get_api_debug(self):
        return self.api_debug

    def get_api_port(self):
        return self.api_port

    def get_api_host(self):
        return self.api_host

    def get_jwt_secret_key(self):
        return self.jwt_secret_key

    def get_api_jwt_time(self):
        return self.api_jwt_time


class Config_email_sender:

    def __init__(self):
        self.email = _email_sender
        self.passw = _email_passw

    def get_email(self):
        return self.email

    def get_passw(self):
        return self.passw


class Database:
    config = None

    def __init__(self):
        # To connect BD
        self.user = _db_user
        self.password = _db_pass
        self.host = _db_host
        self.database_name = _db_databasename

        # DB
        self.config = {'user': self.user,
                       'password': self.password,
                       'host': self.host,
                       'database': self.database_name}


class Passeq:
    """
    Se define los requisitos para las contrasenas
    """

    def __init__(self):
        self.mayus = True
        self.mins = True
        self.leng = 6 # largo minimo
        self.somenum = False # debe tener numero
        self.extrach = False # carateres extras como ! " · $ % & / ( ) = _ ^ * ¡ ... [PENDIENTE]
        self.com_prev = False # Comparar con las contraseñas anteriores [PENDIENTE]

    def checkpass(self, pass_):
        if len(pass_) < self.leng:
            return False, "La contraseña ingresada debe tener %i caracteres como mínimo" % self.leng
        elif self.somenum and re.search('[0-9]', pass_) is None:
            return False, "La contraseña ingresada debe tener como mínimo un número"
        elif self.mayus and re.search('[A-Z]', pass_) is None:
            return False, "La contraseña ingresada debe tener como mínimo una mayúsculas"
        elif self.mins and re.search('[a-z]', pass_) is None:
            return False, "La contraseña ingresada debe tener como mínimo una minúsculas"
        else:
            return True, "Contraseña ok"


if __name__ == '__main__':
    print(_db_user)
    print(_db_pass)
    print(_db_host)
    print(_db_databasename)