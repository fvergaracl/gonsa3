import jwt
from functools import wraps
from flask import jsonify, request
from settings.configs import Config

c = Config()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            tokenTEMP = request.headers['Authorization']
            token = tokenTEMP.split(" ")
            if not tokenTEMP:
                # token not found
                return jsonify({'message': 'Token not found', 'code': 404})
            try:
                # token valid
                data = jwt.decode(token[1], c.get_jwt_secret_key())
            except Exception as e:
                # token not valid
                return jsonify({'message': 'Token not valid', 'code': 403})
            return f(*args, **kwargs)
        except KeyError:
            # token not found
            return jsonify({'message': 'Token not found', 'code': 404})
    return decorated


def get_info_token():
    tokenTEMP = request.headers['Authorization']
    token = tokenTEMP.split(" ")
    data = jwt.decode(token[1], c.get_jwt_secret_key())
    return data


def encode_jwt_data(data):
    return jwt.encode(data, c.get_jwt_secret_key())
