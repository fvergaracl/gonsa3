#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding=utf-8  
import mysql.connector
from settings.configs import Database
from datetime import datetime
from functions.general import encrypt_pass

def get_permission_by_user(type_permission,user_rol):
    try:
        database_ = Database()
        config = database_.config
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        query = "SELECT value, FK_ROL_rol_name FROM permission WHERE FK_PERMISSION_TYPE_permission = %s AND FK_ROL_rol_name = %s "
        data = (type_permission,user_rol,)
        cursor.execute(query, data)
        for (value, FK_ROL_rol_name ) in cursor:
            return value
        cursor.close()
        cnx.close()
        print(type_permission,user_rol)
        print('12123')
        return 'False'
    except Exception as e:
        print('Error #1 en la base de datos')
        print(e)
        return 'False'

def get_all_contries():
    r = []
    try:
        database_ = Database()
        config = database_.config
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        query = "SELECT country FROM country"
        cursor.execute(query)
        for (country) in cursor:
            r.append(str(country[0]))
        cursor.close()
        cnx.close()
        return r
    except Exception as e:
        print('Error #1 en la base de datos')
        print(e)
        return r

def insert_request_log(endpoint_,request_type_, data_, ip_, fk_user_email=None):
    response = -1
    try:
        database_ = Database()
        config = database_.config
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        now = datetime.now()
        query = "INSERT INTO request_log(endpoint,request_type, data, reqdatetime, ip, FK_USERS_email) VALUES (%s, %s, %s, %s, %s, %s);"
        data = (endpoint_, request_type_, data_, str(now), ip_, fk_user_email,)
        cursor.execute(query, data)
        cnx.commit()
        response = int(cursor.lastrowid)
        cnx.close()
        return response
    except Exception as e:
        print(e)
        return response

def insert_general_log( data_, ip_, fk_user_email=None):
    response = -1
    try:
        database_ = Database()
        config = database_.config
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        now = datetime.now()
        query = "INSERT INTO general_logs(data, reqdatetime, ip, FK_USERS_email) VALUES (%s, %s, %s, %s);"
        data = (data_, str(now), ip_, fk_user_email,)
        cursor.execute(query, data)
        cnx.commit()
        response = int(cursor.lastrowid)
        cnx.close()
        return response
    except Exception as e:
        print(e)
        return response