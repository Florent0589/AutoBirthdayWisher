import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from Config.Configurations import Configurations
import requests
import calendar


class BirthdayWisher:

    config = Configurations()
    today = datetime.datetime.now().strftime("%m-%d")
    year_now = int(datetime.datetime.now().strftime("%Y"))

    def get_employees(self, search_filter=None):
        """
        Get all employees based on filters from endpoint
        :param search_filter:
        :return:
        """
        try:
            r = requests.get(self.config.get_employees_api)
            if search_filter is not None:
                r = requests.get(self.config.get_employees_api, params=search_filter)
            employees = r.json()
            return employees
        except requests.RequestException as err:
            print(str(err))
        return None

    def get_birthday_users(self):
        """
        Get employees for current day
        :return: dict
        """
        bday_users = list()
        employees = list()
        if calendar.isleap(self.year_now):
            params = {'dateOfBirth_like': self.today}
            employees = self.get_employees(params)
        else:
            params = {'dateOfBirth_like': self.today}
            leap_employees = None
            normal_employees = self.get_employees(params)
            if self.today == '02-28':
                self.today = '02-29'
                params = {'dateOfBirth_like': self.today}
                leap_employees = self.get_employees(params)

            if leap_employees is not None and normal_employees is not None:
                employees = normal_employees + leap_employees
            elif leap_employees is None and normal_employees is not None:
                employees = normal_employees
            elif leap_employees is not None and normal_employees is None:
                employees = leap_employees

        if employees is not None and len(employees) != 0:
            for employee in employees:
                can_send_wishes = self.can_send_employee(employee)
                if can_send_wishes:
                    bday_users.append(employee)

        return bday_users

    def send_mail(self, to_address: str, subject: str, message: str):
        """
        Send message to employee
        :param to_address str
        :param subject str
        :param message str
        :return: bool
        """

        try:
            email_config = self.config.email_config
            print(message)
            email_message = MIMEMultipart()

            email_message['From'] = email_config['from_email']
            email_message['To'] = to_address
            email_message['Subject'] = subject
            email_message.attach(MIMEText(message, 'html'))
            server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(email_config['smtp_username'], email_config['smtp_password'])
            server.sendmail(email_message['From'], to_address, email_message.as_string())
            server.quit()
            return True
        except Exception as error:
            print((str(error)))
            return False

    def birthday_wisher(self):

        """
        Main service method
        :return:
        """

        employees = self.get_birthday_users()
        if len(employees) == 0:
            return False

        try:
            for emp in employees:
                email_address = self.config.recipient
                full_names = " ".join((emp['name'], emp['lastname']))
                subject = 'Birthday Wishes'
                msg = f'Happy Birthday {full_names}, we wishes you all the best on your special day'
                sent = self.send_mail(email_address, subject=subject, message=msg)
                if sent:
                    notification_date = datetime.datetime.now()
                    notification_date = notification_date.strftime("%y-%m-%d")
                    params = dict(
                        lastNotification=notification_date,
                        lastBirthdayNotified=notification_date
                    )
                    self.update_employee(emp['id'], params)
            return True
        except Exception as err:
            print(str(err))

    def can_send_employee(self, emp: dict):

        """
        Check where employee is working or not working with company, check if configured not to send birthday wishes
        :param emp:
        :return bool:
        """

        try:
            if emp['employmentStartDate'] is None:
                return False
            if emp['employmentEndDate'] is not None:
                return False

            r = requests.get(self.config.donot_send_config)
            dont_employees = r.json()
            emp_id = emp['id']
            if len(dont_employees) != 0:
                if emp_id in dont_employees:
                    return False
            return True
        except Exception as error:
            print((str(error)))
            return False

    def update_employee(self, emp_id: int, params):

        """
        Update employee after sending message
        :param emp_id:
        :param params:
        :return bool:
        """
        try:
            emp_id = str(emp_id)
            r = requests.patch(self.config.get_employees_api + '/' + emp_id, json=params)
            updated_employee = r.json()
            if len(updated_employee) != 0:
                return True
            return False
        except requests.RequestException as error:
            print(str(error))
            return False
