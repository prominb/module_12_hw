from collections import UserDict
from datetime import datetime
# import json
import pickle


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

    def save_to_file(self, filename='book.bin'):
        with open(filename, "wb") as fh:
            pickle.dump(self.data, fh)

    def read_from_file(self, filename='book.bin'):
        try:
            with open(filename, "rb") as fh:
                self.data = pickle.load(fh)
        except FileNotFoundError:
            print('File Not Found. Creating new book...')
    def search(self, request):
        result = []
        for record in self.data.values():
            for phone in record.phones:
                if request in phone.value:
                    result.append(record.__str__())
                    break
        return result


def main():

    def good_bye():
        print("Good bye!")

    # Створення нової адресної книги
    book = AddressBook()

    # try:
    book.read_from_file('book.bin')
    # except FileNotFoundError:
        # print('File Not Found.')  # Creating new book...')

    try:
        while True:
            
            print(
                '\n=== MAIN MENU ===\n' \
                '1. Add Record\n' \
                '2. Search Record\n' \
                '3. Change Record\n' \
                '4. Show all records\n' \
                '5. Save to file and Exit'
            )

            input_command = input('Choose number: ')
            if input_command == '5':
                book.save_to_file('book.bin')
                break
            elif input_command == "1":
                input_name = input('Enter name: ')
                # Створення запису для John
                # john_record = Record("John")
                record_name = Record(input_name)
                input_phone = input('Enter Phone number: ')
                # john_record.add_phone("1234567890")
                record_name.add_phone(input_phone)
                add_another_phone_status = True
                while add_another_phone_status:
                    check_status = input('Add another phone? Y/n: ')
                    if check_status.lower() == 'y':
                        input_phone = input('Enter Phone number: ')
                        # john_record.add_phone("5555555555")
                        record_name.add_phone(input_phone)
                    elif check_status.lower() == 'n':
                        add_another_phone_status = False
                # Додавання запису John до адресної книги
                book.add_record(record_name)
            elif input_command == "2":
                print('Searching...')
                request = input('Enter numbers: ')
                # book.search(request)
                result = book.search(request)
                print(result)
            elif input_command == "3":
                print('Changing...')
            # elif input_command.lower() == "show all":
            #     print(show_all_handler(contact_book))
            elif input_command == "4":
                # Виведення всіх записів у книзі
                for name, record in book.data.items():
                    print(record)
            else:
                print('=> Invalid command! <=')
    except KeyboardInterrupt:
        print("\nAbort the mission")
    finally:
        good_bye()

    # print(book.data)
    # Виведення всіх записів у книзі
    # for name, record in book.data.items():
    #     print(record)


if __name__ == '__main__':
    main()
