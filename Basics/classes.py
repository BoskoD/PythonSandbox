# A class is like a blueprint for creating objects. An object has properties and methods(functions) associated with it. Almost everything in Python is an object

# Create class
class User:
    # Constructor
    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age

        # Adding Encapsulation of variables... Encapsulation is the concept of making the variables non-accessible or accessible upto some extent from the child classes
        self._private = 1000 # Encapsulated variables are declared with _ in the constructor

    def greeting(self):
        return f'My name is {self.name} and I am {self.age} years old.'

    def has_birthday(self):
        self.age += 1

     #function for encap variable
    def print_encapsulated(self):
        print(self._private)      


# Extend class
class Customer(User):
    # Constructor
    def __init__(self, name, email, age):
        User.__init__(self,name,email,age)
        self.name = name
        self.email = email
        self.age = age
        self.balance = 0

    def set_balance(self, balance):
        self.balance = balance

    def greeting(self):
        return f'My name is {self.name} and I am {self.age} and my balance is {self.balance}'
    
# Init user object
bosko = User('Bosko Danilovic', 'bosko@gmail.com', 32)

# Init customer object
john = Customer('John Doe', 'jd@gmail.com', 35)
john.set_balance(500)
print(john.greeting())

bosko.has_birthday()
print(bosko.greeting())

# Encapsulation
bosko.print_encapsulated()
bosko._private = 800
bosko.print_encapsulated()

# Method inherited from parent 
john.print_encapsulated() # Changing the variable for john does not affect bosko
john._private = 600
john.print_encapsulated()

#Similary changing john's doesn't affect brad's variable.
bosko.print_encapsulated()



