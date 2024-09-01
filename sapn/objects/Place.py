class Place:
    def __init__(self, identifier, tokens=0):
        self.identifier = identifier
        self.tokens = tokens

    def add_token(self, n=1):
        self.tokens += n

    def remove_token(self, n=1):
        if self.tokens >= n:
            self.tokens -= n
        else:
            raise ValueError("Not enough tokens")

    def __repr__(self):
        return f"Place({self.identifier}, Tokens: {self.tokens})"