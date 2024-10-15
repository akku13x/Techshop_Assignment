from datetime import datetime

class Order:
    def __init__(self, customer_id, order_date, total_amount):
        self.__order_id = None  # Will be set when inserting into the database
        self.__customer_id = customer_id
        self.__order_date = order_date  # Updated to accept order date
        self.__total_amount = total_amount

    @property
    def order_id(self):
        return self.__order_id

    @property
    def customer_id(self):
        return self.__customer_id

    @property
    def order_date(self):
        return self.__order_date

    @property
    def total_amount(self):
        return self.__total_amount
