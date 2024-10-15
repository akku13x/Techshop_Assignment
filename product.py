class Product:
    def __init__(self, product_name, product_description, product_price, product_quantity, category):
        self.__product_id = None  # Will be set when inserting into the database
        self.__product_name = product_name
        self.__description = product_description
        self.__price = product_price
        self.__stock_quantity = product_quantity
        self.__category = category  # New attribute

    @property
    def product_id(self):
        return self.__product_id

    @property
    def product_name(self):
        return self.__product_name

    @property
    def description(self):
        return self.__description

    @property
    def price(self):
        return self.__price

    @property
    def stock_quantity(self):
        return self.__stock_quantity

    @stock_quantity.setter
    def stock_quantity(self, value):
        if value < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self.__stock_quantity = value

    @property
    def category(self):
        return self.__category
