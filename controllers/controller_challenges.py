#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding=utf-8
import mysql.connector
from settings.configs import Database
from datetime import datetime
from functions.general import get_random_num, get_random_str


def new_challenge(title_, description_, photo_, aim_, fk_deadline_type_, deadline_value_, FK_CLASSROOM_id_number_,
                  FK_CATEGORY_category_name_):
    response = -1
    try:
        database_ = Database()
        config = database_.config
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        now = datetime.now()
        token_ = str(get_random_num(4)) + '-' + str(get_random_str(4))
        query = "INSERT INTO challenge(title,description,token,photo,aim,create_datetime,FK_DEADLINE_type,deadline_value,FK_CLASSROOM_id_number,FK_CATEGORY_category_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        data = (
        title_, description_, token_, photo_, aim_, now, fk_deadline_type_, deadline_value_, FK_CLASSROOM_id_number_,
        FK_CATEGORY_category_name_,)
        cursor.execute(query, data)
        cnx.commit()
        response = int(cursor.lastrowid)
        cnx.close()
        return response
    except Exception as e:
        print(e)
        return response



def get_all_my_challenges(user_email):
    r = []
    try:
        database_ = Database()
        config = database_.config
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        query = "SELECT ch.id_number,ch.title,ch.description,ch.token,ch.photo,ch.aim,ch.create_datetime,ch.last_modified_datetime,ch.FK_DEADLINE_type,ch.deadline_value,ch.FK_CLASSROOM_id_number,ch.FK_CATEGORY_category_name FROM challenge as ch INNER JOIN classroom as cl WHERE cl.FK_USERS_email = %s AND cl.id_number = ch.FK_CLASSROOM_id_number"
        data = (user_email,)
        cursor.execute(query, data)
        for (
        id_number, title, description, token, photo, aim, create_datetime, last_modified_datetime, FK_DEADLINE_type,
        deadline_value, FK_CLASSROOM_id_number, FK_CATEGORY_category_name) in cursor:
            r.append([id_number, title, description, token, photo, aim, create_datetime, last_modified_datetime,
                      FK_DEADLINE_type, deadline_value, FK_CLASSROOM_id_number, FK_CATEGORY_category_name])
        cursor.close()
        cnx.close()
        return r
    except Exception as e:
        print('Error #1 en la base de datos')
        print(e)
        return r


def get_all_students_in_challenge(id_challenge):
    r = []
    try:
        database_ = Database()
        config = database_.config
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        query = "SELECT FK_USERS_email FROM challenge_user WHERE FK_CHALLENGE_id_number = %s"
        data = (id_challenge,)
        cursor.execute(query, data)
        for (FK_USERS_email) in cursor:
            r.append(str(FK_USERS_email[0]))
        cursor.close()
        cnx.close()
        return r
    except Exception as e:
        print('Error #1 en la base de datos')
        print(e)
        return r


def iam_owner_of_this_challenge(id_challenge, email_user):
    r = []
    try:
        database_ = Database()
        config = database_.config
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        query = "SELECT ch.id_number,ch.title,ch.description,ch.token,ch.photo,ch.aim,ch.create_datetime,ch.last_modified_datetime,ch.FK_DEADLINE_type,ch.deadline_value,ch.FK_CLASSROOM_id_number,ch.FK_CATEGORY_category_name FROM challenge as ch INNER JOIN classroom as cl WHERE ch.id_number = %s AND cl.id_number = ch.FK_CLASSROOM_id_number AND cl.FK_USERS_email=%s"
        data = (id_challenge, email_user,)
        cursor.execute(query, data)
        for (id_number) in cursor:
            return True
        cursor.close()
        cnx.close()
        return False
    except Exception as e:
        print('Error #1 en la base de datos')
        print(e)
        return False


def edit_challenge(id_challenge_, title_, description_, photo_, aim_, FK_DEADLINE_type_, deadline_value_,
                   FK_CLASSROOM_id_number_, FK_CATEGORY_category_name_):
    response = -1
    try:
        database_ = Database()
        config = database_.config
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        now = datetime.now()
        token_ = str(get_random_num(4)) + '-' + str(get_random_str(4))
        query = "UPDATE challenge SET title=%s , description=%s, token=%s, photo=%s, aim=%s, last_modified_datetime=%s, FK_DEADLINE_type=%s, deadline_value=%s, FK_CLASSROOM_id_number=%s, FK_CATEGORY_category_name=%s WHERE id_challenge = %s"
        data = (
        title_, description_, token_, photo_, aim_, now, FK_DEADLINE_type_, deadline_value_, FK_CLASSROOM_id_number_,
        FK_CATEGORY_category_name_, id_challenge_,)
        cursor.execute(query, data)
        cnx.commit()
        response = int(cursor.lastrowid)
        cnx.close()
        return response
    except Exception as e:
        print(e)
        return response


# Template

def new_template_challenge(title_, description_, photo_, aim_, FK_CATEGORY_category_name_, FK_USER_email):
    response = -1
    try:
        database_ = Database()
        config = database_.config
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        now = datetime.now()
        query = "INSERT INTO challenge_template(title, description, token, photo, aim ,added_datetime, status ,FK_CATEGORY_category_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
        data = (title_, description_, photo_, aim_, now, "show", FK_CATEGORY_category_name_, FK_USER_email,)
        cursor.execute(query, data)
        cnx.commit()
        response = int(cursor.lastrowid)
        cnx.close()
        return response
    except Exception as e:
        print(e)
        return response


def get_all_templates_challenge():
    r = []
    try:
        database_ = Database()
        config = database_.config
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        query = "SELECT id_number, title, description, photo, aim, added_datetime, last_modified_datetime, FK_CATEGORY_category_name, FK_USERS_email FROM challenge_template WHERE status =%s"
        cursor.execute(query, "show", )
        for (id_number, title, description, photo, aim, added_datetime, last_modified_datetime, FK_CATEGORY_category_name, FK_USERS_email) in cursor:
            r.append([id_number, title, description, photo, aim, added_datetime, last_modified_datetime, FK_CATEGORY_category_name, FK_USERS_email])
        cursor.close()
        cnx.close()
        return r
    except Exception as e:
        print('Error #1 en la base de datos')
        print(e)
        return r

def edit_template_challenge(id_challenge_, title_, description_, photo_, aim_, FK_CATEGORY_category_name_, FK_USER_email):
    response = -1
    try:
        database_ = Database()
        config = database_.config
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        now = datetime.now()
        query = "UPDATE challenge_template SET title=%s , description=%s, photo=%s, aim=%s, last_modified_datetime=%s,  FK_CATEGORY_category_name=%s WHERE FK_USERS_email=%s AND id_challenge = %s"
        data = (title_, description_, photo_, aim_, now, FK_CATEGORY_category_name_, FK_USER_email, id_challenge_,)
        cursor.execute(query, data)
        cnx.commit()
        response = int(cursor.lastrowid)
        cnx.close()
        return response
    except Exception as e:
        print(e)
        return response


def iam_challenge_owner_by_id(id_challenge_, FK_USER_email):
    try:
        database_ = Database()
        config = database_.config
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        query = "SELECT ch.id_number as iddd FROM classroom as cl INNER JOIN challenge as ch WHERE cl.id_number = ch.FK_CLASSROOM_id_number AND ch.id_number=%s AND cl.FK_USERS_email=%s "
        data_ = (id_challenge_,FK_USER_email,)
        cursor.execute(query, data_, )
        for (iddd) in cursor:
            return True
        cursor.close()
        cnx.close()
        return False
    except Exception as e:
        print('Error #1 en la base de datos')
        print(e)
        return False


#### ESTUDIANTE