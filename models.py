from datetime import datetime
class Transaction:

    def __init__(self, description, date, amount):
        self.description = description
        self.date = date
        self.amount = amount

    @staticmethod
    def from_dict(source):
        if type(source["date"] is str):
            date_format = "%Y-%m-%d"
            datetime_object = datetime.strptime(source["date"], date_format)
            source["date"] = datetime_object.timestamp()
        else:
            source["date"] = datetime.fromtimestamp(source["date"].timestamp())
        transaction = Transaction(source["description"], source["date"], source["amount"])
        return transaction
    
    def to_dict(self):
        dict_transaction = {"description": self.description, "date":self.date, "amount":self.amount}
        return dict_transaction
        

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