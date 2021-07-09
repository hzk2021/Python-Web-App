class Order:
    count_id = 0

    def __init__(self, name , item, quantity):
        Order.count_id += 1
        self.__order_id = Order.count_id
        self.__name = name
        self.__item = item
        self.__quantity = quantity

    def get_order_id(self):
        return self.__order_id
    def get_name(self):
        return self.__name
    def get_item(self):
        return self.__item
    def get_quantity(self):
        return self.__quantity

    def set_order_id(self, order_id):
        self.__order_id = order_id
    def set_name(self, name):
        self.__name = name
    def set_item(self, item):
        self.__item = item
    def set_quantity(self, quantity):
        self.__quantity = quantity