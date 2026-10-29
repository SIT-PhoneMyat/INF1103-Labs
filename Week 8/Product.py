class Product:
    def __init__(self, product_id, name, price, stock_quantity):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock_quantity = stock_quantity

    # Methods/Behaviours below
    
    def update_stock(self, new_quantity):
        self.__stock_quantity = new_quantity

    def display_information(self):
        print(f"ID: {self.product_id}")
        print(f"Name: {self.name}")
        print(f"Price: {self.price}")
        print(f"Stock: {self.stock_quantity}")

    # Getters and Setters below

    @property
    def product_id(self):
        return self.__product_id

    @product_id.setter
    def product_id(self, value):
        self.__product_id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        self.__price = value

    @property
    def stock_quantity(self):
        return self.__stock_quantity

    @stock_quantity.setter
    def stock_quantity(self, value):
        self.__stock_quantity = value

    
