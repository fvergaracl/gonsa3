#!/usr/bin/env python
# -*- coding: utf-8 -*-

from controllers.general_db_functions import *

from controllers.controller_classs import *

from routes.apidoc import *

apins = Namespace('professor/class',
                  description="Endpoints utilizados solo por profesores en clases")  # pylint: disable=invalid-name


@apins.route('/', methods=['GET'])
@apins.doc(
    security='apikey',
    responses={
        200: 'Success',
        400: 'Bad Request',
        403: 'Not Authorized',
        404: 'Token not found',
        500: 'Internal server error'
    }
)
class Profesor_get_clcls(Resource):
    @token_required
    def get(self):
        """
		Método para obtener todas las clases (alias) creados por el profesor
		<strong>Se obtiene un arreglo de los siguientes datos:</strong>
		-[0] Id de classroom\n
		-[1] Alias de la clase\n
		"""
        data = get_info_token()
        ip_ = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        try:
            insert_request_log("/professor/class/" , "GET", "", ip_, data['email'])
            all_class = get_all_my_challenges_profesor(data['email'])
            response_str = {'message': "Todas tus clases", 'data': all_class, 'code': 200}
            insert_general_log(str(response_str), ip_, data['email'])
            return jsonify(response_str)
        except Exception as e:
            message = 'Se ha producido un error en nuestros servidores'
            code = 500
            response_str = str({'error': "/professor/class/", 'detalle': str(e)})
            insert_general_log(response_str, ip_, data['email'])
            return jsonify({'message': message, 'code': code})


@apins.route('/create', methods=['POST'])
@apins.doc(
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
class Profesor_create_a_class_Cls(Resource):
    test_fields = apins.model('Creacion_clase', {
        'classname': fields.String(
            required=True,
            description='Corresponde a la nombre de la clase (alias)',
            example='Clase2medioB'
        )
    })

    @apins.expect(test_fields)
    @token_required
    def post(self):
        """Metodo para crear clase"""
        data = get_info_token()
        ip_ = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        try:
            classname = str(request.get_json()['classname'].encode('utf-8').strip().decode("utf-8"))
            Payload = {"classname": classname}
            insert_request_log("/professor/class/create", "POST", str(Payload), ip_, data['email'])
            if get_permission_by_user('Create_class', data['rol']) == 'True':
                response = new_class(classname, data['email'])
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
            response_str = str({'error': "/professor/class/create", 'detalle': str(e)})
            insert_general_log(response_str, ip_, data['email'])
            return jsonify({'message': message, 'code': code})


@apins.route('/edit/<id_class>', methods=['PUT'])
@apins.doc(
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
class Profesor_edit_a_class_Cls(Resource):
    test_fields = apins.model('Creacion_clase', {
        'classname': fields.String(
            required=True,
            description='Corresponde a la nombre de la clase (alias)',
            example='Clase2medioB'
        )
    })

    @apins.expect(test_fields)
    @token_required
    def put(self, id_class):
        """Metodo para editar clase"""
        data = get_info_token()
        ip_ = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        try:
            classname = str(request.get_json()['classname'].encode('utf-8').strip().decode("utf-8"))
            Payload = {"classname": classname}
            insert_request_log("/professor/class/edit/"+ str(id_class), "PUT", str(Payload), ip_, data['email'])
            if get_permission_by_user('Update_class', data['rol']) == 'True':
                response = edit_class_profesor_(id_class,classname)
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
            response_str = str({'error': "/professor/class/edit/"+str(id_class), 'detalle': str(e)})
            insert_general_log(response_str, ip_, data['email'])
            return jsonify({'message': message, 'code': code})


@apins.route('/adduser', methods=['POST'])
@apins.doc(
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
class Profesor_add_user_to_class_(Resource):
    test_fields = apins.model('Añadir usuario a clase', {
        'idclass': fields.String(
            required=True,
            description='Id de la clase',
            type="integer",
            example=1
        ), 'studentemail': fields.String(
            required=True,
            description='Email del estudiante a añadir',
            example='estudiante1@test.com'
        )
    })

    @apins.expect(test_fields)
    @token_required
    def post(self):
        """Metodo para añadir un usuario"""
        data = get_info_token()
        ip_ = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        try:
            studentemail_ = str(request.get_json()['studentemail'].encode('utf-8').strip().decode("utf-8"))
            idclass_ = str(request.get_json()['idclass'])
            Payload = {"studentemail": studentemail_, "idclass": idclass_}
            insert_request_log("/professor/class/adduser", "POST", str(Payload), ip_, data['email'])
            if get_permission_by_user('Update_class', data['rol']) == 'True':
                if im_owner_of_this_class(idclass_, data['email']):
                    if not this_user_below_to_this_class(studentemail_, idclass_):
                        resp = insert_a_student_in_this_class(idclass_, studentemail_)
                        if resp >= 0:
                            response_str = {'message': 'Estudiante enlazado a clase exitosamente', 'code': 200}
                            insert_general_log(str(response_str), ip_, data['email'])
                            return jsonify(response_str)
                        else:
                            response_str = {'message': 'Hubo un error en el sistema, por favor contacta con el administrador',
                                 'code': 400}
                            insert_general_log(str(response_str), ip_, data['email'])
                            return jsonify(response_str)

                    else:
                        response_str = {'message': 'Este estudiante ya esta enlazado con esta clase', 'code': 400}
                        insert_general_log(str(response_str), ip_, data['email'])
                        return jsonify(response_str)
                else:
                    response_str = {'message': 'No tienes los suficientes permisos para realizar esta acción', 'code': 403}
                    insert_general_log(str(response_str), ip_, data['email'])
                    return jsonify(response_str)

            else:
                response_str = {'message': 'Acción no permitida', 'code': 403}
                insert_general_log(str(response_str), ip_, data['email'])
                return jsonify(response_str)
        except Exception as e:
            message = 'Se ha producido un error en nuestros servidores'
            code = 500
            response_str = str({'error': "/professor/class/adduser" , 'detalle': str(e)})
            insert_general_log(response_str, ip_, data['email'])
            return jsonify({'message': message, 'code': code})
