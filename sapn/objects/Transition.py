class Transition:
    def __init__(self, identifier, input_places=None, output_places=None):
        self.identifier = identifier
        self.input_places = input_places if input_places else []
        self.output_places = output_places if output_places else []

    def is_enabled(self):
        return all(place.tokens > 0 for place in self.input_places)

    def fire(self):
        if self.is_enabled():
            for place in self.input_places:
                place.remove_token()
            for place in self.output_places:
                place.add_token()
        else:
            raise ValueError("Transition is not enabled")

    def __repr__(self):
        return f"Transition({self.identifier})"