from flask_jwt import jwt_required, current_identity
from flask_restful import marshal_with, fields, reqparse
from models import session,Wallet,Transaction
from resources.base_resource import BaseResource as Resource
from flask import Response,request
import json
from sqlalchemy import text
from resource_exception import handle_exceptions
from flask import request, jsonify
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from marshmallow import Schema, fields, ValidationError, pre_load
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity,JWTManager)
__author__ = 'shashi'


# Custom validator
def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')

class WalletSchema(Schema):
    id = fields.Int(dump_only=True)
    amount = fields.Int(required=True,validate=must_not_be_blank)
    type = fields.Str(required=True,validate=must_not_be_blank)

wallet_schema = WalletSchema()



class WalletCrud(Resource):

    def get(self,**kwargs):
        try:
            wallet_id= int(kwargs.get('wallet_id'))
            user_obj = session.query(Wallet).filter(Wallet.id == wallet_id).first()
            user_obj = user_obj.to_dict()
            amount = user_obj['amount']
            return Response(json.dumps({'amount':amount,'message':'ok',}),status=200,  mimetype='application/json')
        except Exception as e:
            return Response(json.dumps({'message':'WALLET-ID-NOT-FOUND'}),  mimetype='application/json')



    
        



class TransactionCrud(Resource):

    def get(self,**kwargs):
        try:
            wallet_id= int(kwargs.get('wallet_id'))
            transaction_obj = session.query(Transaction).filter(Transaction.wallet_id == wallet_id).all()
            transactions = [r.to_dict() for r in transaction_obj]
            return Response(json.dumps({'transactions':transactions,'message':'ok',}),status=200,  mimetype='application/json')
        except Exception as e:
            return Response(json.dumps({'message':'WALLET-ID-NOT-FOUND'}),  mimetype='application/json')



    
class WalletTransaction(Resource):

    def delete(self,**kwargs):
        try:
            wallet_id= int(kwargs.get('wallet_id'))
            wallet_obj = session.query(Wallet).filter(Wallet.id == wallet_id).first()
            wallet_obj = wallet_obj.to_dict()
            try:
                transaction_id= int(kwargs.get('transaction_id'))
                transaction_obj=Transaction.query.filter_by(id=transaction_id).one()
                session.delete(transaction_obj)
                session.commit()
            except Exception as e:
                return Response(json.dumps({'message':'TRANSACTION-ID-NOT-FOUND'}),  mimetype='application/json')

            transaction_obj = transaction_obj.to_dict()
            if transaction_obj['type'] == "CREDIT":
                wallet_obj['amount'] = wallet_obj['amount']-transaction_obj['amount']
            else:
                wallet_obj['amount'] = wallet_obj['amount']+transaction_obj['amount']

            wallet = Wallet(**wallet_obj)
            session.merge(wallet)
            session.commit()
            return Response(json.dumps({'transactionId':transaction_obj['id'],'message':'ok','status':"CANCELLED"}),status=200,  mimetype='application/json')
        except Exception as e:
            return Response(json.dumps({'message':'WALLET-ID-NOT-FOUND'}),  mimetype='application/json')


class RevertTransaction(Resource):
    def post(self,**kwargs):

        try:
            wallet_data ={}
            transact_data ={}
            wallet_id= int(kwargs.get('wallet_id'))
            req_data = json.loads(request.data)
            try:
                wallet_id= int(kwargs.get('wallet_id'))
                data = wallet_schema.load(req_data)
            except ValidationError as err:
                return Response(json.dumps({'message':str(err)}),  mimetype='application/json')
            amount = req_data['amount']
            type = req_data['type']
            wallet_obj = session.query(Wallet).filter(Wallet.id == wallet_id).first()
            wallet_obj = wallet_obj.to_dict()
            # make a query to wallet table then update
            if type=="CREDIT":
                wallet_obj.update({'amount':amount+wallet_obj['amount']})
            elif type =="DEBIT" and wallet_obj['amount']-amount>=-50000:
                wallet_obj.update({'amount':wallet_obj['amount']-amount})
            else:
                raise Exception("INSUFFICENT-FUNDS")
            wallet = Wallet(**wallet_obj)
            session.merge(wallet)
            session.commit()
            transact_data.update({'amount':amount})
            transact_data.update({'type':type})
            transact_data.update({'wallet_id':wallet_id})
            transact = Transaction(**transact_data)
            session.add(transact)
            session.flush()
            session.commit()
            return Response(json.dumps({'transactionId':transact.id,'message':'ok',}),  mimetype='application/json')
        except Exception as e:
            return Response(json.dumps({'message':'TRANSACTION-FAILED'}),  mimetype='application/json')





        



