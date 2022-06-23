from marshmallow import Schema, fields

# Parameter (Schema)
class UserPostRequest(Schema):
    name = fields.Str(doc="name", required=True)
    gender = fields.Str(doc="gender", required=True)
    birth = fields.Str(doc="birth", required=True)
    note = fields.Str(doc="note")
    account = fields.Str(doc="account", required=True)
    password = fields.Str(doc="password", required=True)

class UserPatchRequest(Schema):
    name = fields.Str(doc="name")
    gender = fields.Str(doc="gender")
    birth = fields.Str(doc="birth")
    note = fields.Str(doc="note")
    account = fields.Str(doc="account")
    password = fields.Str(doc="password")



class UseranotherResponse(Schema):
    message = fields.Str(example="success")

# Get 
class UserGetResponse(UseranotherResponse):
    data = fields.List(
        fields.Dict(), 
        example={
            "id": 1,
            "name": "name",
            "birth": "1970/01/01",
            "gender": "male",
            "note": ""
        }
    )
    datetime = fields.Str()


class LoginReqest(Schema):
    account = fields.Str(doc="account", required=True)
    password = fields.Str(doc="password", required=True)
