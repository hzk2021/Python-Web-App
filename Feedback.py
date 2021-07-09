class Feedback:
    count_id = 0

    def __init__(self, name, phone, email, enquiry, service, status):
        Feedback.count_id += 1
        self.__feedback_id = Feedback.count_id
        self.__name = name
        self.__phone = phone
        self.__email = email
        self.__enquiry = enquiry
        self.__service = service
        self.__status = status

    def get_feedback_id(self):
        return self.__feedback_id

    def get_status(self):
        return self.__status

    def get_name(self):
        return self.__name

    def get_service(self):
        return self.__service

    def get_phone(self):
        return self.__phone

    def get_email(self):
        return self.__email

    def get_enquiry(self):
        return self.__enquiry

    def set_feedback_id(self, feedback_id):
        self.__feedback_id = feedback_id

    def set_service(self, service):
        self.__service = service

    def set_name(self, name):
        self.__name = name

    def set_phone(self, phone):
        self.__phone = phone

    def set_email(self, email):
        self.__email = email

    def set_enquiry(self, enquiry):
        self.__enquiry = enquiry

    def set_status(self, status):
        self.__status = status
