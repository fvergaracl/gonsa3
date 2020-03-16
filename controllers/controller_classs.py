#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding=utf-8  
import mysql.connector
from settings.configs import Database

def new_class(school_, _FK_owner_nick):
	response = -1
	try:
		database_ = Database()
		config = database_.config
		cnx = mysql.connector.connect(**config)
		cursor = cnx.cursor()
		query = "INSERT INTO classroom(classroom_name, FK_USERS_email) VALUES (%s, %s);"
		data = (school_, _FK_owner_nick,)
		cursor.execute(query, data)
		cnx.commit()
		response = int(cursor.lastrowid)
		cnx.close()
		return response 
	except Exception as e:
		print('Error #1 en la base de datos | new_class')
		print(e)
		return response

def im_owner_of_this_class(id_class,FK_USER_EMAIL):
	try:
		database_ = Database()
		config = database_.config
		cnx = mysql.connector.connect(**config)
		cursor = cnx.cursor()
		query = "SELECT id_number, classroom_name from classroom WHERE FK_USERS_email=%s and id_number=%s"
		data = (FK_USER_EMAIL,id_class,)
		cursor.execute(query, data)
		for (id_number, classroom_name) in cursor:
			return True
		cursor.close()
		cnx.close()
		return False
	except Exception as e:
		print('Error #1 en la base de datos | im_owner_of_this_class')
		print(e)
		return False

def insert_a_student_in_this_class(id_class,FK_USER_EMAIL):
	response = -1
	try:
		database_ = Database()
		config = database_.config
		cnx = mysql.connector.connect(**config)
		cursor = cnx.cursor()
		query = "INSERT INTO classmate(FK_CLASSROOM_id_number, FK_USERS_email) VALUES (%s, %s);"
		data = (id_class, FK_USER_EMAIL,)
		cursor.execute(query, data)
		cnx.commit()
		response = int(cursor.lastrowid)
		cnx.close()
		return response
	except Exception as e:
		print('Error #1 en la base de datos | insert_a_student_in_this_class')
		print(e)
		return response

def this_user_below_to_this_class(FK_USER_EMAIL,id_class):
	try:
		database_ = Database()
		config = database_.config
		cnx = mysql.connector.connect(**config)
		cursor = cnx.cursor()
		query = "SELECT * FROM classmate WHERE FK_CLASSROOM_id_number=%s and FK_USERS_email=%s"
		data = (id_class,FK_USER_EMAIL,)
		cursor.execute(query, data)
		for (id_number) in cursor:
			return True
		cursor.close()
		cnx.close()
		return False
	except Exception as e:
		print('Error #1 en la base de datos | this_user_below_to_this_class')
		print(e)
		return False

def get_all_my_challenges_profesor(email_user):
	r = []
	try:
		database_ = Database()
		config = database_.config
		cnx = mysql.connector.connect(**config)
		cursor = cnx.cursor()
		query = "SELECT id_number, classroom_name FROM `classroom` WHERE FK_USERS_email =%s"
		data = (email_user,)
		cursor.execute(query, data)
		for (id_number, classroom_name) in cursor:
			r.append([id_number, classroom_name])
		cursor.close()
		cnx.close()
		return r
	except Exception as e:
		print('Error #1 en la base de datos | get_all_my_challenges_profesor')
		print(e)
		return r


def edit_class_profesor_(id_class, new_classname):
	response = -1
	try:
		database_ = Database()
		config = database_.config
		cnx = mysql.connector.connect(**config)
		cursor = cnx.cursor()
		query = "UPDATE challenge SET classroom_name=%s WHERE id_number=%s"
		data = (new_classname, id_class,)
		cursor.execute(query, data)
		cnx.commit()
		response = int(cursor.lastrowid)
		cnx.close()
		return response
	except Exception as e:
		print(e)
		return response

##### ESTUDIANTE

def get_all_my_class_student(email_user):
	r = []
	try:
		database_ = Database()
		config = database_.config
		cnx = mysql.connector.connect(**config)
		cursor = cnx.cursor()
		query = "SELECT room.id_number, room.classroom_name, users.firstname, users.lastname FROM classmate as mate INNER JOIN classroom as room INNER JOIN users WHERE room.FK_USERS_email = users.email AND mate.FK_CLASSROOM_id_number = room.id_number and mate.FK_USERS_email = %s"
		data = (email_user,)
		cursor.execute(query, data)
		for (id_number, classroom_name, firstname, lastname) in cursor:
			r.append([id_number, classroom_name, firstname, lastname])
		cursor.close()
		cnx.close()
		return r
	except Exception as e:
		print('Error #1 en la base de datos | get_all_my_class_student')
		print(e)
		return r


def get_all_my_challenges_student_by_idclass(email_user,id_class):
	r = []
	try:
		database_ = Database()
		config = database_.config
		cnx = mysql.connector.connect(**config)
		cursor = cnx.cursor()
		query = "SELECT ch.id_number, ch.title, ch.description, ch.token, ch.photo, ch.aim, ch.create_datetime, ch.last_modified_datetime, ch.FK_DEADLINE_type, ch.deadline_value, ch.FK_CATEGORY_category_name FROM classmate as mate INNER JOIN classroom as room INNER JOIN challenge as ch INNER JOIN users WHERE room.FK_USERS_email = users.email AND mate.FK_CLASSROOM_id_number = room.id_number and mate.FK_USERS_email = %s AND ch.FK_CLASSROOM_id_number = room.id_number"
		data = (email_user,id_class,)
		cursor.execute(query, data)
		for (id_number, title, description, token, photo, aim, create_datetime, last_modified_datetime, FK_DEADLINE_type, deadline_value, FK_CATEGORY_category_name) in cursor:
			r.append([id_number, title, description, token, photo, aim, create_datetime, last_modified_datetime, FK_DEADLINE_type, deadline_value, FK_CATEGORY_category_name])
		cursor.close()
		cnx.close()
		return r
	except Exception as e:
		print('Error #1 en la base de datos | get_all_my_challenges_student_by_idclass')
		print(e)
		return r