import pickle
import os.path
import os


class MapSaver:

    def __init__(self):
        self.filename = "saved.rgl"

    def save(self, session):
        with open(self.filename, "w") as file:
            pickle.dump(session, file)

    def load(self):
        with open(self.filename, "r") as file:
            result = pickle.load(file)
        return result

    def exist_saved(self):
        return os.path.exists(self.filename)

    def remove_saved(self):
        return os.remove(self.filename)
