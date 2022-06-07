from flask_restful import reqparse
import pymysql
from flask import jsonify
import util, user_route_model
from flask_apispec import doc, use_kwargs, MethodResource, marshal_with
from user_route_model import UserGetResponse, UseranotherResponse, \
    UserPostRequest, UserPatchRequest, LoginReqest
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta

def db_init():
    db = pymysql.connect(
        host='192.168.66.26',
        user='super',
        password='0104',
        port=3306,
        db='api_class'
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)
    return db, cursor

def get_access_token(account):
    token = create_access_token(
        identity={"account": account},
        expires_delta=timedelta(days=1)
    )
    return token

class Users(MethodResource):
    @doc(description="Get users info", tags=['User'])
    @jwt_required()
    @marshal_with(UserGetResponse, code=200)
    def get(self):
        db, cursor = db_init()

        sql = "SELECT * FROM api_class.member;"
        cursor.execute(sql)

        users = cursor.fetchall()
        db.close()
        return util.success(users)
    
    @doc(description="Post users info", tags=['User'])
    @use_kwargs(UserPostRequest,location="json")
    @marshal_with(UseranotherResponse, code=200)

    def post(self,**kwargs):
        db, cursor = db_init()

        user = {
            'name': kwargs['name'],
            'gender': kwargs['gender'],
            'birth': kwargs.get('birth') or '1900-01-01',
            'note': kwargs.get('note'),
            'account':kwargs.get('account'),
            'password':kwargs.get('password')
        }
        sql = """

        INSERT INTO `api_class`.`member` (`name`,`gender`,`account`,`password`,`birth`,`note`)
        VALUES ('{}','{}','{}','{}','{}','{}');

        """.format(
            user['name'], user['gender'], user['account'], user['password'], user['birth'], user['note'])
            
        result = cursor.execute(sql)
        
        db.commit()
        db.close()

        if result == 1:
            return util.success()
                
        return util.failure()

class User(MethodResource):
    @doc(description="Patch users info", tags=['User'])
    @use_kwargs(UserPatchRequest,location="json")
    @marshal_with(UseranotherResponse, code=200)

    def patch(self, id,**kwargs):
        db, cursor = db_init()
      
        user = {
            'name': kwargs.get('name'),
            'gender': kwargs.get('gender'),
            'birth': kwargs.get('birth'),
            'note': kwargs.get('note'),
            'account':kwargs.get('account'),
            'password':kwargs.get('password')
        }

        query = []
        print(user)
        '''{'name': None, 'gender': 'Double', 'birth': None, 'note': None}'''
        for key, value in user.items():
            if value is not None:
                query.append(f"{key} = '{value}'")
        query = ",".join(query)
        '''
        UPDATE table_name
        SET column1=value1, column2=value2, column3=value3···
        WHERE some_column=some_value;

        '''
        sql = """
            UPDATE api_class.member
            SET {}
            WHERE id = {};
        """.format(query, id)

        result = cursor.execute(sql)
        
        db.commit()
        db.close()
        
        if result == 1:
            return util.success()
                
        return util.failure()

    @doc(description="Delete users info", tags=['User'])
    @marshal_with(UseranotherResponse, code=200)

    def delete(self, id):
        db, cursor = db_init()
        sql = f'DELETE FROM `api_class`.`member` WHERE id = {id};'
        result = cursor.execute(sql)
        message = "success" if result == 1 else "failure"
        db.commit()
        db.close()

        if result == 1:
            return util.success()
                
        return util.failure()

class Login(MethodResource):
    @doc(description='User Login', tags=['Login'])
    @use_kwargs(user_route_model.LoginReqest, location="json")
    # @marshal_with(user_router_model.UserGetResponse, code=200)
    def post(self, **kwargs):
        db, cursor = db_init()
        account, password = kwargs["account"], kwargs["password"]
        sql = f"SELECT * FROM api_class.member WHERE account = '{account}' AND password = '{password}';"
        cursor.execute(sql)
        user = cursor.fetchall()
        db.close()

        if user != ():
            token = get_access_token(account)
            data = {
                "message": f"Welcome back {user[0]['name']}",
                "token": token}
            return util.success(data)
        
        return util.failure({"message":"Account or password is wrong"})
