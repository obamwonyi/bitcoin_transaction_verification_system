from marshmallow import Schema, fields, post_load

class PrevOutSchema(Schema):
    scriptpubkey = fields.Str(required=True)
    scriptpubkey_asm = fields.Str(required=True)
    scriptpubkey_type = fields.Str(required=True)
    scriptpubkey_address = fields.Str(required=True)
    value = fields.Int(required=True)

class VinSchema(Schema):
    txid = fields.Str(required=True)
    vout = fields.Int(required=True)
    prevout = fields.Nested(PrevOutSchema, required=True)
    scriptsig = fields.Str(required=True)
    scriptsig_asm = fields.Str(required=True)
    witness = fields.List(fields.Str(), required=False)
    is_coinbase = fields.Bool(required=True)
    sequence = fields.Int(required=True)
    inner_redeemscript_asm = fields.Str(required=False)
    inner_witnessscript_asm = fields.Str(required=False)

class VoutSchema(Schema):
    scriptpubkey = fields.Str(required=True)
    scriptpubkey_asm = fields.Str(required=True)
    scriptpubkey_type = fields.Str(required=True)
    scriptpubkey_address = fields.Str(required=False)
    value = fields.Int(required=True)

class TransactionSchema(Schema):
    version = fields.Int(required=True)
    locktime = fields.Int(required=True)
    vin = fields.List(fields.Nested(VinSchema), required=True)
    vout = fields.List(fields.Nested(VoutSchema), required=True)

    @post_load
    def make_transaction(self, data, **kwargs):
        return Transaction(**data)

class Transaction:
    """
    This class holds method for managing transactions
    """
    def __init__(self, version, locktime, vin, vout) -> None:
        self.version = version
        self.locktime = locktime
        self.vin = vin
        self.vout = vout
