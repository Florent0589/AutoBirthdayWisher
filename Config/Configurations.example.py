class Configurations(object):
    __email_config = {
        'smtp_username': 'xxxxxxxxxx@gmail.com',
        'smtp_password': '**********',
        'connection_security': 'SSL/TLS',
        'from_email': 'xxxxxxxxxxx@gmail.com',
        'smtp_server': 'smtp.gmail.com',
        'connection_type': 2,
        'smtp_port': 587,
    }

    # email to send wishes
    __recipient = ''

    __realm_api = 'https://interview-assessment-1.realmdigital.co.za/'

    @property
    def email_config(self):
        return self.__email_config

    @property
    def get_employees_api(self):
        return self.__realm_api + 'employees'

    @property
    def donot_send_config(self):
        return self.__realm_api + 'do-not-send-birthday-wishes'

    @property
    def recipient(self):
        return self.__recipient
