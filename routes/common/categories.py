#!/usr/bin/env python
# -*- coding: utf-8 -*-
from routes.apidoc import *
from controllers.controller_categories import *
from controllers.general_db_functions import insert_request_log, insert_general_log

@api.route('/categories', methods=['GET'])
@api.doc(
    responses={
        200: 'Success',
        500: 'Internal server error'
    }
)
class GetallCategories_common_cls(Resource):
    def get(self):
        """
        Método para obtener todas las categorías
        """
        FK_USER_email = None
        try:
            data_ = get_info_token()
            FK_USER_email = data_['email']
        except:
            pass
        ip_ = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        insert_request_log("/categories", "GET", "", ip_, FK_USER_email)
        try:
            data = get_all_categories()
            response_str = str({'message': "Todas las categorías", 'data': data, 'code': 200})
            insert_general_log(response_str, ip_)
            return jsonify({'message': "Todas las categorías", 'data': data, 'code': 200})
        except Exception as e:
            message = 'Se ha producido un error en nuestros servidores'
            code = 500
            ip_ = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
            response_str = str({'error': "/categories", 'detalle': str(e)})
            insert_general_log(response_str, ip_,FK_USER_email)
            return jsonify({'message': message, 'code': code})
