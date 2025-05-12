class Transaction:
    def __init__(self, id, description, date, amount):
        self.id = id
        self.description = description
        self.date = date
        self.amount = amount

class User:
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password

class Card:
    def __init__(self, id, name, columns):
        self.id = id
        self.name = name
        self.columns = columns