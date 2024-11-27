class Dog:
    def __init__(self, name, gender, size, weight, birth_date, adopted=False):
        self.name = name
        self.gender = gender
        self.size = size
        self.weight = weight
        self.birth_date = birth_date
        self.adopted = adopted

    def to_dict(self):
        return {
            'name': self.name,
            'gender': self.gender,
            'size': self.size,
            'weight': self.weight,
            'birth_date': self.birth_date,
            'adopted': self.adopted,
        }
