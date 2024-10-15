# entity/payment.py

class Payment:
    def __init__(self, order_id, payment_method, amount, payment_date):
        self.order_id = order_id
        self.payment_method = payment_method
        self.amount = amount
        self.payment_date = payment_date

    # Getters and setters for encapsulation
    def get_order_id(self):
        return self.order_id

    def set_order_id(self, order_id):
        self.order_id = order_id

    def get_payment_method(self):
        return self.payment_method

    def set_payment_method(self, payment_method):
        self.payment_method = payment_method

    def get_amount(self):
        return self.amount

    def set_amount(self, amount):
        self.amount = amount

    def get_payment_date(self):
        return self.payment_date

    def set_payment_date(self, payment_date):
        self.payment_date = payment_date
