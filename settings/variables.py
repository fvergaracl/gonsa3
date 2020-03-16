#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

config_host = os.getenv('_host')
config_port = os.getenv('_port')


_jwt_secret_key = os.getenv('_jwt_secret_key')

_db_user = os.getenv('_db_user')
_db_pass = os.getenv('_db_pass')
_db_host = os.getenv('_db_host')
_db_databasename = os.getenv('_db_databasename')

_email_sender = os.getenv('_email_sender')
_email_passw = os.getenv('_email_passw')