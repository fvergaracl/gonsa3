#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding=utf-8
import mysql.connector
from settings.configs import Database


def get_all_categories():
	r = []
	try:
		database_ = Database()
		config = database_.config
		cnx = mysql.connector.connect(**config)
		cursor = cnx.cursor()
		query = "SELECT category_name, description FROM category"
		cursor.execute(query,)
		for (category_name, description) in cursor:
			r.append([category_name, description])
		cursor.close()
		cnx.close()
		return r
	except Exception as e:
		print('Error #1 en la base de datos')
		print(e)
		return r