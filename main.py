from collections import UserDict
import re

class PhoneValidationError(Exception):
     def __init__(self, message="Phone should contain 10 numbers."):
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

    def verify_phone(self,phone_number):
        pattern = r"^[0-9]{10}$"
        if re.match(pattern,phone_number) is None:
             raise PhoneValidationError()

    
              

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self,phone_number):
         
         try:
              Phone.verify_phone(self,phone_number)
              self.phones.append(Phone(phone_number))
         except PhoneValidationError as e:
              print (f"Error: {e}. Please try again.")

    def find_phone(self,phone:str)->Phone:
        for p in self.phones:
             if p.value == phone:
                  return p
             
    def edit_phone(self,old_phone:str,new_phone:str)->None:
        
        for index, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[index] = Phone(new_phone)

    def remove_phone(self,phone:str)->None:
         
        found_phone = self.find_phone(phone)

        if found_phone:
            self.phones.remove(found_phone)
    
    

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    
    def add_record(self,record:Record):
         self.data[record.name.value] = record
    
    def find(self,name:str)->Record:
         return self.data.get(name,None)

    def delete(self,name:str)->None:
        if name in self.data.keys():
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
