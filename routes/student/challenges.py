#!/usr/bin/env python
# -*- coding: utf-8 -*-
from routes.apidoc import *
from functions.token_functions import token_required, get_info_token
from controllers.general_db_functions import *
from controllers.controller_challenges import *
from functions.search_functions import *
apisch = Namespace('student/challenge', description="Endpoints utilizados solo por profesores en desafios")  # pylint: disable=invalid-name



@apisch.route('/deadline_status/<id_challenge>', methods=['GET'])
@apisch.doc(
    security='apikey',
    responses={
        200: 'Success',
        400: 'Bad Request',
        403: 'Forbidden',
        404: 'Token not found',
        500: 'Internal server error',
        503: 'Service Unavailable'
    }
)
class student_deadline_status(Resource):
    @token_required
    def get(self,id_challenge):
        """
        [NO FUNCIONANDO] - Ver el estado de deadline, para comprobar si aún puede ejecutar alguna acción sobre el desafío
        """
        data = get_info_token()
        ip_ = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        response = ({'message': "Endpoint Pendiente", 'code': 200})
        insert_general_log(str(response), ip_, data['email'])
        return jsonify(response)


@apisch.route('/search', methods=['POST'])
@apisch.doc(
    security='apikey',
    responses={
        200: 'Success',
        400: 'Bad Request',
        403: 'Forbidden',
        404: 'Token not found',
        500: 'Internal server error',
        503: 'Service Unavailable'
    },

)
class search_student_(Resource):
    test_fields = apinspd.model('búsqueda', {
        'query': fields.String(required=True, description='Título de desafío', example='esto es una query'),
        'searchengine': fields.String(required=True, description='Motod de búsqueda [google]', example='duckduckgo'),
        'id_challenge': fields.String(required=True, type="integer", description='id de clase a la cual se enlaza el desafío (Atributo numérico)', example=1)
    })

    @apisch.expect(test_fields)
    @token_required
    def post(self):
        """Realizar búsqueda [duckduckgo]"""
        data = get_info_token()
        ip_ = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        response = ""
        code = 500
        message = ''
        try:
            query_ = str(request.get_json()['query'].encode('utf-8').strip().decode("utf-8"))
            searchengine_ = str(request.get_json()['searchengine'].encode('utf-8').strip().decode("utf-8"))
            id_challenge_ = str(request.get_json()['id_challenge'])
            if searchengine_.lower() == 'google':
                response = googlesearch(query_)
                code = 200
                message = 'TODOOK'
            return jsonify({'message': message, 'code': code, 'response': response})

        except Exception as e:
            message = 'Se ha producido un error en nuestros servidores'
            code = 500
            print(str(e))
            return jsonify({'message': message, 'code': code})