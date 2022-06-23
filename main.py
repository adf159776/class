pip3 install flask==2.0.3
pip3 install Flask-RESTful==0.3.9
pip3 install flask-apispec==0.11.0
pip3 install Flask-JWT-Extended==4.3.1

from flask import Flask
from flask_restful import Api
from user import Users,User,Login
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_jwt_extended import JWTManager

app = Flask(__name__)
api = Api(app)

app.config["JWT_SECRET_KEY"] = "secret_key"
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Awesome Project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)

api.add_resource(Users, '/user')
docs.register(Users)
api.add_resource(User, '/user/<int:id>')
docs.register(User)
api.add_resource(Login, '/Login')
docs.register(Login)

if __name__ == '__main__':
    JWTManager().init_app(app)
    app.run(debug=True)
