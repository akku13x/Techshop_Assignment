# entity/order_detail.py

class OrderDetail:
    def __init__(self, order_detail_id, product_id, quantity):
        self.__order_detail_id = order_detail_id
        self.__product_id = product_id
        self.__quantity = quantity

    @property
    def order_detail_id(self):
        return self.__order_detail_id

    @property
    def product_id(self):
        return self.__product_id

    @property
    def quantity(self):
        return self.__quantity

    def calculate_subtotal(self, product_price):
        return product_price * self.__quantity

    def get_order_detail_info(self):
        return f"Order Detail ID: {self.order_detail_id}, Product ID: {self.product_id}, Quantity: {self.quantity}"
