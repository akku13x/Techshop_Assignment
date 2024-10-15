from abc import ABC, abstractmethod

class ServiceProvider(ABC):

    @abstractmethod
    def add_customer(self, customer):
        pass

    @abstractmethod
    def add_product(self, product):
        pass

    @abstractmethod
    def place_order(self, order, order_details):
        pass

    @abstractmethod
    def get_product_price(self, product_id):
        pass

    @abstractmethod
    def update_product_quantity(self, product_id, new_quantity):
        pass

    @abstractmethod
    def get_order_status(self, order_id):
        pass

    @abstractmethod
    def track_order_status(self, order_id):
        pass

    @abstractmethod
    def generate_sales_report(self, start_date, end_date):
        pass

    @abstractmethod
    def update_customer_info(self, customer_id, email=None, phone=None):
        pass

    @abstractmethod
    def process_payment(self, payment):
        pass

    @abstractmethod
    def search_products_by_category(self, category):
        pass

    @abstractmethod
    def delete_product(self, product_id):
        pass

    @abstractmethod
    def list_customers(self):  # New method
        pass

    @abstractmethod
    def get_order_total(self, customer_id, order_id):  # New method
        pass