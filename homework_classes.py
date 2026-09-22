# Система для управління адресною книгою.
from collections import UserDict
from datetime import datetime, date, timedelta
import re


class Field:
    """
    Base class for record fields.
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)  # Повернення строки value


class Birthday(Field):
    """
    A class for storing the birthday. Mandatory field.
    """
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError as ve:
            raise ValueError("Invalid date format. Use DD.MM.YYYY") from ve
        super().__init__(value)


class Email(Field):
    """
    A class for storing a phone number. It includes format validation (10 digits).
    """
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Invalid email format! Use something like: name@example.com")
        super().__init__(value)

    @staticmethod
    def validate(email):
        # Check is valid email
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(regex, email)


class Name(Field):
    """
    A class for storing the contact name. Mandatory field.
    """
    pass


class Phone(Field):
    """
    A class for storing a phone number. It includes format validation (10 digits).
    """
    def __init__(self, value):
        if len(value) == 10 and int(value):
            super().__init__(value)
        else:
            raise ValueError("Phone must be a string of 10 digits.")


class Record:
    """
    A class for storing contact information, including the name and a list of phones.
    """
    def __init__(self, name: str):

        self.name = Name(name.lower())
        self.phones = []
        self.birthday = None
        self.emails = []

    def add_phone_record(self, phone: str) -> None:
        """
        Method for adding phone.
        """
        is_valid_phone = Phone(phone)
        self.phones.append(is_valid_phone)

    def add_email_record(self, email: str) -> None:
        """
        Method for adding phone.
        """
        is_valid_email = Email(email)
        self.emails.append(is_valid_email)

    def add_birthday_record(self, birthday):
        """
        Method for adding Birthday.
        """
        self.birthday = Birthday(birthday)
        
    def edit_phone_record(self, old_phone: str, new_phone: str) -> None:
        """
        Method for editing phone.
        """
        is_valid_phone = Phone(new_phone)
        found_old_phone = self.find_phone_record(old_phone)

        if found_old_phone:
            found_old_phone.value = is_valid_phone.value
        else:
            raise ValueError(f"Phone number {old_phone} was not found for editing.")

    def find_phone_record(self, phone: str) -> str:
        """
        Phone search method.
        """
        for found_phone in self.phones:
            if found_phone.value == phone:
                return found_phone

        return None

    def remove_email_record(self):
        """
        Method for removing all emails.
        """
        self.emails = []

    def remove_birthday_record(self):
        """
        Method for removing birthday.
        """
        self.birthday = None

    def remove_phone_record(self, phone: str) -> None:
        """
        Method for removing phone.
        """
        phone_to_remove = self.find_phone_record(phone)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError(f"Phone number {phone} was not found in this record.")

    def __str__(self) -> str:
        phones_str = ', '.join(p.value for p in self.phones)
        birthday_str = self.birthday.value if self.birthday else 'Birthday is missing'
        emails_str = ', '.join(e.value for e in self.emails)

        return (f"\nContact name: {self.name.value.capitalize()}\n"
                f"Phones: {phones_str if phones_str else 'Phones is missing'}\n"
                f"Birthday: {birthday_str}\n"
                f"Emails: {emails_str if emails_str else 'Emails is missing'}\n")


class AddressBook(UserDict):
    """
    A class for storing and managing records.
    """
    def add_record_addr_book(self, value: Record) -> None:
        """
        Method for adding record.
        """
        self.data[value.name.value] = value

    def get_string_to_date_addr_book(self, date_string):
        """
        Let's convert the date from a string to datetime format.
        """
        return datetime.strptime(date_string, "%d.%m.%Y").date()

    def get_date_to_string_addr_book(self, date_datetime):
        """
        Let's convert the date from datetime to string format.
        """
        return date_datetime.strftime("%d.%m.%Y")

    def find_next_weekday_addr_book(self, start_date, weekday):
        """
        Find the next date for a given day of the week (birthday), starting from the initial date (0).
        """
        # Calculate the difference in days between the target day of the week (0) and the day of the week of the start date (birthday).
        days_ahead = weekday - start_date.weekday()
        # If the target day has already passed this week or is today...
        if days_ahead <= 0:
            # ... add 7 days to move the search to the following week
            days_ahead += 7
        # Return a new date by adding the found number of days to the initial date.
        return start_date + timedelta(days=days_ahead)

    def adjust_for_weekend_addr_book(self, birthday):
        if birthday.weekday() >= 5:
            return self.find_next_weekday_addr_book(birthday, 0)
        return birthday

    def get_birthdays_addr_book(self, book, days=7):
        birthdays = [] # [{"name": "Contact name", "birthday": 'DD.MM.YYYY'}] 
        # today = self.string_to_date('22.04.2024') # date.today()
        today = date.today()
        for name in book:

            user_birthday = self.find_name_addr_book(name.lower())
            try:
                user_birthday = user_birthday.birthday.value
            except AttributeError:
                continue
            user_birthday = self.get_string_to_date_addr_book(user_birthday)
            birthday_this_year = user_birthday.replace(year=today.year)
            """
            At this point, add a check to see if the birthday falls in the following year.
            """
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=birthday_this_year.year + 1)

            if 0 <= (birthday_this_year - today).days <= days:
                """ 
                Add the postponement of the greeting date to the next working day,
                if the birthday falls on a weekend.
                """
                congratulation_date_str = self.get_date_to_string_addr_book(self.adjust_for_weekend_addr_book(birthday_this_year))
                birthdays.append({name.capitalize(): congratulation_date_str})
        return birthdays

    def find_name_addr_book(self, name: str) -> Record:
        """
        Method for searching record by name.
        """

        return self.data.get(name.lower(), None)

    def delete_name_addr_book(self, name: str) -> None:
        """
        Deleting record by name.
        """
        name = name.lower()
        if name.lower() in self.data:
            del self.data[name]

    def __str__(self) -> str:
        """
        For printing our book
        """
        text = 'Contact in AddressBook:'
        new_values = self.data.values()

        for new_value in new_values:
            text += f" \n{new_value}"
        return text

    # def __repr__(self):
        # print(f"Repr self-str: {str(self)}")
        # return str(self)

def main():
    """
    The main menu for start script
    """
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone_record("1234567890")
    john_record.add_phone_record("5555555555")
    john_record.add_birthday_record('25.09.1970')
    # print(john_record.birthday, type(john_record.birthday))
    # print(john_record.birthday.value, type(john_record.birthday.value))

    # Додавання запису John до адресної книги
    book.add_record_addr_book(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone_record("9876543210")

    # Додавання запису Jane до адресної книги
    book.add_record_addr_book(jane_record)

    # Виведення всіх записів у книзі
    print(book)

    # Знаходження та редагування телефону для John
    john = book.find_name_addr_book("John")
    john.edit_phone_record("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone_record("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

    # Пошук днів народження в наступні 7 днів
    birthdays = book.get_birthdays_addr_book(book)
    print('Birthdays: ', birthdays, type(birthdays))

    # Видалення запису Jane
    book.delete_name_addr_book("Jane")

    # Виведення всіх записів у книзі
    print(book)


if __name__ == '__main__':
    main()
