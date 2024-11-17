class Book:

    def __init__(self, id, title, author, genre, location, availability, userId):
        self.id = id
        self.title = title
        self.author = author
        self.genre = genre
        self.location = location
        self.availability = availability
        self.userId = userId
    
    @staticmethod
    def from_row(row):
        return Book(row["id"], row["title"], row["author"], row["genre"], row["location"], row["availability"], row["userId"])

    def to_json(self):
        result = {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "location": self.location,
            "availability": self.availability,
            "userId": self.userId
        }
        return result