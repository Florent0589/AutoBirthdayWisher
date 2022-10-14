from ServiceReference.BirthdayWisherClass import BirthdayWisher

wisher = BirthdayWisher()


def test_update_employee(emp_id):
    emp = {
        'id': emp_id
    }
    test = wisher.update_employee(emp)
    if not test:
        print('Failed to update employee')
    else:
        print('Success! update employe')


def test_get_employees(mm_dd):
    test = wisher.get_employees(search_filter={
        'dateOfBirth_like': mm_dd
    })
    if test is None:
        print('Failed to get employees')
    else:
        print('Success! got employees')


def test_send_email(email, subject, message):
    test = wisher.send_mail(email, subject, message)
    if not test:
        print('Failed to send message')
    else:
        print('Success! Message sent')


if __name__ == '__main__':
    test_update_employee(100)
    test_get_employees('02-15')
    test_send_email('', 'Test', 'This is suppose to be a birthday wish, one , two, three')
