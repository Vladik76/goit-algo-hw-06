from collections import UserDict
import re

class PhoneValidationError(Exception):
     """
     Custom exception. Phone validation
     """
     def __init__(self, message="Phone should contain 10 numbers."):
        self.message = message
        super().__init__(self.message)

class NotUniquePhoneError(Exception):
    """
    Error when phone is not unique
    """
    def __init__(self, message="The phone number already exists"):
        self.message = message
        super().__init__(self.message)

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
	pass

class Phone(Field):
    def __init__(self, value):
        if not self.verify_phone(value):
            raise PhoneValidationError()
        super().__init__(value)

    def verify_phone(self,phone_number)->bool:
        pattern = r"^[0-9]{10}$"
        return re.match(pattern,phone_number) is not None

  
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def find_phone(self,phone_number:str)->Phone:

        for p in self.phones:
            if p.value == phone_number:
                return p
    
    def check_duplicate(self,phone_number:str)->Phone:
        """
        Checks if passed phone number already in list of Phones
        Returns Phone if phone_number does not exists otherwise raise exception NotUniquePhoneError
        """
        phone=Phone(phone_number)

        if phone in self.phones:
            raise NotUniquePhoneError
        else:
            return phone

    def add_phone(self,phone_number:str)->str:
        """
        Add phone

        Function raises: 
        PhoneValidationError exception if new phone number is incorrect
        NotUniquePhoneError exception if new phone already in list of phones
        """
        self.phones.append(self.check_duplicate(phone_number)) # append to phones list if correct. Oterwise, raise an Exception

    def edit_phone(self,old_phone_number:str,new_phone_number:str)->None:
        """
        Edit phone

        Function raises: 
        ValueError exception if phone is not in list
        PhoneValidationError exception if new phone number is incorrect
        NotUniquePhoneError exception if new phone already in list of phones
        """
        self.phones[self.phones.index(self.find_phone(old_phone_number))] = self.check_duplicate(new_phone_number)

    def remove_phone(self,phone_number:str)->None:
        """
        Remove phone from the list of phones

        Function raises: 
        ValueError exception if phone is not in list
        PhoneValidationError exception if new phone number is incorrect
        """
        self.phones.remove(self.find_phone(phone_number))
    

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    
    def add_record(self,record:Record)->None:
        """
        Add Record to Address book
        Raises ValueError exception if record already exists.
        """
        if record.name.value not in self.data.keys():
            self.data[record.name.value] = record
        else:
            raise ValueError(f"The Record {record.name} already exists.")
        
    
    def find(self,name:str)->Record:
         return self.data.get(name,None)

    def delete(self,name:str)->None:
        """
        Raises KeyError if record does not exist
        """
        del self.data[name]




#TESTS

book = AddressBook()

john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

book.add_record(john_record)

jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

for name, record in book.data.items():
     print(record)

john = book.find("John")
print(john)
john.edit_phone("1234567890", "1112223333")
print(john)
john.remove_phone("1112223333")
print(john)

found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

book.delete("Jane")


for name, record in book.data.items():
     print(record)
