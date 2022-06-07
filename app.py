from flask import Flask
from flask_restful import Api
from user import Users,User,Login
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_jwt_extended import JWTManager

app = Flask(__name__)
api = Api(app)

