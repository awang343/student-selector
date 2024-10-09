import numpy as np 
import pandas as pd 
import scipy as sp

class Class:
    def __init__(self, csv_name):
        self.load_class(csv_name)
        print(self.data)
    
    def load_class(self, csv_name):
        self.data = pd.read_csv(csv_name, index_col="Id")
        self.data["Talk Count"] = 0
        self.update_weights()
    
    def update_weights(self):
        self.data["Weights"] = sp.special.softmax(np.log(1/(self.data["Talk Count"]+0.1))/np.log(1.7))
    
    def choose_random(self):
        id = np.random.choice(self.data.index, p = self.data["Weights"])
        self.data.loc[id, "Talk Count"] += 1
        self.update_weights()
        return self.data.loc[id, "Name"]

    def volunteer(self, *, id=None, name=None):
        if id is None and name is None:
            raise "Provide an id or name"
        print(name)
        self.data.loc[np.logical_or(self.data["Name"] == name, self.data.index == id), "Talk Count"] += 1
        self.update_weights()
    
    def add_person(self, name):
        self.data.loc[len(self.data)] = [name, 0, 0]
        self.update_weights()
    
    def remove_person(self, *, id = None, name = None):
        if not np.any(id == self.data.index) and not np.any(name == self.data["Name"]):
            print(name in self.data["Name"])
            raise "Provide a valid id or name"
        if id is not None and name is not None:
            raise "Specify either id or name"

        self.data = self.data[self.data["Name"] != name]
        self.data = self.data[self.data.index != id]
