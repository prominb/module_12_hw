from collections import UserDict
from datetime import datetime
import json


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    # Перевірка на коректність веденого номера телефону setter для value класу Phone.
    def check_phone(self):
        if len(self._value) != 10 or not self._value.isdecimal():  # Реалізовано валідацію номера телефону (має бути 10 цифр).
            raise ValueError("Phone must contain 10 digits only!")
    
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value
        self.check_phone()


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    # ValueError: time data '44.2.2014' does not match format '%d.%m.%Y'
    def set_birthday(self, new_value):
        if new_value:
            self._value = datetime.strptime(new_value, "%d.%m.%Y")

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value):
        self._value = new_value
        self.set_birthday(self._value)


class Record:
    '''Record: Додавання телефонів. Видалення телефонів. Редагування телефонів. Пошук телефону.
    Клас Record приймає ще один додатковий (опціональний) аргумент класу Birthday'''
    def __init__(self, name, birthday = None):
        self.name = Name(name)  # Реалізовано зберігання об'єкта Name в окремому атрибуті.
        self.phones = []  # Реалізовано зберігання списку об'єктів Phone в окремому атрибуті.
        self.birthday = Birthday(birthday)  # опціональний аргумент класу Birthday

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p._value for p in self.phones)}"

    # Реалізовано методи для:
    def add_phone(self, phone: str):  # додавання - add_phone
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):  # видалення - remove_phone
        for i in range(len(self.phones)):
            if str(self.phones[i]) == phone:
                return self.phones.pop(i)

    def edit_phone(self, phone: str, new_phone: str):  # редагування - edit_phone
        is_exists = self.find_phone(phone)
        if is_exists:
            get_index = self.phones.index(is_exists)
            self.phones[get_index] = Phone(new_phone)
        else:
            raise ValueError(f'Phone {phone} not found!')

    def find_phone(self, phone: str):  # пошуку об'єктів Phone - find_phone
        for item in filter(lambda i: i.__str__() == phone, self.phones):
            return item
    
    def days_to_birthday(self):  # повертає кількість днів до наступного дня народження.
        if not self.birthday.value:
            return 'Field "Birthday" is Empty!'
        else:
            today = datetime.now().date()
            test1 = self.birthday.value
            test1.strptime
            test1 = test1.replace(year=today.year)
            test1 = test1.date()
            if test1 > today:
                result = test1 - today
                return f'Next Bday = {result.days}'
            else:
                result = test1.replace(year=today.year + 1) - today
                return f'Next Bday = {result.days}. It was {(test1 - today).days} days ago.'


class AddressBook(UserDict):
    '''AddressBook: Додавання записів. Пошук записів за іменем. Видалення записів за іменем.'''
    """Записи Record у AddressBook зберігаються як значення у словнику. В якості ключів використовується значення Record.name.value."""
    # Реалізовано метод add_record, який додає запис до self.data.
    def add_record(self, record: Record):  # Додавання запису.
        self.data[record.name.value] = record

    def find(self, name):  # Реалізовано метод find, який знаходить запис за ім'ям.
        return self.data.get(name)

    def delete(self, name):  # Реалізовано метод delete, який видаляє запис за ім'ям.
        if name in self.data:
            return f'Record with {self.data.pop(name)} was removed!'
    
    def iterator(self, records_number):  # повертає генератор за записами AddressBook (за одну ітерацію повертає N записів).
        counter = 0
        convert_list = list(self.data.items())
        while counter < len(convert_list):
            convert_dict = dict(convert_list[counter : counter + records_number])
            for key, value in convert_dict.items():
                yield value
                counter += records_number - 1


contact_book = {}

def input_error(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except ValueError:
            return "The phone contains a letters!"
        except IndexError:
            return "Invalid command! Enter user name."
        except KeyError:
            return "Name doesn\'t exists."
    return inner

def hello_handler():
    print("How can I help you?")

@input_error
def add_handler(input_command_lower_case):
    input_command_list = input_command_lower_case.split()
    name, phone = input_command_list[1], input_command_list[2]
    if name.title() in contact_book.keys():
        return f'Name {name.title()} already exists.' \
                'Please use "change" command.'
    elif phone in contact_book.values():
        return f'Phone {phone} already exists. Please use "change" command.'
    else:
        title_name = name.title()
        phone = phone.removeprefix('+')
        if phone.isdecimal():
            contact_book[title_name] = phone
        else:
            print(int(phone))
    return 'Contact added!'

@input_error
def change_handler(input_command_lower_case):
    input_command_list = input_command_lower_case.split()
    name, phone = input_command_list[1], input_command_list[2]
    if name.title() not in contact_book.keys():
        return f'Name {name.title()} doesn\'t exists.' \
                'Please use "add" command.'
    elif phone in contact_book.values():
        return f'Phone {phone} already exists.' \
                'Please use "show all" to see all contacts.'
    else:
        title_name = name.title()
        phone = phone.removeprefix('+')
        if phone.isdecimal():
            contact_book[title_name] = phone
        else:
            print(int(phone))
    return 'Contact changed!'

@input_error
def phone_handler(input_command_lower_case):
    input_command_list = input_command_lower_case.split()
    name = input_command_list[1].capitalize()
    return contact_book.get(name, f'Name {name} doesn\'t exists.')

@input_error
def show_all_handler(contact_book):
    if len(contact_book) == 0:
        print(contact_book.pop('test'))
    else:
        for key, value in contact_book.items():
            print(f"Name: {key:<15} Phone: {value}")
        return contact_book

def good_bye():
    print("Good bye!")

def main():
    try:
        while True:
            input_command = input('Enter your command: ')
            input_cmd_lower_case = input_command.lower()
            if input_cmd_lower_case in ("good bye", "close", "exit"):
                break
            elif input_cmd_lower_case == "hello":
                hello_handler()
            elif input_cmd_lower_case[:3] == "add":
                print(add_handler(input_cmd_lower_case))
            elif input_cmd_lower_case[:6] == "change":
                print(change_handler(input_cmd_lower_case))
            elif input_cmd_lower_case[:5] == "phone":
                print(phone_handler(input_cmd_lower_case))
            elif input_command.lower() == "show all":
                print(show_all_handler(contact_book))
            else:
                print('=> Invalid command! <=')
            # print(contact_book)
    except KeyboardInterrupt:
        print("\nAbort the mission")
    finally:
        good_bye()
    # # Створення нової адресної книги
    # book = AddressBook()



# if __name__ == '__main__':
#     main()


# # Створення запису для John
# john_record = Record("John")
# # john_record = Record("John", "27/02/2024")
# # john_record = Record("John", "27/02/2014")
# # john_record = Record("John", "3.2.2014")  # WORK
# # john_record = Record("John", "27.1.2014")  # WORK
# # john_record = Record("John", "27.21.2014")  # WORK
# john_record.add_phone("1234567890")
# john_record.add_phone("5555555555")
# # john_record.add_phone("555555")  # WORK
# # john_record.add_phone("555qq5555")  # WORK

# # print(john_record.birthday, type(john_record.birthday), repr(john_record.birthday))
# # john_record.birthday
# # print(john_record.days_to_birthday())
# # john_record.days_to_birthday()

# # Додавання запису John до адресної книги
# book.add_record(john_record)

# # Створення та додавання нового запису для Jane
# jane_record = Record("Jane")
# jane_record.add_phone("9876543210")
# book.add_record(jane_record)

# # # Виведення всіх записів у книзі
# # for name, record in book.data.items():
# #     print(record)

# # # Знаходження та редагування телефону для John
# # john = book.find("John")
# # john.edit_phone("1234567890", "1112223333")

# # print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# # # Пошук конкретного телефону у записі John
# # found_phone = john.find_phone("5555555555")
# # print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# # # Видалення запису Jane
# # book.delete("Jane")


# # Виведення всіх записів у книзі
# # for name, record in book.data.items():
# #     print(record)


# test1_record = Record("Test1")
# test1_record.add_phone("1111111111")
# book.add_record(test1_record)

# test2_record = Record("Test2")
# test2_record.add_phone("2222222222")
# book.add_record(test2_record)

# test3_record = Record("Test3")
# test3_record.add_phone("3333333333")
# book.add_record(test3_record)

# test4_record = Record("Test4")
# test4_record.add_phone("4444444444")
# book.add_record(test4_record)

# test5_record = Record("Test5")
# test5_record.add_phone("5555555555")
# book.add_record(test5_record)

# test6_record = Record("Test6")
# test6_record.add_phone("6666666666")
# book.add_record(test6_record)

# # Виведення N записів у книзі
# records_generator = book.iterator(5)
# for i in records_generator:
#     print(i)
