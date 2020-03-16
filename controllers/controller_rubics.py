
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding=utf-8
import mysql.connector
from settings.configs import Database
from datetime import datetime


def new_rubic(title_, description_, datajson_, id_challenge):
    response = -1
    try:
        database_ = Database()
        config = database_.config
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        now = datetime.now()
        query = "INSERT INTO rubic(title, description, create_datetime, datajson, FK_CHALLENGE_id_number) VALUES (%s, %s, %s, %s, %s);"
        data = (title_, description_,str(now) , datajson_, id_challenge,)
        cursor.execute(query, data)
        cnx.commit()
        response = int(cursor.lastrowid)
        cnx.close()
        return response
    except Exception as e:
        print(e)
        return response


def this_challenge_have_rubic(id_challenge_):
    try:
        database_ = Database()
        config = database_.config
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        query = "SELECT id_number FROM `rubic` WHERE FK_CHALLENGE_id_number=%s "
        data_ = (id_challenge_,)
        cursor.execute(query, data_, )
        for (id_number) in cursor:
            return True
        cursor.close()
        cnx.close()
        return False
    except Exception as e:
        print('Error #1 en la base de datos')
        print(e)
        return False


def edit_rubic(title_, description_, datajson_, id_challenge, id_rubic):
    response = -1
    try:
        database_ = Database()
        config = database_.config
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        now = datetime.now()
        query = "UPDATE rubic SET title=%s , description=%s, last_modified_datetime=%s, datajson=%s, FK_CHALLENGE_id_number=%s WHERE id_number=%s "
        data = (title_, description_, str(now), datajson_, id_challenge, id_rubic,)
        cursor.execute(query, data)
        cnx.commit()
        response = int(cursor.lastrowid)
        cnx.close()
        return response
    except Exception as e:
        print(e)
        return response


def get_all_my_rubics(fk_user_email):
    r = []
    try:
        database_ = Database()
        config = database_.config
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        query = "SELECT ru.id_number, ru.title, ru.description, ru.create_datetime, ru.last_modified_datetime, ru.datajson, ru.FK_CHALLENGE_id_number  FROM rubic as ru INNER JOIN challenge as ch INNER JOIN classroom as cl WHERE cl.id_number = ch.FK_CLASSROOM_id_number AND ru.FK_CHALLENGE_id_number=ch.id_number AND cl.FK_USERS_email=%s"
        data_ = (fk_user_email,)
        cursor.execute(query, data_, )
        for (id_number, title, description, create_datetime, last_modified_datetime, datajson, FK_CHALLENGE_id_number) in cursor:
            r.append([id_number, title, description, create_datetime, last_modified_datetime, datajson, FK_CHALLENGE_id_number])
        cursor.close()
        cnx.close()
        return r
    except Exception as e:
        print('Error #1 en la base de datos')
        print(e)
        return r

def get_all_template_rubic_show():
    r = []
    try:
        database_ = Database()
        config = database_.config
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        query = "SELECT id_number, title, description, create_datetime, last_modified_datetime, datajson, status, FK_USERS_email FROM `rubic_template` WHERE status = 'show' "
        cursor.execute(query, )
        for (id_number, title, description, create_datetime, last_modified_datetime, datajson, status, FK_USERS_email) in cursor:
            r.append([id_number, title, description, create_datetime, last_modified_datetime, datajson, status, FK_USERS_email])
        cursor.close()
        cnx.close()
        return r
    except Exception as e:
        print('Error #1 en la base de datos')
        print(e)
        return r


def new_template_rubic(title_, description_, datajson_, fk_user_email):
    response = -1
    try:
        database_ = Database()
        config = database_.config
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        now = datetime.now()
        query = "INSERT INTO rubic_template(title, description, create_datetime, datajson, status, FK_USERS_email) VALUES (%s, %s, %s, %s, %s, %s);"
        data = (title_, description_, str(now), datajson_, "show", fk_user_email,)
        cursor.execute(query, data)
        cnx.commit()
        response = int(cursor.lastrowid)
        cnx.close()
        return response
    except Exception as e:
        print(e)
        return response

def edit_template_rubic(title_, description_, datajson_, status_, id_rubic):
    response = -1
    try:
        database_ = Database()
        config = database_.config
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        now = datetime.now()
        query = "UPDATE rubic_template SET title=%s , description=%s, last_modified_datetime=%s, datajson=%s, FK_CHALLENGE_id_number=%s WHERE id_number=%s "
        data = (title_, description_, str(now), datajson_, status_, id_rubic,)
        cursor.execute(query, data)
        cnx.commit()
        response = int(cursor.lastrowid)
        cnx.close()
        return response
    except Exception as e:
        print(e)
        return response


def this_is_my_template_rubic(id_rubic_, fk_user_email):
    try:
        database_ = Database()
        config = database_.config
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        query = "SELECT id_number status FROM `rubic_template` WHERE id_number=%s AND FK_USERS_email=%s"
        data_ = (id_rubic_, fk_user_email,)
        cursor.execute(query, data_, )
        for (id_number) in cursor:
            return True
        cursor.close()
        cnx.close()
        return False
    except Exception as e:
        print('Error #1 en la base de datos')
        print(e)
        return False
