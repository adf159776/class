from flask import Flask
import pymysql
import json
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Erp Project API',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/api', # URI to access UI of API Doc
    'JSON_AS_ASCII': False
})
docs = FlaskApiSpec(app)

def db_init():
    db = pymysql.connect(
        host = os.getenv("dbip"),
        user = os.getenv("dbuser"),
        password = os.getenv("dbpassword"),
        port = int(os.getenv("dbport"))
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)
    return db, cursor

@app.route('/employees/<fullname>/punch')
def personpunch(fullname):
    db, cursor = db_init()
    cursor.execute(f"SELECT fullname,`inout`,FROM_UNIXTIME(timestamp, '%Y-%m-%d') date,FROM_UNIXTIME(timestamp, '%r') time,ipaddress FROM punch.`info` where fullname = '{fullname}' ORDER BY timestamp DESC;")
    data = json.dumps(cursor.fetchall())
    db.commit()
    cursor.close()
    db.close()

    return data

@app.route('/employees/<fullname>/punch/<int:yearmonth>')
def personpunchdate(fullname,yearmonth):
    db, cursor = db_init()
    cursor.execute(f"SELECT fullname,`inout`,FROM_UNIXTIME(timestamp, '%Y-%m-%d') date,FROM_UNIXTIME(timestamp, '%r') time,ipaddress FROM punch.`info` where fullname = '{fullname}' and FROM_UNIXTIME(timestamp, '%Y%m') = {yearmonth} ORDER BY timestamp DESC;")
    data = json.dumps(cursor.fetchall())
    db.commit()
    cursor.close()
    db.close()

    return data

docs.register(personpunch)
docs.register(personpunchdate)


if __name__ == '__main__':
    app.run()
