class Session:
    def __init__(self, id, userId, ttl):
        self.id = id
        self.userId = userId
        self.ttl = ttl

    def from_row(row):
        return Session(row["id"], row["userId"], row["ttl"])
    
    def to_json(self):
        return {
            "id": self.id,
            "userId": self.userId,
            "ttl": self.ttl
        }