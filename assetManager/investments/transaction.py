class Transaction:
    def __init__(self, transaction_json, ticker):
        self.quantity = transaction_json['quantity']
        self.price = transaction_json['price']
        self.amount = transaction_json['amount']
        self.security_id = transaction_json['security_id']
        self.ticker = ticker