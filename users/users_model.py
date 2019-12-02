class User:
    def __init__(self, first_name,
                 last_name, username,
                 password_digest):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password_digest = password_digest
