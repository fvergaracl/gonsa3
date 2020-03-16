from flask import jsonify, request
from . import routes
from flask_restplus import Resource, Api, fields, Namespace
from functions.token_functions import token_required, get_info_token
from settings.configs import Config
from routes.professor.classs import apins
from routes.professor.challenges import apinspd
from routes.professor.rubics import apiprub
from routes.student.classs import api_student_class
from routes.student.challenges import apisch

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'authorization'
    }
}

api = Api(routes,
          version='3.1.1',
          title='REST API - GoNSa',
          contact='felipe.vergara@uach.cl',
          description='Endpoints for GoNSa3',
          default="API Endpoints - GoNSa3",
          authorizations=authorizations,

          doc='/doc/')
api.add_namespace(apins)
api.add_namespace(apinspd)
api.add_namespace(apiprub)
api.add_namespace(api_student_class)
api.add_namespace(apisch)
c = Config()