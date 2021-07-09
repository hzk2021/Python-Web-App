class Product:
    count_id = 0
    def __init__(self,image,name,stock,price,specs):
        Product.count_id+=1
        self.__product_id = Product.count_id
        self.__image=image
        self.__name=name
        self.__stock=stock
        self.__price=price
        self.__specs=specs
    def get_product_id(self):
        return self.__product_id

    def get_image(self):
        return self.__image
    def get_name(self):
        return self.__name
    def get_stock(self):
        return self.__stock
    def get_price(self):
        return self.__price
    def get_specs(self):
        return self.__specs
    def set_user_id(self, product_id):
        self.__product_id = product_id
    def set_image(self, image):
        self.__image = image

    def set_name(self, name):
        self.__name = name
    def set_stock(self, stock):
        self.__stock = stock
    def set_price(self,price):
        self.__price = price
    def set_specs(self, specs):
        self.__specs = specs

