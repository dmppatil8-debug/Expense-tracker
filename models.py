class Expense:
    def __init__(self, id, amount, category, date, note):
        self.id = id
        self.amount = amount
        self.category = category
        self.date = date
        self.note = note

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "note": self.note
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["amount"],
            data["category"],
            data["date"],
            data["note"]
        )