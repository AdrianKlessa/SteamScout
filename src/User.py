class User:
    def __init__(self, id: int, name: str, password_hash: str) -> None:
        self.id = id
        self.name = name
        self.password_hash = password_hash

    def __repr__(self):
        return self.name