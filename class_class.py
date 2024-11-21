import pandas as pd
import numpy as np
from scipy import special

class Class:
    def __init__(self, csv_name):
        self.load_class(csv_name)

    def load_class(self, csv_name):
        self.data = pd.read_csv(csv_name, index_col="Id")
        self.data["Talk Count"] = 0
        self.update_weights()

    def update_weights(self):
        self.data["Weights"] = special.softmax(
            np.log(1 / (self.data["Talk Count"] + 0.1)) / np.log(1.7)
        )

    def choose_random(self):
        id = np.random.choice(self.data.index, p=self.data["Weights"])
        selected_student = self.data.loc[id, "Name"]
        self.data.loc[id, "Talk Count"] += 1
        self.update_weights()
        return selected_student

    def volunteer(self, *, id=None, name=None):
        if id is None and name is None:
            raise ValueError("Provide an id or name")
        if id is not None:
            self.data.loc[id, "Talk Count"] += 1
        else:
            idx = self.data[self.data["Name"] == name].index
            self.data.loc[idx, "Talk Count"] += 1
        self.update_weights()

    def add_person(self, name):
        new_id = self.data.index.max() + 1
        self.data.loc[new_id] = [name, 0, 0]
        self.update_weights()

    def remove_person(self, *, id=None, name=None):
        if id is not None:
            if id in self.data.index:
                self.data = self.data.drop(id)
            else:
                raise ValueError("Invalid ID provided.")
        elif name is not None:
            idx = self.data[self.data["Name"] == name].index
            if not idx.empty:
                self.data = self.data.drop(idx)
            else:
                raise ValueError("Invalid name provided.")
        else:
            raise ValueError("Provide a valid id or name")
        self.update_weights()
