from marshmallow import Schema, fields, post_load

class TransactionSchema(Schema):
    version = fields.Int(required=True)
    locktime = fields.Int(required=True)
    vin = fields.List(fields.Dict(), required=True)
    vout = fields.List(fields.Dict(), required=True)

    @post_load
    def make_transaction(self, data, **kwargs):
        return Transaction(**data)