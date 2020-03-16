#!/usr/bin/env python
# -*- coding: utf-8 -*-
import jwt,os ,subprocess
from datetime import datetime
from settings.configs import Passeq
from routes.apidoc import *
from controllers.users import login_user, this_user_exist, crear_usuario
from controllers.general_db_functions import *


from routes.professor.challenges import *
from routes.professor.classs import *
from routes.common.categories import *

NOPUBLIC = Namespace(name="nopublic")



@api.route('/', methods=['GET'])
@api.doc(
    responses={
        200: 'Success'
    }
)
class Indexcls(Resource):
    def get(self):
        """
        Método para ver si el API esta arriba
        """
        ip_ = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        insert_request_log("/", "GET", "", ip_)
        response_str= str({'message': "It's works", 'code': 200, "version": "v1"})
        insert_general_log(response_str,ip_)
        print('----')
        return jsonify({'message': "It's works :)", 'code': 200, "commit": "444"})


@api.route('/getallcontries', methods=['GET'])
@api.doc(
    responses={
        200: 'Success'
    }
)
class Getallcontries_(Resource):
    def get(self):
        """
        Método para obtener todos los paises
        """
        ip_ = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        insert_request_log("/getallcontries", "GET", "", ip_)
        response = {'message': get_all_contries(), 'code': 200}
        response_str= str(response)
        insert_general_log(response_str,ip_)
        return jsonify(response)

@api.route('/create_user', methods=['POST'])
@api.doc(
    responses={
        200: 'Success',
        400: 'Bad Request',
        500: 'Internal server error'
    }
)
class Create_user_(Resource):
    test_fields = api.model('Crear usuario', {
        'fname': fields.String(required=False, description='Nombre', example='Nombre1'),
        'lname': fields.String(required=False, description='Apellido', example='Apellido1'),
        'user': fields.String(required=True, description='Usuario', example='studenttest'),
        'passw1': fields.String(required=True, description='Contraseña', example='111111'),
        'passw2': fields.String(required=True, description='Repetición de contraseña', example='111111'),
        'email': fields.String(required=True, description='email', example='fvergara@fvergara.cl'),
        'birthday': fields.String(required=False, description='Fecha de cumpleaños ejemplo "09/19/18"', example='09/19/18'),
        'contry': fields.String(required=False, description='País .Se obtiene los paises disponibles con el endpoint /getallcontries', example='Chile')
    })
    @api.expect(test_fields)
    def post(self):
        """
        Método para crear usuario [defaul: tipo estudiante]
        """
        try:

            user_ = str(request.get_json()['user'].encode('utf-8').strip().decode("utf-8"))
            pass_1 = str(request.get_json()['passw1'].encode('utf-8').strip().decode("utf-8"))
            pass_2 = str(request.get_json()['passw2'].encode('utf-8').strip().decode("utf-8"))
            email_ = str(request.get_json()['email'].encode('utf-8').strip().decode("utf-8"))
            contry_ = str(request.get_json()['contry'].encode('utf-8').strip().decode("utf-8"))
            try:
                fname_ = str(request.get_json()['fname'].encode('utf-8').strip().decode("utf-8"))
            except:
                fname_ = None
            try:
                lname_ = str(request.get_json()['lname'].encode('utf-8').strip().decode("utf-8"))
            except:
                lname_ = None
            try:
                birthday_ = str(request.get_json()['birthday'].encode('utf-8').strip().decode("utf-8"))
            except:
                birthday_ = None
            ip_ = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
            Payload = {"user":user_, "passw1":"[Private]", "passw2":"[Private]"}
            insert_request_log("/create_user","POST",str(Payload),ip_)
            if not (pass_1 == pass_2):
                response = {"message": "Las contraseñas ingresadas no coinciden", 'code': 400}
                response_str = str(response)
                insert_general_log(response_str, ip_)
                return jsonify(response)
            if this_user_exist(user_, email_):
                response = {"message": "El usuario o email, ya se encuentra registrado. Por favor recupere su contraseña", 'code': 400}
                response_str = str(response)
                insert_general_log(response_str, ip_)
                return jsonify(response)
            resp_bool , resp = Passeq.checkpass(pass_1)
            if not resp_bool:
                response = {"message": resp, 'code': 400}
                response_str = str(response)
                insert_general_log(response_str, ip_)
                return jsonify(response)
            else:
                response_controller = crear_usuario(email_, user_, fname_, lname_, pass_1, birthday_, contry_, "Student")
                if response_controller >= 1:
                    response = {"message": "Usuario creado exitosamente", 'code': 200}
                else:
                    response = {"message": "No se ha podido crear el usuario, hubo un error en nuestros servidores :( ... Por favor, intente más tarde", 'code': 500}
                response_str = str(response)
                insert_general_log(response_str, ip_)
                return jsonify(response)
        except Exception as e:
            print('/create_user |' + str(e))
            ip_ = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
            response_str = str({'error': "/create_user", 'detalle': str(e)})
            insert_general_log(response_str, ip_)
            return jsonify({'message': "Hubo un problema en el servidor, contacte al administrador por favor", 'code': 500})



@api.route('/login', methods=['POST'])
@api.doc(
    responses={
        200: 'Success',
        400: 'Bad Request',
        500: 'Internal server error'
    }
)
class LoginCls(Resource):
    test_fields = api.model('Login', {
        'user': fields.String(required=True, description='Usuario', example='profesor1'),
        'passw': fields.String(required=True, description='Contraseña', example='111111')
    })
    @api.expect(test_fields)
    def post(self):
        """
        Método de autentificación
        """
        message = ''
        code = 500
        token = ''
        try:
            print('***********')
            user_ = str(request.get_json()['user'].encode('utf-8').strip().decode("utf-8"))
            pass_ = str(request.get_json()['passw'].encode('utf-8').strip().decode("utf-8"))
            ip_ = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
            Payload = {"user":user_, "passw":"[Private]"}
            insert_request_log("/login","POST",str(Payload),ip_)
            if user_ == '' or user_.strip() == '':
                message = 'You must enter an email or your user to enter the system'
                code = 400
                raise Exception
            if pass_ == '' or pass_.strip() == '':
                message = 'You must enter an email or your user to enter the system'
                code = 400
                raise Exception
            response = login_user(user_,pass_)
            if 'Error #2 en la base de datos' in str(response):
                code = 500
                message = 'Error interno en el servidor - (DB)'
                print('**1111***')
                raise Exception
            print(response)
            if len(response)>=1:
                message ='Logeado correctamente'
                code = 200
                token = jwt.encode({"nickname":response[0],"email":response[1], "rol":response[2], 'exp': datetime.utcnow() + c.get_api_jwt_time()}, c.get_jwt_secret_key())
                response_str = str({'message': message, 'token':token.decode("utf-8"), 'code': code})
                insert_general_log(response_str, ip_)
                return jsonify({'message': message, 'token':token.decode("utf-8"), 'code': code})
            else:
                message = 'Ususario o contraseña incorrecto'
                code = 400
                return jsonify({'message': message, 'code': code})
        except Exception as e:
            print('/login |' +str(e))
            ip_ = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
            if str(e) == '':
                response_str = str({'error': "/login", 'detalle': 'Error interno en el servidor'})
                print(response_str)
            else:
                response_str = str({'error': "/login", 'detalle': str(e)})
            insert_general_log(response_str, ip_)
            return jsonify({'message': message, 'code': code})



    


@api.route('/islogged', methods=['GET'])
@api.doc(
    security='apikey',
    responses={
        200: 'Success',
        400: 'Bad Request',
        403: 'Not Authorized',
        404: 'Token not found',
        500: 'Internal server error'
    }
)
class IsloggedClss(Resource):
    @token_required
    def get(self):
        """
        Método para testear si token es válido
        """
        data = get_info_token()
        ip_ = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        insert_request_log("/islogged", "GET", "", ip_, data['email'])
        response_str = str({'message': "You're logged",'data':data , 'code': 200})
        insert_general_log(response_str, ip_, data['email'])
        return jsonify({'message': "You're logged",'data':data , 'code': 200})

