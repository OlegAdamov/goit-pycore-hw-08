import pickle
from homework_classes import Record, AddressBook


# Decorator
def input_error(func):
    """ Decorator
    Handles errors from functions and entered commands.
    """
    def inner(*args, **kwargs) -> Exception:
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Please enter only nedeed part for command"
        except KeyError:
            return "Enter user name"
        except IndexError:
            return "Please enter all part in command"
        except FileNotFoundError:
            return {}
        except TypeError as te:
            return te
            
    return inner


@input_error
def add_contact(args: list, book: AddressBook) -> str:
    """
    The function is designed to add a new contact to the book dictionary.
    """
    name, phone, *_ = args
    name = name.lower()
    record = book.find_name_addr_book(name)
    message = 'Contact updated'

    if record is None:

        record = Record(name)
        book.add_record_addr_book(record)
        message = 'Contact added'

    if phone:
        record.add_phone_record(phone)

    return message


@input_error
def add_birthday(args: list, book: AddressBook):
    """
    The function is designed to add a new birthday contact to the contact book.
    """
    name, birthday, *_ = args
    record = book.find_name_addr_book(name.lower())
    message = "Contact updated."

    if record is None:
        return f"The name: {name.capitalize()} is missing"

    record.add_birthday_record(birthday)
    
    return message


@input_error
def add_email(args: list, book: AddressBook):
    """
    The function is designed to add a new birthday contact to the contact book.
    """
    name, email, *_ = args
    record = book.find_name_addr_book(name.lower())
    message = "Contact updated."
    if record is None:
        return f"The name: {name.capitalize()} is missing"
    record.add_email_record(email)
    
    return message


@input_error
def show_birthday(args:list, book: AddressBook):
    """
    The function returns a list of all birthday book from the book dictionary.
    """
    name, *_ = args
    record = book.find_name_addr_book(name.lower())
    if record is None:
        return f"Your name {name.capitalize()} is missing from the book"
    congratulation_name = f"{name.capitalize()}, Birth date: {record.birthday.value}"
    return congratulation_name


@input_error
def birthdays(book):
    """
    The function returns a list of birthday book that will be in next 7 days from the book dictionary.
    """
    birthdays_list = book.get_birthdays_addr_book(book, 7)
    return birthdays_list


@input_error
def change_phone(args: list, book: dict) -> str:
    """
    Save a new phone number for a contact that already exists in the book.
    """
    name, old_phone, new_phone, *_ = args
    record = book.find_name_addr_book(name.lower())
    if record is None:
        return f"Your name {name.capitalize()} is missing from the book"    
    record.edit_phone_record(old_phone, new_phone)
    return "Phone is changed."


# Command parser.
@input_error
def parse_input(user_input: str) -> tuple[str, list]:
    """
    Responsible for parsing user-entered strings,
    extracting keywords and command modifiers from the string.
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def phones_username(args: list, book: dict) -> str:
    """
    Output the phone number for the specified contact to the console.
    """
    name, *_ = args
    record = book.find_name_addr_book(name.lower())
    if record is None:
        return f"Your name {name.capitalize()} is missing from the book"
    find_phone = list(map(lambda phone: phone.value, record.phones))
    phone_name = f"{name.capitalize()}, phones: {find_phone}"
    return phone_name


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Return a new address book if the file is not found.


def return_all_contacts(book: dict) -> str:
    """
    The function returns a list of all contacts from the book dictionary.
    """

    if not book: return f"Your book file is clear"
    all_contacts = ""

    for value in book.values():
        all_contacts += (f"{value}")
    return all_contacts


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def remove_contact(args: list, book: dict):

    name, *_ = args
    name = name.lower()
    record = book.find_name_addr_book(name)

    if record is None:
        return f"Your name {name.capitalize()} is missing from the book"

    book.delete_name_addr_book(name)
    return f"Your contact {name.capitalize()} is deleted from the book"


@input_error
def main():

    book = load_data()

    commands = '''
    1) exit or close - To exit the application
    2) help - To print this menu
    3) add [username] [phone] - To add a new contact
    4) change [username] [old_phone] [new_phone] - To change the phone number your username
    5) all - To print all book
    6) phones [username] - To print phone number your username
    7) add-birthday [username] [birthday] - Add a date of birth for the specified contact.
    8) show-birthday [username] - Show the date of birth for the specified contact.
    9) birthdays - Show birthdays for the next 7 days, along with the dates when greetings should be sent.
    10) add-email [username] [email] - Add an email in contatc
    11) remove-contact [username] - To remove a contact

    '''

    print("CONTACTS BOT\n")
    print("Welcome to the assistant bot!")
    print(commands)

    """
    Request-response loop.
    Responsible for receiving data from the user and
    returning a response to the user from the handler function.
    """
    while True:

        user_input = input("Enter your command (enter 'exit' or 'close' to stop): ").strip().lower()
        command, *args = parse_input(user_input)

        # Command handler functions - Responsible for the direct execution of commands.
        if command in ["close", "exit"]:    # Program execution termination function.
            print('Goodbye!')
            save_data(book)  # Викликати перед виходом з програми
            break

        if command == 'hello':
            print("How can I help you?")

        elif command == 'help':
            print(commands)

        elif command == 'add':
            print(add_contact(args, book))

        elif command == 'change':
            print(change_phone(args, book))

        elif command == 'phones':
            print(phones_username(args, book))

        elif command == 'all':
            print (return_all_contacts(book))

        elif command == 'add-birthday':
            print (add_birthday(args, book))

        elif command == 'add-email':
            print (add_email(args, book))

        elif command == 'show-birthday':
            print (show_birthday(args, book))

        elif command == 'birthdays':
            print (birthdays(book))

        elif command == 'remove-contact':
            print (remove_contact(args, book))

        else:
            print("Invalid command.")
            continue


if __name__ == "__main__":
    main()
