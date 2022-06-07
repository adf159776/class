from flask_restful import reqparse
import pymysql
from flask import jsonify
import util, model
from flask_apispec import doc, use_kwargs, MethodResource, marshal_with
from model import UserGetResponse, UseranotherResponse, \
    UserPostRequest, UserPatchRequest
from datetime import timedelta

def db_init():
    db = pymysql.connect(
        host='219.91.64.26',
        user='super',
        password='0104',
        port=3306,
        db='api_class'
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)
    return db, cursor

class product(MethodResource):
    
    @doc(description="Get products info", tags=['cart'])
    def get(self):
        db, cursor = db_init()
        
        
        sql1 = "SELECT * FROM api_class.cart;"
        cursor.execute(sql1)
        products = cursor.fetchall()
        
        sql2 = "SELECT sum(price*quantity) as total FROM api_class.cart;"
        cursor.execute(sql2)
        total = cursor.fetchall()
        
        re={"products":products,"total":total}
        db.close()
        return re
    
    @doc(description="Post products info", tags=['cart'])
    @use_kwargs(UserPostRequest,location="json")
    @marshal_with(UseranotherResponse, code=200)

    def post(self,**kwargs):
        db, cursor = db_init()

        product = {
            'product': kwargs['product'],
            'price': kwargs['price'],
            'quantity': kwargs['quantity']
        }
        sql = """
        INSERT INTO `api_class`.`cart` (`product`,`price`,`quantity`)
        VALUES ('{}','{}','{}');
        """.format(
            product['product'], product['price'], product['quantity'])
            
        result = cursor.execute(sql)
        
        db.commit()
        db.close()

        if result == 1:
            return util.success()
                
        return util.failure()

class edit(MethodResource):
    @doc(description="Patch product info", tags=['cart'])
    @use_kwargs(UserPatchRequest,location="json")
    @marshal_with(UseranotherResponse, code=200)

    def patch(self, name,**kwargs):
        db, cursor = db_init()
      
        product = {
            'product': kwargs.get('product'),
            'price': kwargs.get('price'),
            'quantity': kwargs.get('quantity')
        }

        query = []
  
        for key, value in product.items():
            if value is not None:
                query.append(f"{key} = '{value}'")
        query = ",".join(query)
        '''
        UPDATE table_name
        SET column1=value1, column2=value2, column3=value3···
        WHERE some_column=some_value;
        '''
        sql = """
            UPDATE api_class.cart
            SET {}
            WHERE product = '{}';
        """.format(query, name)

        result = cursor.execute(sql)
        
        db.commit()
        db.close()
        
        if result == 1:
            return util.success()
                
        return util.failure()

    @doc(description="Delete product info", tags=['cart'])
    @marshal_with(UseranotherResponse, code=200)

    def delete(self, name):
        db, cursor = db_init()
        sql = f"DELETE FROM `api_class`.`cart` WHERE product = '{name}';"
        result = cursor.execute(sql)
        message = "success" if result == 1 else "failure"
        db.commit()
        db.close()

        if result == 1:
            return util.success()
                
        return util.failure()

    @doc(description="Get products info", tags=['cart'])
    def get(self, name):
        db, cursor = db_init()

        sql1 = f"SELECT * FROM api_class.cart where product like '%{name}%';"
        cursor.execute(sql1)
        products = cursor.fetchall()

        
        sql2 = f"SELECT sum(price*quantity) as total FROM api_class.cart where product like '%{name}%';"
        cursor.execute(sql2)
        total = cursor.fetchall()
        
        re={"products":products,"total":total}
        db.close()
        return re
