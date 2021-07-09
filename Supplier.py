class Supplier:
    count_id = 0
    def __init__(self, name, contact_number, email, address, description):
        Supplier.count_id += 1
        self.__supplier_id = Supplier.count_id
        self.__name = name
        self.__contact_number = contact_number
        self.__email = email
        self.__address = address
        self.__description = description

    def get_supplier_id(self):
        return self.__supplier_id
    def get_name(self):
        return self.__name
    def get_contact_number(self):
        return self.__contact_number
    def get_email(self):
        return self.__email
    def get_address(self):
        return self.__address
    def get_description(self):
        return self.__description

    def set_supplier_id(self, supplier_id):
        self.__supplier_id = supplier_id
    def set_name(self, name):
        self.__name = name
    def set_contact_number(self, contact_number):
        self.__contact_number = contact_number
    def set_email(self, email):
        self.__email = email
    def set_address(self, address):
        self.__address = address
    def set_description(self, description):
        self.__description = description