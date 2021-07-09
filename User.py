class User:
    def __init__(self, username, password):
        self.username = username
        self.__password = password

    def get_username(self):
        return self.username

    def get_password(self):
        return self.__password

    def set_username(self, username):
        self.username = username

    def set_password(self, password):
        self.__password = password

class Customer(User):
    def __init__(self, username, password, email, phone_number, points):
        super().__init__(username, password)
        self.username = username
        self.__password = password
        self.email = email
        self.phone_number = phone_number
        self.points = float(points)

    def get_email(self):
        return self.email

    def get_phone_number(self):
        return self.phone_number

    def get_points(self):
        return self.points

    def set_email(self, email):
        self.email = email

    def set_phone_number(self, phone_number):
        self.phone_number = phone_number

    def add_points(self, points):
        self.points += float(points)

    def deduct_points(self, points):
        if float(self.points) > 0:
            self.points -= float(points)

    def __str__(self):
        return "Hi " + self.get_username() + " you currently have " + str(self.get_points()) + " Points"
