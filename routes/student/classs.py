# -*- coding: utf-8 -*-

from controllers.general_db_functions import *

from controllers.controller_classs import *

from routes.apidoc import *

api_student_class = Namespace('student/class',
                  description="Endpoints utilizados solo por estudiantes en clases")



@api_student_class.route('/', methods=['GET'])
@api_student_class.doc(
    security='apikey',
    responses={
        200: 'Success',
        400: 'Bad Request',
        403: 'Not Authorized',
        404: 'Token not found',
        500: 'Internal server error'
    }
)
class Student_get_clcls(Resource):
    @token_required
    def get(self):
        """
		Método para obtener todas las clases a las cuales pertenece
		"""
        data = get_info_token()
        ip_ = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        try:
            insert_request_log("/student/class/" , "GET", "", ip_, data['email'])
            all_class = get_all_my_class_student(data['email'])
            response_str = {'message': "Todas tus clases", 'data': all_class, 'code': 200}
            insert_general_log(str(response_str), ip_, data['email'])
            return jsonify(response_str)
        except Exception as e:
            message = 'Se ha producido un error en nuestros servidores'
            code = 500
            response_str = str({'error': "/student/class/", 'detalle': str(e)})
            insert_general_log(response_str, ip_, data['email'])
            return jsonify({'message': message, 'code': code})

@api_student_class.route('/<id_class>', methods=['GET'])
@api_student_class.doc(
    security='apikey',
    responses={
        200: 'Success',
        400: 'Bad Request',
        403: 'Not Authorized',
        404: 'Token not found',
        500: 'Internal server error'
    }
)
class Student_get_clcls(Resource):
    @token_required
    def get(self,id_class):
        """
		Método para obtener todos los desafós de una clase
		"""
        data = get_info_token()
        ip_ = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        try:
            insert_request_log("/student/class/" , "GET", "", ip_, data['email'])
            all_class_challenge = get_all_my_challenges_student_by_idclass(data['email'],id_class)
            response_str = {'message': "Todos tus desafíos en la clase solicitada", 'data': all_class_challenge, 'code': 200}
            insert_general_log(str(response_str), ip_, data['email'])
            return jsonify(response_str)
        except Exception as e:
            message = 'Se ha producido un error en nuestros servidores'
            code = 500
            response_str = str({'error': "/student/class/", 'detalle': str(e)})
            insert_general_log(response_str, ip_, data['email'])
            return jsonify({'message': message, 'code': code})