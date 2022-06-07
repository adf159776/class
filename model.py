from marshmallow import Schema, fields

# Parameter (Schema)
class UserPostRequest(Schema):
    product = fields.Str(doc="product", required=True)
    price = fields.Str(doc="price", required=True)
    quantity = fields.Str(doc="quantity", required=True)

class UserPatchRequest(Schema):
    product = fields.Str(doc="product")
    price = fields.Str(doc="price")
    quantity = fields.Str(doc="quantity")



class UseranotherResponse(Schema):
    message = fields.Str(example="success")

# Get 
class UserGetResponse(UseranotherResponse):
    data = fields.List(
        fields.Dict(), 
        example={
    "products": [
        {
            "id": 6,
            "price": 20,
            "product": "apple",
            "quantity": 1
        }
    ],
    "total": [
        {
            "sum(price*quantity)": "20"
        }
    ]
}
    )
    datetime = fields.Str()
