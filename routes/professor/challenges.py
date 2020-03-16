#!/usr/bin/env python
# -*- coding: utf-8 -*-
from routes.apidoc import *
from functions.token_functions import token_required, get_info_token
from controllers.general_db_functions import *
from settings.configs import Config
from controllers.controller_challenges import *
from controllers.controller_classs import im_owner_of_this_class
apinspd = Namespace('professor/challenge', description="Endpoints utilizados solo por profesores en desafios")  # pylint: disable=invalid-name



@apinspd.route('/', methods=['GET'])
@apinspd.doc(
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
class profesor_get_all_challenges__(Resource):
    @token_required
    def get(self):
        """
        Obtener todos los desafíos (Creados por el usuario [Profesor])
        <strong>Se obtiene un arreglo de los siguientes datos:</strong>
        -[0] Id de desafio\n
        -[1] Título\n
        -[2] Descripción\n
        -[3] Token interno (No habilitado)\n
        -[4] Foto (base64)\n
        -[5] Objetivos\n
        -[6] Fecha de creación\n
        -[7] Ultima vez modificado\n
        -[8] Tipo de deadline\n
        -[9] Valor de deadline\n
        -[10] ID de classroom a la que pertenece\n
        -[11] Categoría del desafío\n
        """
        data = get_info_token()
        ip_ = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        try:
            insert_request_log("/professor/challenge/", "GET", "", ip_,data['email'])
            if get_permission_by_user('Read_challenge', data['rol']) == 'True':
                response = get_all_my_challenges(data['email'])
                if len(response)>= 1:
                    message = 'ok'
                    code = 200
                else:
                    message = 'Algo sucedió en la base de datos'
                    code = 503
                response_str = str({'message': message, 'code': code, 'challenges':response})
                insert_general_log(response_str, ip_, data['email'])
                return jsonify({'message': message, 'code': code, 'challenges':response})
            else:
                message = 'Acción no permitida'
                code = 403
                response_str = str({'message': message, 'code': code})
                insert_general_log(response_str, ip_, data['email'])
                return jsonify({'message': message, 'code': code})
        except Exception as e:
            message = 'Se ha producido un error en nuestros servidores'
            code = 500
            response_str = str({'error': "/professor/challenge/", 'detalle': str(e)})
            insert_general_log(response_str, ip_, data['email'])
            return jsonify({'message': message, 'code': code})


@apinspd.route('/create', methods=['POST'])
@apinspd.doc(
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
class profesor_create_a_challenge__(Resource):
    test_fields = apinspd.model('crear_desafio', {
        'title': fields.String(required=True, description='Título de desafío', example='Ejemlo de Título de desafío'),
        'description': fields.String(required=True, description='Descripción de desafío', example='Ejemplo de descripción de desafío'),
        'photo': fields.String(required=True, description='Foto en string (base64)', example=' data:image/png;base64,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'),
        'aim': fields.String(required=True, description='Objetivos del desafío', example='aprender a buscar, seleccionar fuentes relevantes'),
        'deadline_type': fields.String(required=True, description='Cierre de desafío.Puede ser de tipo [minutes,timestamp] ', example='minutes'),
        'deadline_value': fields.String(required=True, type="integer", description='Depende del tipo de deadline (Atributo numérico)', example=30),
        'id_classroom': fields.String(required=True, type="integer", description='id de clase a la cual se enlaza el desafío (Atributo numérico)', example=1),
        'category': fields.String(required=True, description='Categoría a la cual pertenece el desafío a ingresar', example='matemática')
    })

    @apinspd.expect(test_fields)
    @token_required
    def post(self):
        """Crear nuevo desafío"""
        data = get_info_token()
        ip_ = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        try:

            title_ = str(request.get_json()['title'].encode('utf-8').strip().decode("utf-8"))
            description_ = str(request.get_json()['description'].encode('utf-8').strip().decode("utf-8"))
            photo_ = str(request.get_json()['photo'].encode('utf-8').strip().decode("utf-8"))
            aim_ = str(request.get_json()['aim'].encode('utf-8').strip().decode("utf-8"))
            deadline_type_ = str(request.get_json()['deadline_type'].encode('utf-8').strip().decode("utf-8"))
            deadline_value_ = str(request.get_json()['deadline_value'].encode('utf-8').strip().decode("utf-8"))
            id_classroom_ = str(request.get_json()['id_classroom'].encode('utf-8').strip().decode("utf-8"))
            category_ = str(request.get_json()['category'].encode('utf-8').strip().decode("utf-8"))
            Payload ={"title": title_, "description": description_,
                      "photo": photo_, "aim":aim_, "deadline_type":deadline_type_,
                      "deadline_value": deadline_value_, "id_classroom":id_classroom_, "category": category_}
            insert_request_log("/professor/challenge/create", "POST", str(Payload), ip_, data['email'])
            if get_permission_by_user('Create_challenge', data['rol']) == 'True':
                if im_owner_of_this_class(id_classroom_,data['email']):
                    response = new_challenge(title_, description_, photo_, aim_, deadline_type_, deadline_value_, id_classroom_,category_)
                    if response >=1:
                        message = 'ok'
                        code = 200
                    else:
                        message = 'Algo sucedió en la base de datos'
                        code = 503
                else:
                    message = 'Usted no tiene permisos suficientes para añadir este desafío a la clase solicitada'
                    code = 403
                    response = -1
                response_str = str({'message': message, 'code': code, 'id_challenge': response})
                insert_general_log(response_str, ip_, data['email'])
                return jsonify({'message': message, 'code': code, 'id_challenge': response})
            else:
                message = 'Acción no permitida'
                code = 403
                response_str = str({'message': message, 'code': code})
                insert_general_log(response_str, ip_, data['email'])
                return jsonify({'message': message, 'code': code})
        except Exception as e:
            message = 'Se ha producido un error en nuestros servidores'
            code = 500
            response_str = str({'error': "/professor/challenge/create", 'detalle': str(e)})
            insert_general_log(response_str, ip_, data['email'])
            return jsonify({'message': message, 'code': code})


@apinspd.route('/edit/<id_challenge>', methods=['PUT'])
@apinspd.doc(
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
class profesor_edit_a_challenge__(Resource):
    test_fields = apinspd.model('editar_desafio', {
        'title': fields.String(required=True, description='Título de desafío', example='Ejemlo de Título de desafío'),
        'description': fields.String(required=True, description='Descripción de desafío', example='Ejemplo de descripción de desafío'),
        'photo': fields.String(required=True, description='Foto en string (base64)', example=' data:image/png;base64,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'),
        'aim': fields.String(required=True, description='Objetivos del desafío', example='aprender a buscar, seleccionar fuentes relevantes'),
        'deadline_type': fields.String(required=True, description='Cierre de desafío.Puede ser de tipo [minutes,timestamp] ', example='minutes'),
        'deadline_value': fields.String(required=True, type="integer", description='Depende del tipo de deadline (Atributo numérico)', example=30),
        'id_classroom': fields.String(required=True, type="integer", description='id de clase a la cual se enlaza el desafío (Atributo numérico)', example=1),
        'category': fields.String(required=True, description='Categoría a la cual pertenece el desafío a ingresar', example='matemática')
    })

    @apinspd.expect(test_fields)
    @token_required
    def put(self,id_challenge):
        """Editar desafío por id"""
        data = get_info_token()
        ip_ = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        try:
            if data['rol'] == 'Professor':
                title_ = str(request.get_json()['title'].encode('utf-8').strip().decode("utf-8"))
                description_ = str(request.get_json()['description'].encode('utf-8').strip().decode("utf-8"))
                photo_ = str(request.get_json()['photo'].encode('utf-8').strip().decode("utf-8"))
                aim_ = str(request.get_json()['aim'].encode('utf-8').strip().decode("utf-8"))
                deadline_type_ = str(request.get_json()['deadline_type'].encode('utf-8').strip().decode("utf-8"))
                deadline_value_ = str(request.get_json()['deadline_value'].encode('utf-8').strip().decode("utf-8"))
                id_classroom_ = str(request.get_json()['id_classroom'].encode('utf-8').strip().decode("utf-8"))
                category_ = str(request.get_json()['category'].encode('utf-8').strip().decode("utf-8"))
                Payload = {"title": title_, "description": description_,
                           "photo": photo_, "aim": aim_, "deadline_type": deadline_type_,
                           "deadline_value": deadline_value_, "id_classroom": id_classroom_, "category": category_}
                insert_request_log("/professor/challenge/edit/"+str(id_challenge), "PUT", str(Payload), ip_, data['email'])
                if iam_owner_of_this_challenge(id_challenge,data['email']):
                    if get_permission_by_user('Update_challenge', data['rol']) == 'True':
                        response = edit_challenge(id_challenge,title_, description_, photo_, aim_, deadline_type_, deadline_value_,
                                                 id_classroom_, category_)
                        if response >= 1:
                            message = 'ok'
                            code = 200
                        else:
                            message = 'Algo sucedió en la base de datos'
                            code = 503
                        response_str = str({'message': message, 'code': code, 'id_challenge': response})
                        insert_general_log(response_str, ip_, data['email'])
                        return jsonify({'message': message, 'code': code, 'id_challenge': response})
                    else:
                        message = 'Acción no permitida'
                        code = 403
                        response_str = str({'message': message, 'code': code})
                        insert_general_log(response_str, ip_, data['email'])
                        return jsonify({'message': message, 'code': code})
        except Exception as e:
            message = 'Se ha producido un error en nuestros servidores'
            code = 500
            response_str = str({'error': "/professor/challenge/edit/" + str(id_challenge), 'detalle': str(e)})
            insert_general_log(response_str, ip_, data['email'])
            return jsonify({'message': message, 'code': code})

@apinspd.route('/<id_challenge>/get_all_students', methods=['GET'])
@apinspd.doc(
    security='apikey',
    responses={
        200: 'Success',
        403: 'Forbidden',
        404: 'Token not found',
        500: 'Internal server error',
        503: 'Service Unavailable'
    }
)
class _get_all_students_(Resource):
    @token_required
    def get(self,id_challenge):
        """
        Obtiene lista de los estudiantes suscritos al desafío y el estado de cada uno
        """
        code = 500
        data = get_info_token()
        ip_ = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        insert_request_log("/professor/challenge/"+ str(id_challenge)+ "/get_all_students", "GET", "", ip_, data['email'])
        try:
            if data['rol'] == 'Professor':
                print(data['email'])
                if iam_owner_of_this_challenge(id_challenge,data['email']):
                    data_ = get_all_students_in_challenge(id_challenge)
                    response_str = {'message': data_ , 'code': 200}
                    insert_general_log(str(response_str), ip_, data['email'])
                    return jsonify(response_str)
                else:
                    response_str = {'message': 'Acción no permitida, probablemente no tienes la autorización necesaria', 'code': 403}
                    insert_general_log(str(response_str), ip_, data['email'])
                    return jsonify(response_str)
            else:
                return jsonify({'message': 'Acción no permitida' , 'code': 503})
        except Exception as e:
            message = 'Se ha producido un error en nuestros servidores'
            response_str = str({'error': "/professor/challenge/" +str(id_challenge) + "/get_all_students" , 'detalle': str(e)})
            insert_general_log(response_str, ip_, data['email'])
            return jsonify({'message': message, 'code': code})


# TEMPLATES
@apinspd.route('/template/create', methods=['POST'])
@apinspd.doc(
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
class profesor_create_a_template_challenge__(Resource):
    test_fields = apinspd.model('crear_template_desafio', {
        'title': fields.String(required=True, description='Título de desafío', example='Ejemlo de Título de desafío'),
        'description': fields.String(required=True, description='Descripción de desafío', example='Ejemplo de descripción de desafío'),
        'photo': fields.String(required=True, description='Foto en string (base64)', example=' data:image/png;base64,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'),
        'aim': fields.String(required=True, description='Objetivos del desafío', example='aprender a buscar, seleccionar fuentes relevantes'),
        'category': fields.String(required=True, description='Categoría a la cual pertenece el desafío a ingresar', example='matemática')
    })

    @apinspd.expect(test_fields)
    @token_required
    def post(self):
        """Crear nuevo template de desafío"""
        data = get_info_token()
        ip_ = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        try:

            title_ = str(request.get_json()['title'].encode('utf-8').strip().decode("utf-8"))
            description_ = str(request.get_json()['description'].encode('utf-8').strip().decode("utf-8"))
            photo_ = str(request.get_json()['photo'].encode('utf-8').strip().decode("utf-8"))
            aim_ = str(request.get_json()['aim'].encode('utf-8').strip().decode("utf-8"))
            category_ = str(request.get_json()['category'].encode('utf-8').strip().decode("utf-8"))
            Payload = {"title": title_, "description": description_,
                       "photo": photo_, "aim": aim_, "category": category_}
            insert_request_log("/professor/challenge/template/create", "POST", str(Payload), ip_, data['email'])
            if get_permission_by_user('Create_challenge', data['rol']) == 'True':
                response = new_template_challenge(title_, description_, photo_, aim_, category_, data['email'])
                if response >=1:
                    message = 'ok'
                    code = 200
                else:
                    message = 'Algo sucedió en la base de datos'
                    code = 503
                response_str = {'message': message, 'code': code, 'id_challenge_template':response}
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
            response_str = str({'error': "/template/create", 'detalle': str(e)})
            insert_general_log(response_str, ip_, data['email'])
            return jsonify({'message': message, 'code': code})



@apinspd.route('/template', methods=['GET'])
@apinspd.doc(
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
class profesor_get_all_template_challenges__(Resource):
    @token_required
    def get(self):
        """
        Obtener todos los templates desafíos (Creados por el profesor y otros profesores)
        <strong>Se obtiene un arreglo de los siguientes datos:</strong>
        -[0] Id de template del desafio\n
        -[1] Título\n
        -[2] Descripción\n
        -[3] Foto (base64)\n
        -[4] Objetivos\n
        -[5] Fecha de creación\n
        -[6] Ultima vez modificado\n
        -[8] Estado [Show]\n
        -[9] Categoría del desafío\n
        -[10] Creado por [email del usuario]\n
        """
        data = get_info_token()
        ip_ = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        try:

            insert_request_log("/professor/challenge/template/", "GET", "", ip_, data['email'])
            if get_permission_by_user('Read_challenge', data['rol']) == 'True':
                response = get_all_templates_challenge()
                response_str = {'message': 'Template de todos los desafíos disponibles', 'code': 200, 'template_challenge':response}
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
            response_str = str({'error': "/template", 'detalle': str(e)})
            insert_general_log(response_str, ip_, data['email'])
            return jsonify({'message': message, 'code': code})


@apinspd.route('/template/edit/<id_challenge>', methods=['PUT'])
@apinspd.doc(
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
class professor_edit_a_template_challenge__(Resource):
    test_fields = apinspd.model('editar_template_desafio', {
        'title': fields.String(required=True, description='Título de desafío', example='Ejemlo de Título de desafío'),
        'description': fields.String(required=True, description='Descripción de desafío', example='Ejemplo de descripción de desafío'),
        'photo': fields.String(required=True, description='Foto en string (base64)', example=' data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAOCAYAAAAWo42rAAAMSmlDQ1BJQ0MgUHJvZmlsZQAASImVVwdYU8kWnltSSWiBCEgJvYlSpEsJoUUQkCrYCEkgocSQEETsLssquHYRARu6KqLoWgBZK+paF8HuWh6KqCjrYsGGypsUWNf93nvfO9839/45c85/SubeOwOATg1PKs1FdQHIkxTI4iNCWJNS01ikLkADOkAbeAE3Hl8uZcfFRQMoQ/e/y9sbAFHer7oouf45/19FTyCU8wFA4iDOEMj5eRAfBAAv4UtlBQAQfaDeemaBVImnQGwggwlCLFXiLDUuUeIMNa5U2STGcyDeDQCZxuPJsgDQboZ6ViE/C/Jo34LYVSIQSwDQIUMcyBfxBBBHQjwqL2+GEkM74JDxFU/W3zgzhjl5vKxhrK5FJeRQsVyay5v1f7bjf0termIohh0cNJEsMl5ZM+zbrZwZUUpMg7hXkhETC7E+xO/FApU9xChVpIhMUtujpnw5B/YMMCF2FfBCoyA2hThckhsTrdFnZIrDuRDDFYIWiQu4iRrfxUJ5WIKGs0Y2Iz52CGfKOGyNbwNPpoqrtD+tyElia/hviYTcIf43xaLEFHXOGLVQnBwDsTbETHlOQpTaBrMpFnFihmxkinhl/jYQ+wklESFqfmxapiw8XmMvy5MP1YstFom5MRpcVSBKjNTw7ObzVPkbQdwslLCThniE8knRQ7UIhKFh6tqxdqEkSVMv1iktCInX+L6S5sZp7HGqMDdCqbeC2FRemKDxxQML4IJU8+Mx0oK4RHWeeEY2b3ycOh+8CEQDDggFLKCAIwPMANlA3Nbb1At/qWfCAQ/IQBYQAheNZsgjRTUjgdcEUAz+gEgI5MN+IapZISiE+s/DWvXVBWSqZgtVHjngMcR5IArkwt8KlZdkOFoyeAQ14n9E58Ncc+FQzv1Tx4aaaI1GMcTL0hmyJIYRQ4mRxHCiI26CB+L+eDS8BsPhjvvgvkPZ/mVPeEzoIDwkXCd0Em5PFy+SfVMPC0wAnTBCuKbmjK9rxu0gqyceggdAfsiNM3ET4IKPhZHYeBCM7Qm1HE3myuq/5f5bDV91XWNHcaWglBGUYIrDt57aTtqewyzKnn7dIXWuGcN95QzPfBuf81WnBfAe9a0lthg7gJ3FTmLnsSNYE2Bhx7Fm7BJ2VImHV9Ej1SoaihavyicH8oj/EY+nianspNy13rXH9ZN6rkBYpHw/As4M6SyZOEtUwGLDN7+QxZXwR49iubu6+QKg/I6oX1OvmarvA8K88Jcu/wQAvmVQmfWXjmcNwOHHADDe/qWzfgUfjxUAHG3nK2SFah2uvBAAFX6hDIAxMAfWwAHW4w6/Vv4gGISB8SAWJIJUMA12WQTXswzMBHPAQlAKysEKsBZUgU1gK9gJ9oD9oAkcASfBr+AiaAfXwR24errBc9AH3oIBBEFICB1hIMaIBWKLOCPuiA8SiIQh0Ug8koqkI1mIBFEgc5DvkHJkFVKFbEHqkJ+Rw8hJ5DzSgdxGHiA9yCvkI4qhNNQANUPt0DGoD8pGo9BEdCqaheajxWgJugytRGvR3WgjehK9iF5HO9HnaD8GMC2MiVliLpgPxsFisTQsE5Nh87AyrAKrxRqwFvg/X8U6sV7sA07EGTgLd4ErOBJPwvl4Pj4PX4pX4TvxRvw0fhV/gPfhXwh0ginBmeBH4BImEbIIMwmlhArCdsIhwhn4NHUT3hKJRCbRnugNn8ZUYjZxNnEpcQNxL/EEsYPYRewnkUjGJGdSACmWxCMVkEpJ60m7ScdJV0jdpPdkLbIF2Z0cTk4jS8iLyBXkXeRj5CvkJ+QBii7FluJHiaUIKLMoyynbKC2Uy5RuygBVj2pPDaAmUrOpC6mV1AbqGepd6mstLS0rLV+tiVpirQValVr7tM5pPdD6QNOnOdE4tCk0BW0ZbQftBO027TWdTrejB9PT6AX0ZfQ6+in6ffp7bYb2aG2utkB7vna1dqP2Fe0XOhQdWx22zjSdYp0KnQM6l3V6dSm6drocXZ7uPN1q3cO6N3X79Rh6bnqxenl6S/V26Z3Xe6pP0rfTD9MX6Jfob9U/pd/FwBjWDA6Dz/iOsY1xhtFtQDSwN+AaZBuUG+wxaDPoM9Q3HGuYbFhkWG141LCTiTHtmFxmLnM5cz/zBvPjCLMR7BHCEUtGNIy4MuKd0UijYCOhUZnRXqPrRh+NWcZhxjnGK42bjO+Z4CZOJhNNZppsNDlj0jvSYKT/SP7IspH7R/5uipo6mcabzjbdanrJtN/M3CzCTGq23uyUWa850zzYPNt8jfkx8x4LhkWghdhijcVxi2csQxablcuqZJ1m9VmaWkZaKiy3WLZZDljZWyVZLbLaa3XPmmrtY51pvca61brPxsJmgs0cm3qb320ptj62Itt1tmdt39nZ26XY/WDXZPfU3siea19sX29/14HuEOSQ71DrcM2R6OjjmOO4wbHdCXXydBI5VTtddkadvZzFzhucO0YRRvmOkoyqHXXThebCdil0qXd5MJo5Onr0otFNo1+MsRmTNmblmLNjvrh6uua6bnO946bvNt5tkVuL2yt3J3e+e7X7NQ+6R7jHfI9mj5djnccKx24ce8uT4TnB8wfPVs/PXt5eMq8Grx5vG+907xrvmz4GPnE+S33O+RJ8Q3zn+x7x/eDn5Vfgt9/vT38X/xz/Xf5Px9mPE47bNq4rwCqAF7AloDOQFZgeuDmwM8gyiBdUG/Qw2DpYELw9+AnbkZ3N3s1+EeIaIgs5FPKO48eZyzkRioVGhJaFtoXphyWFVYXdD7cKzwqvD++L8IyYHXEikhAZFbky8ibXjMvn1nH7xnuPnzv+dBQtKiGqKuphtFO0LLplAjph/ITVE+7G2MZIYppiQSw3dnXsvTj7uPy4XyYSJ8ZNrJ74ON4tfk782QRGwvSEXQlvE0MSlyfeSXJIUiS1JuskT0muS36XEpqyKqVz0phJcyddTDVJFac2p5HSktO2p/VPDpu8dnL3FM8ppVNuTLWfWjT1/DSTabnTjk7Xmc6bfiCdkJ6Sviv9Ey+WV8vrz+Bm1GT08Tn8dfzngmDBGkGPMEC4SvgkMyBzVebTrICs1Vk9oiBRhahXzBFXiV9mR2Zvyn6XE5uzI2cwNyV3bx45Lz3vsERfkiM5PcN8RtGMDqmztFTame+Xvza/TxYl2y5H5FPlzQUGcMN+SeGg+F7xoDCwsLrw/czkmQeK9IokRZdmOc1aMutJcXjxT7Px2fzZrXMs5yyc82Aue+6Weci8jHmt863nl8zvXhCxYOdC6sKchb8tcl20atGb71K+aykxK1lQ0vV9xPf1pdqlstKbP/j/sGkxvli8uG2Jx5L1S76UCcoulLuWV5R/WspfeuFHtx8rfxxclrmsbbnX8o0riCskK26sDFq5c5XequJVXasnrG5cw1pTtubN2ulrz1eMrdi0jrpOsa6zMrqyeb3N+hXrP1WJqq5Xh1TvrTGtWVLzboNgw5WNwRsbNpltKt/0cbN4860tEVsaa+1qK7YStxZufbwtedvZn3x+qttusr18++cdkh2dO+N3nq7zrqvbZbpreT1ar6jv2T1ld/ue0D3NDS4NW/Yy95bvA/sU+579nP7zjf1R+1sP+BxoOGh7sOYQ41BZI9I4q7GvSdTU2Zza3HF4/OHWFv+WQ7+M/mXHEcsj1UcNjy4/Rj1WcmzwePHx/hPSE70ns052tU5vvXNq0qlrpyeebjsTdebcr+G/njrLPnv8XMC5I+f9zh++4HOh6aLXxcZLnpcO/eb526E2r7bGy96Xm9t921s6xnUcuxJ05eTV0Ku/XuNeu3g95nrHjaQbt25Oudl5S3Dr6e3c2y9/L/x94M6Cu4S7Zfd071XcN71f+y/Hf+3t9Oo8+iD0waWHCQ/vdPG7nj+SP/rUXfKY/rjiicWTuqfuT4/0hPe0P5v8rPu59PlAb+kfen/UvHB4cfDP4D8v9U3q634pezn4aulr49c73ox909of13//bd7bgXdl743f7/zg8+Hsx5SPTwZmfiJ9qvzs+LnlS9SXu4N5g4NSnoyn2gpgcKCZmQC82gEAPRXuHdoBoE5Wn/NUgqjPpioE/hNWnwVV4gXAjmAAkhYAEA33KBvhsIWYBu/KrXpiMEA9PIaHRuSZHu5qLho88RDeDw6+NgOA1ALAZ9ng4MCGwcHP22CytwE4ka8+XyqFCM8Gm52U6PI4nWLwjfwbZ7F+i5OEl9MAAAAJcEhZcwAAFiUAABYlAUlSJPAAAAGbaVRYdFhNTDpjb20uYWRvYmUueG1wAAAAAAA8eDp4bXBtZXRhIHhtbG5zOng9ImFkb2JlOm5zOm1ldGEvIiB4OnhtcHRrPSJYTVAgQ29yZSA1LjQuMCI+CiAgIDxyZGY6UkRGIHhtbG5zOnJkZj0iaHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyI+CiAgICAgIDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiCiAgICAgICAgICAgIHhtbG5zOmV4aWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20vZXhpZi8xLjAvIj4KICAgICAgICAgPGV4aWY6UGl4ZWxYRGltZW5zaW9uPjEwPC9leGlmOlBpeGVsWERpbWVuc2lvbj4KICAgICAgICAgPGV4aWY6UGl4ZWxZRGltZW5zaW9uPjE0PC9leGlmOlBpeGVsWURpbWVuc2lvbj4KICAgICAgPC9yZGY6RGVzY3JpcHRpb24+CiAgIDwvcmRmOlJERj4KPC94OnhtcG1ldGE+Ct0tKCsAAAAcaURPVAAAAAIAAAAAAAAABwAAACgAAAAHAAAABwAAAMhYYTAFAAAAlElEQVQoFSSPARLDIAgE7/AJST6Ttr/stP2s0EUdYxD3DvBxvyvCCodqpnp5hLIIgph/cvFxfwpO7LWyShGDONWsOPvNJ6D7EnweW23zaM3Ot7CNzscXMIFajWTZgJGY1G3vJbueOO4a6AmWgOaIE5h2hbW8QYDeQEwmulgV1mi4OPG8Xj8cNzhpIQb0Hh6APCsR/wEAAP//r15TYwAAAJNJREFULZCLEcIwDEPllA2gxy5QxiwwLK14cpucc4mtj526L1/v3qUyMamXreQmlchyEvPzbY0jMXbL05B/m2qk2hAJIsAPZ99hW5eQKGxIBWuUC1bNL4AUSLVFyoZYAYeKy6Clui0rrzpcUKO5eDYxDka6278+Vhe9RN4D0DlXHBIxizqKDINCwK3Aq+fon4B87j+DhJecoSYYRAAAAABJRU5ErkJggg=='),
        'aim': fields.String(required=True, description='Objetivos del desafío', example='aprender a buscar, seleccionar fuentes relevantes'),
        'category': fields.String(required=True, description='Categoría a la cual pertenece el desafío a ingresar', example='matemática')
    })

    @apinspd.expect(test_fields)
    @token_required
    def put(self,id_challenge):
        """Editar template de desafío , creado por el usuario"""
        data = get_info_token()
        ip_ = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        try:
            title_ = str(request.get_json()['title'].encode('utf-8').strip().decode("utf-8"))
            description_ = str(request.get_json()['description'].encode('utf-8').strip().decode("utf-8"))
            photo_ = str(request.get_json()['photo'].encode('utf-8').strip().decode("utf-8"))
            aim_ = str(request.get_json()['aim'].encode('utf-8').strip().decode("utf-8"))
            category_ = str(request.get_json()['category'].encode('utf-8').strip().decode("utf-8"))
            Payload = {"title": title_, "description": description_,
                       "photo": photo_, "aim": aim_, "category": category_}
            insert_request_log("/professor/challenge/template/edit/" + str(id_challenge), "PUT", str(Payload), ip_, data['email'])
            if get_permission_by_user('Update_challenge', data['rol']) == 'True':
                response = edit_template_challenge(id_challenge, title_, description_, photo_, aim_, category_, data['email'])
                if response >=1:
                    message = 'ok'
                    code = 200
                else:
                    message = 'No se pudo editar el desafío, probablemente no tienes los suficientes permisos. Por favor, contacta con el administrador'
                    code = 403
                response_str = {'message': message, 'code': code, 'id_challenge_template':response}
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
            response_str = str({'error': "/template/edit/"+ str(id_challenge), 'detalle': str(e)})
            insert_general_log(response_str, ip_, data['email'])
            return jsonify({'message': message, 'code': code})