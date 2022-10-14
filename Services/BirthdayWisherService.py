from ServiceReference.BirthdayWisherClass import BirthdayWisher

bday_wisher = BirthdayWisher()


def send_birthday_wishes():
    try:
        bday_wisher.birthday_wisher()
    except Exception as error:
        print(str(error))
        pass


if __name__ == '__main__':
    send_birthday_wishes()
