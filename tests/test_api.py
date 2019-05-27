import unittest
import requests
import json
import sys

class TestFlaskApiUsingRequests(unittest.TestCase):

    def test_wallet_getbalance(self):
        wallet_id = 1
        response = requests.get('http://127.0.0.1:5000/wallets/'+str(wallet_id))
        self.assertEqual(response.json()['message'], 'ok')
    def test_wallet_gettransaction_via_id(self):
        wallet_id = 1
        transaction_id = 6
        response = requests.get('http://127.0.0.1:5000/wallets/'+str(wallet_id)+'/transaction/'+str(transaction_id))
        self.assertEqual(response.json()['message'], 'ok')
    def test_wallet_getall_transaction(self):
        response = requests.get('http://127.0.0.1:5000/wallets/1/transaction')
        self.assertEqual(response.json()['message'], 'ok')
    def test_delete_transaction(self):
        wallet_id = 1
        transaction_id = 10
        response = requests.delete('http://127.0.0.1:5000/wallets/'+str(wallet_id)+'/transaction/'+str(transaction_id))
        self.assertEqual(response.json()['message'], 'ok')
    def test_do_transaction(self):
        payload = {
                     "amount":60,
                     "type":"CREDIT"
                    }
        payload = json.dumps(payload)
        response = requests.post('http://127.0.0.1:5000/wallets/1/transaction',data=payload)
        self.assertEqual(response.json()['message'], 'ok')
    



if __name__ == "__main__":
    unittest.main()