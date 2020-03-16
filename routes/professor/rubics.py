#!/usr/bin/env python
# -*- coding: utf-8 -*-

from controllers.controller_rubics import *
from controllers.general_db_functions import *
from controllers.controller_challenges import iam_challenge_owner_by_id
from routes.apidoc import *
apiprub = Namespace('professor/rubic', description="Endpoints utilizados solo por profesores en rubic")  # pylint: disable=invalid-name


@apiprub.route('/create', methods=['POST'])
@apiprub.doc(
    security='apikey',
    responses={
        200: 'Success',
        403: 'Forbidden',
        404: 'Token not found',
        500: 'Internal server error',
        503: 'Service Unavailable'
    }
)
class Professor_rubic_create(Resource):
    test_fields = apins.model('Creación de Rúbrica', {
        'title': fields.String(required=True, description='Título o alias de la rúbrica',example='prueba 1'),
        'description': fields.String(required=True, description='Descripción de la rúbrica', example='Evaluación de 1-7 en cuanto al aprendizaje'),
        'datajson': fields.String(required=True, description='Título o alias de la rubrica', example='[{"id":1,"text":"Evaluación general del desafío","description":"Descripción de rúbrica","min":1,"max":7,"percentage":100}]'),
        'id_challenge': fields.String(required=True, description='Id del desafío', example='1')
    })

    @apiprub.expect(test_fields)
    @token_required
    def post(self):
        """Metodo para crear rúbrica y enlazarla con un desafío"""
        data = get_info_token()
        ip_ = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        try:
            data = get_info_token()
            title_ = str(request.get_json()['title'].encode('utf-8').strip().decode("utf-8"))
            description_ = str(request.get_json()['description'].encode('utf-8').strip().decode("utf-8"))
            datajson_ = str(request.get_json()['datajson'].encode('utf-8').strip().decode("utf-8"))
            id_challenge_ = str(request.get_json()['id_challenge'].encode('utf-8').strip().decode("utf-8"))
            Payload = {"title": title_, "description":description_, "datajson":datajson_, "id_challenge":id_challenge_ }
            insert_request_log("/professor/rubic/create" , "POST", str(Payload), ip_, data['email'])
            if get_permission_by_user('Create_rubic', data['rol']) == 'True':
                if not iam_challenge_owner_by_id(id_challenge_, data['email']):
                    response_str = {'message': 'Acción no permitida en el desafío', 'code': 403}
                    insert_general_log(str(response_str), ip_, data['email'])
                    return jsonify(response_str)
                if this_challenge_have_rubic(id_challenge_):
                    response_str = {'message': 'Este desafío ya tiene rúbica', 'code': 403}
                    insert_general_log(str(response_str), ip_, data['email'])
                    return jsonify(response_str)
                response = new_rubic(title_, description_, datajson_, id_challenge_)
                if response >= 1:
                    message = 'Rúbrica creada'
                    code = 200
                else:
                    message = 'Algo sucedió en la base de datos'
                    code = 503
                response_str = {'message': message, 'code': code, 'id_class': response}
                insert_general_log(str(response_str), ip_, data['email'])
                return jsonify(response_str)
            else:
                message = 'Acción no permitida'
                code = 403
                response_str = {'message': message, 'code': code}
                insert_general_log(str(response_str), ip_, data['email'])
                return jsonify(response_str)
        except Exception as e:
            message = 'Se ha producido un error en nuestros servidores'
            code = 500
            response_str = str({'error': "/professor/rubic/create", 'detalle': str(e)})
            insert_general_log(response_str, ip_, data['email'])
            return jsonify({'message': message, 'code': code})



@apiprub.route('/edit/<id_rubic>', methods=['PUT'])
@apiprub.doc(
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
class Profesor_edit_a_rubic(Resource):
    test_fields = apins.model('Edición de Rúbrica', {
        'title': fields.String(required=True, description='Título o alias de la rúbrica', example='prueba 1'),
        'description': fields.String(required=True, description='Descripción de la rúbrica',
                                     example='Evaluación de 1-7 en cuanto al aprendizaje'),
        'datajson': fields.String(required=True, description='Título o alias de la rubrica',
                                  example='[{"id":1,"text":"Evaluación general del desafío","description":"Descripción de rúbrica","min":1,"max":7,"percentage":100}]'),
        'id_challenge': fields.String(required=True, description='Id del desafío', example='1')
    })

    @apiprub.expect(test_fields)
    @token_required
    def put(self, id_rubic):
        """Metodo para editar rúbicas
        Para desvincular una rúbica de un desafío, solo asigna <strong>-1</strong> a la variable <strong>id_challenge """
        data = get_info_token()
        ip_ = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        try:
            # EDITAR-ACA
            #CHECKEAR SI EL DESAFIO YA FUE INICIADO
            title_ = str(request.get_json()['title'].encode('utf-8').strip().decode("utf-8"))
            description_ = str(request.get_json()['description'].encode('utf-8').strip().decode("utf-8"))
            datajson_ = str(request.get_json()['datajson'].encode('utf-8').strip().decode("utf-8"))
            id_challenge_ = str(request.get_json()['id_challenge'].encode('utf-8').strip().decode("utf-8"))
            Payload = {"title": title_, "description": description_, "datajson": datajson_,
                       "id_challenge": id_challenge_}
            insert_request_log("/professor/rubic/edit/"+str(id_rubic), "PUT", str(Payload), ip_, data['email'])
            if get_permission_by_user('Update_rubic', data['rol']) == 'True':
                if not iam_challenge_owner_by_id(id_challenge_, data['email']):
                    response_str = {'message': 'Acción no permitida en el desafío', 'code': 403}
                    insert_general_log(str(response_str), ip_, data['email'])
                    return jsonify(response_str)
                response = edit_rubic(title_, description_, datajson_, id_challenge_, id_rubic)
                if response >= 1:
                    message = 'ok'
                    code = 200
                else:
                    message = 'Algo sucedió en la base de datos'
                    code = 503
                response_str = {'message': message, 'code': code, 'id_class': response}
                insert_general_log(str(response_str), ip_, data['email'])
                return jsonify(response_str)
            else:
                message = 'Acción no permitida'
                code = 403
                response_str = {'message': message, 'code': code}
                insert_general_log(str(response_str), ip_, data['email'])
                return jsonify(response_str)
        except Exception as e:
            message = 'Se ha producido un error en nuestros servidores'
            code = 500
            response_str = str({'error': "/professor/rubic/edit/" + str(id_rubic), 'detalle': str(e)})
            insert_general_log(response_str, ip_, data['email'])
            return jsonify({'message': message, 'code': code})




@apiprub.route('/', methods=['GET'])
@apiprub.doc(
    security='apikey',
    responses={
        200: 'Success',
        400: 'Bad Request',
        403: 'Not Authorized',
        404: 'Token not found',
        500: 'Internal server error'
    }
)
class Profesor_get_rubic(Resource):
    @token_required
    def get(self):
        """
		Método para obtener todas las rúbricas creadas por el profesor
		<strong>Se obtiene un arreglo de los siguientes datos:</strong>
		-[0] Id de rúbrica\n
		-[1] Titúlo de rúbrica\n
		-[2] Descripción de rúbrica\n
		-[3] Fecha de creación\n
		-[4] Fecha de modificación\n
		-[5] data\n
		-[6] Id de desafío\n
		"""
        data = get_info_token()
        ip_ = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        try:
            insert_request_log("/professor/rubic/", "GET", "", ip_, data['email'])
            my_rubics = get_all_my_rubics(data['email'])
            response_str = {'message': "Todas tus rubicas", 'data': my_rubics, 'code': 200}
            insert_general_log(str(response_str), ip_, data['email'])
            return jsonify(response_str)
        except Exception as e:
            message = 'Se ha producido un error en nuestros servidores'
            code = 500
            response_str = str({'error': "/professor/rubic/", 'detalle': str(e)})
            insert_general_log(response_str, ip_, data['email'])
            return jsonify({'message': message, 'code': code})


# TEMPLATE


@apiprub.route('/template', methods=['GET'])
@apiprub.doc(
    security='apikey',
    responses={
        200: 'Success',
        400: 'Bad Request',
        403: 'Not Authorized',
        404: 'Token not found',
        500: 'Internal server error'
    }
)
class Profesor_get_rubic_template(Resource):
    @token_required
    def get(self):
        """
		Método para obtener todas las rúbricas creadas por el profesor
		<strong>Se obtiene un arreglo de los siguientes datos:</strong>
		-[0] Id de rúbrica\n
		-[1] Titúlo de rúbrica\n
		-[2] Descripción de rúbrica\n
		-[3] Fecha de creación\n
		-[4] Fecha de modificación\n
		-[5] Data\n
		-[6] Status\n
		-[7] Creador\n
		"""
        data = get_info_token()
        ip_ = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        try:
            if not get_permission_by_user('Read_rubic', data['rol']) == 'True':
                response_str = {'message': "Acción no permitida", 'code': 403}
                insert_general_log(str(response_str), ip_, data['email'])
                return jsonify(response_str)
            insert_request_log("/professor/rubic/", "GET", "", ip_, data['email'])
            all_template_rubics = get_all_template_rubic_show()
            response_str = {'message': "Todas los templates de rúbricas", 'data': all_template_rubics, 'code': 200}
            insert_general_log(str(response_str), ip_, data['email'])
            return jsonify(response_str)
        except Exception as e:
            message = 'Se ha producido un error en nuestros servidores'
            code = 500
            response_str = str({'error': "/professor/rubic/template", 'detalle': str(e)})
            insert_general_log(response_str, ip_, data['email'])
            return jsonify({'message': message, 'code': code})



@apiprub.route('/template/create', methods=['POST'])
@apiprub.doc(
    security='apikey',
    responses={
        200: 'Success',
        403: 'Forbidden',
        404: 'Token not found',
        500: 'Internal server error',
        503: 'Service Unavailable'
    }
)
class Professor_template_rubic_create(Resource):
    test_fields = apins.model('Creación de template de Rúbrica', {
        'title': fields.String(required=True, description='Título o alias de la rúbrica',example='prueba 1'),
        'description': fields.String(required=True, description='Descripción de la rúbrica', example='Evaluación de 1-7 en cuanto al aprendizaje'),
        'datajson': fields.String(required=True, description='Título o alias de la rubrica', example='[{"id":1,"text":"Evaluación general del desafío","description":"Descripción de rúbrica","min":1,"max":7,"percentage":100}]'),
    })

    @apiprub.expect(test_fields)
    @token_required
    def post(self):
        """Metodo para crear template de rúbrica"""
        data = get_info_token()
        ip_ = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        try:
            title_ = str(request.get_json()['title'].encode('utf-8').strip().decode("utf-8"))
            description_ = str(request.get_json()['description'].encode('utf-8').strip().decode("utf-8"))
            datajson_ = str(request.get_json()['datajson'].encode('utf-8').strip().decode("utf-8"))
            Payload = {"title": title_, "description": description_, "datajson": datajson_}
            insert_request_log("/professor/rubic/template/create", "POST", str(Payload), ip_, data['email'])
            if get_permission_by_user('Create_rubic', data['rol']) == 'True':
                response = new_template_rubic(title_, description_, datajson_, data['email'])
                if response >= 1:
                    message = 'Template de rúbica creada'
                    code = 200
                else:
                    message = 'Algo sucedió en la base de datos'
                    code = 503
                response_str = {'message': message, 'code': code, 'id_template_rubica': response}
                insert_general_log(str(response_str), ip_, data['email'])
                return jsonify(response_str)
            else:
                message = 'Acción no permitida'
                code = 403
                response_str = {'message': message, 'code': code}
                insert_general_log(str(response_str), ip_, data['email'])
                return jsonify(response_str)
        except Exception as e:
            message = 'Se ha producido un error en nuestros servidores'
            code = 500
            response_str = str({'error': "/professor/rubic/create", 'detalle': str(e)})
            insert_general_log(response_str, ip_, data['email'])
            return jsonify({'message': message, 'code': code})


@apiprub.route('/template/edit/<id_rubic>', methods=['PUT'])
@apiprub.doc(
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
class Profesor_edit_a_template_rubic(Resource):
    test_fields = apins.model('Edición de Rúbrica', {
        'title': fields.String(required=True, description='Título o alias de la rúbrica', example='prueba 1'),
        'description': fields.String(required=True, description='Descripción de la rúbrica',
                                     example='Evaluación de 1-7 en cuanto al aprendizaje'),
        'datajson': fields.String(required=True, description='Título o alias de la rubrica',
                                  example='[{"id":1,"text":"Evaluación general del desafío","description":"Descripción de rúbrica","min":1,"max":7,"percentage":100}]'),
        'status': fields.String(required=True, description='Variable para mostrar o eliminar desafio tipo <strong>["show","hide"]</strong>', example='1')
    })

    @apiprub.expect(test_fields)
    @token_required
    def put(self, id_rubic):
        """Metodo para editar template de rúbicas
        Para eliminar una rúbrica , solo se debe asignar <strong>hide</strong> en el atributo <strong>status</strong>"""
        data = get_info_token()
        ip_ = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        try:
            title_ = str(request.get_json()['title'].encode('utf-8').strip().decode("utf-8"))
            description_ = str(request.get_json()['description'].encode('utf-8').strip().decode("utf-8"))
            datajson_ = str(request.get_json()['datajson'].encode('utf-8').strip().decode("utf-8"))
            status_ = str(request.get_json()['status'].encode('utf-8').strip().decode("utf-8"))
            Payload = {"title": title_, "description": description_, "datajson": datajson_, "status": status_}
            insert_request_log("/professor/rubic/template/edit/" + str(id_rubic), "PUT", str(Payload), ip_, data['email'])
            if get_permission_by_user('Update_rubic', data['rol']) == 'True':
                if not this_is_my_template_rubic(id_rubic, data['email']):
                    response_str = {'message': 'Acción no permitida en el desafío', 'code': 403}
                    insert_general_log(str(response_str), ip_, data['email'])
                    return jsonify(response_str)
                response = edit_template_rubic(title_, description_, datajson_, status_, id_rubic)
                if response >= 1:
                    message = 'Template de rúbrica editado exitosamente'
                    code = 200
                else:
                    message = 'Algo sucedió en la base de datos'
                    code = 503
                response_str = {'message': message, 'code': code}
                insert_general_log(str(response_str), ip_, data['email'])
                return jsonify(response_str)
            else:
                message = 'Acción no permitida'
                code = 403
                response_str = {'message': message, 'code': code}
                insert_general_log(str(response_str), ip_, data['email'])
                return jsonify(response_str)
        except Exception as e:
            message = 'Se ha producido un error en nuestros servidores'
            code = 500
            response_str = str({'error': "/professor/rubic/template/edit/" + str(id_rubic), 'detalle': str(e)})
            insert_general_log(response_str, ip_, data['email'])
            return jsonify({'message': message, 'code': code})
