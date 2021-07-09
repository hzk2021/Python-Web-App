class Entry:
    def __init__(self, entry_id,full_name, nric, phone_no, temperature, date, entry_time, exit_time):
        self.__entry_id = entry_id
        self.__full_name = full_name
        self.__nric = nric
        self.__phone_no = phone_no
        self.__temperature = float(temperature)
        self.__date = date
        self.__entry_time = entry_time
        self.__exit_time = exit_time

# getter/accessor
    def get_entry_id(self):
        return self.__entry_id

    def get_full_name(self):
        return self.__full_name

    def get_nric(self):
        return self.__nric

    def get_phone_no(self):
        return self.__phone_no

    def get_temperature(self):
        return self.__temperature

    def get_date(self):
        return self.__date

    def get_entry_time(self):
        return self.__entry_time

    def get_exit_time(self):
        return self.__exit_time

# setter/mutator
    def set_entry_id(self, entry_id):
        self.__entry_id = entry_id

    def set_full_name(self, full_name):
        self.__full_name = full_name

    def set_nric(self, nric):
        self.__nric = nric

    def set_phone_no(self, phone_no):
        self.__phone_no = phone_no

    def set_temperature(self, temperature):
        self.__temperature = temperature

    def set_date(self, date):
        self.__date = date

    def set_entry_time(self, entry_time):
        self.__entry_time = entry_time

    def set_exit_time(self, exit_time):
        self.__exit_time = exit_time

    def __str__(self):
        s = str(("Entry ID: " + str(self.get_entry_id()),
             "Full Name: " + str(self.get_full_name()),
             "Phone Number: " + str(self.get_phone_no()),
             "Temperature: " + str(self.get_temperature()),
             "Entry Date: " + str(self.get_date()),
             "Entry Time: " + str(self.get_entry_time()),
             "Exit Time: " + str(self.get_exit_time()) + "."))

        return s
