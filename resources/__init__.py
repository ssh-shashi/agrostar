from flask_cors import CORS
from flask_restplus import Api
from resources.wallet import WalletCrud,TransactionCrud,WalletTransaction,RevertTransaction
__author__ = 'shashi rest api '


def create_restful_api(app):
    api = Api(app)

    CORS(app, resources={r"*": {"origins": "*"}})

    api.add_resource(WalletCrud, '/wallets/<string:wallet_id>',endpoint="get wallet balance")
    api.add_resource(TransactionCrud, '/wallets/<string:wallet_id>/transaction',endpoint="get wallet all transaction")
    api.add_resource(WalletTransaction, '/wallet/<string:wallet_id>/transaction/<string:transaction_id>',endpoint="delete_transaction")
    api.add_resource(RevertTransaction, '/wallets/<string:wallet_id>/transaction/<string:transaction_id>',endpoint="revert transaction")
    
   