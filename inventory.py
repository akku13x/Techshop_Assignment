class Inventory:
    def __init__(self, inventory_id, product, quantity_in_stock):
        self.__inventory_id = inventory_id
        self.__product = product
        self.__quantity_in_stock = quantity_in_stock

    @property
    def inventory_id(self):
        return self.__inventory_id

    @property
    def product(self):
        return self.__product

    @property
    def quantity_in_stock(self):
        return self.__quantity_in_stock
