from datetime import datetime
class Transaction:
    def __init__(self, tx_id, description, date, amount, category, user_id):
        self.tx_id = tx_id
        self.description = description
        self.date = date
        self.amount = amount
        self.category = category
        self.user_id = user_id

    # this is from a dictionary of values to the item itself. Like an initializer
    # Use Cases: getting data from the firestore to display or send elsewhere
    @classmethod
    def from_dict(cls, source):
        source['date'] = datetime.fromtimestamp(source['date'].timestamp())
        transaction = cls(source['tx_id'], source['description'], source['date'], source['amount'], source['category'], source['user_id'])
        return transaction
    
    # this is from item to dictionary
    # Use Cases: Adding data via request -> object -> dict 
    def to_dict(self):
        dict_transaction = {"description": self.description, "date":self.date, "amount":self.amount, 'category': self.category, 'user_id': self.user_id}
        return dict_transaction
        

class User:
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password


class Card:
    def __init__(self, card_id, name, columns):
        self.card_id = card_id
        self.name = name
        self.columns = columns


class Category:
    def __init__(self, category_id, category_name):
        self.category_id = category_id
        self.category_name = category_name