#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding=utf-8  
import mysql.connector
from settings.configs import Database
from functions.general import encrypt_pass, random_salt

def get_salt_of_user(user_):
    try:
        database_ = Database()
        config = database_.config
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        query = "SELECT salt FROM users WHERE (nickname = %s or email = %s)"
        data = (user_,user_,)
        cursor.execute(query, data)
        r = ''
        for (salt) in cursor:
            print(str(salt[0]))
            r = str(salt[0])
            return r
        cursor.close()
        cnx.close()
        return r
    except Exception as e:
        print('Error #1 en la base de datos')
        print(e)
        return 'Error #1 en la base de datos'

def login_user(user_, passw_):
    try:
        database_ = Database()
        config = database_.config
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        salt = get_salt_of_user(user_)
        passw_salted = encrypt_pass(passw_,salt)
        query = "SELECT nickname, email,FK_ROL_rol_name FROM users WHERE (nickname = %s or email = %s) AND passw = %s"
        data = (user_,user_, passw_salted,)
        cursor.execute(query, data)
        for (nickname, email,FK_ROL_rol_name) in cursor:
            return [nickname, email, FK_ROL_rol_name]
        cursor.close()
        cnx.close()
        return []
    except Exception as e:
        print(str(e))
        return 'Error #2 en la base de datos'


def this_user_exist(user_, email_):
    try:
        database_ = Database()
        config = database_.config
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        query = "SELECT email FROM users WHERE email=%s OR users =%s"
        data = (email_,user_,)
        cursor.execute(query, data)
        for (email) in cursor:
            return True
        cursor.close()
        cnx.close()
        return False
    except Exception as e:
        print(str(e))
        return False


def crear_usuario(email_, nickname_, firstname_, lastname_, passw_, birthdat_datetime_, contry_, type_):
    response = -1
    try:
        database_ = Database()
        config = database_.config
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        salt = random_salt()
        passw_salted = encrypt_pass(passw_, salt)
        query = "INSERT INTO `users` (`email`, `nickname`, `firstname`, `lastname`, `passw`, `salt`, `birthday_datetime`, `FK_COUNTRY_country`, `FK_ROL_rol_name`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
        data = (email_, nickname_, firstname_, lastname_, passw_salted, salt, birthdat_datetime_, contry_, type_,)
        cursor.execute(query, data)
        cnx.commit()
        response = int(cursor.lastrowid)
        cnx.close()
        return response
    except Exception as e:
        print(e)
        return response