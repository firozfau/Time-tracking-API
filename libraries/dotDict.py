class DotDict(dict):
    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(f"'DotDict' object has no attribute '{item}'")

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, item):
        try:
            del self[item]
        except KeyError:
            raise AttributeError(f"'DotDict' object has no attribute '{item}'")


    def convert_to_dotdict(self,data):
        if isinstance(data, dict):
            return DotDict({key: self.convert_to_dotdict(value) for key, value in data.items()})
        else:
            return data
