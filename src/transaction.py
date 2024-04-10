from marshmallow import Schema, fields, post_load

class TransactionSchema(Schema):
    version = fields.Int(required=True)
    locktime = fields.Int(required=True)
    vin = fields.List(fields.Dict(), required=True)
    vout = fields.List(fields.Dict(), required=True)

    @post_load
    def make_transaction(self, data, **kwargs):
        return Transaction(**data)

class Transaction:
    """
    This class holds method for managing transactions
    """
    def __init__(self, version, locktime, vin, vout) -> None:
        self.version = version
        self.locktime = version
        self.vin = vin
        self.vout = vout
