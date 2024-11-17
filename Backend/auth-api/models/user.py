class User:
    def __init__(self, id, firstName, lastName, email, password):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password

    def from_row(row):
        return User(row["id"], row["firstName"], row["lastName"], row["email"], row["password"])

    def to_json(self):
        return {
            "id": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email
        }
