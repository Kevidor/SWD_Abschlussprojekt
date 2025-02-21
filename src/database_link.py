from typing import Self
from datetime import datetime
from queries import Query
from serializable import Serializable
from database import DatabaseConnector

class Link(Serializable):
    
    db_connector = DatabaseConnector().get_table("Link")
    
    def __init__(self, index : str, joint1 : int, joint2 : int, Linestyle : str, Line_color : str):
        super().__init__(index,joint1, joint2, Linestyle,Line_color)
        
    @classmethod
    def instantiate_from_dict(cls, data: dict) -> Self:
        return cls(data['index'], data['joint1'], data['joint1'], data['Linestyle'], data['Line_color'])

    def get_index(self) -> str:
        return F"{self.index}"
    
    def store_data(self):
        print("Storing data...")

        query = Query()
        # upsert: https://tinydb.readthedocs.io/en/latest/usage.html#upserting-data
        result = self.db_connector.upsert(self.__to_dict(), query.index == self.index)
        if result:
            print("Data updated.")
        else:
            print("Data inserted.")

    
    def delete(self):
        print("Deleting data...")
        query = Query()
        if self.db_connector.remove(query.index == self.index): # Joint id muss hier rein
            print("Data deleted.")
        else:
            print("Data not found.")
    
    @classmethod
    def find_by_attribute(cls, by_attribute: str, attribute_value: str, num_to_return=1) -> Self | list[Self]:
        # Load data from the database and create an instance of the Joint class
        Linkquery= Query()
        result = cls.db_connector.search(Linkquery[by_attribute] == attribute_value)

        if result:
            if num_to_return == -1:
                num_to_return = len(result)

            data = result[:num_to_return]
            link_results = [cls.instantiate_from_dict(d) for d in data]
            return link_results if num_to_return > 1 else link_results[0]
        else:
            return None
 
    @classmethod
    def find_all(cls) -> list[Self]:
        # Load all data from the database and create instances of the Joint Class
        Links = []
        for Link_data in cls.db_connector.all():
            Links.append(cls.instantiate_from_dict(Link_data))
        return Links

    # String representation of the class
    def __repr__(self):
        return self.__str__()
    
    #Do not modify this function unless you really know what you are doing!
    def __to_dict(self, *args):
        """
        This function converts an object recursively into a dict.
        It is not necessary to understand how this function works!
        For the sake of simplicity it doesn't handle class attributes and callable objects like (callback) functions as attributes well
        """

        #If no object is passed to the function convert the object itself
        if len(args) > 0:
            obj = args[0] #ignore all other objects but the first one
        else:
            obj = self

        if isinstance(obj, dict):
            #If the object is a dict try converting all its values into dicts also
            data = {}
            for (k, v) in obj.items():
                data[k] = self.__to_dict(v)
            return data
        elif hasattr(obj, "__iter__") and not isinstance(obj, str):
            #If the object is iterable (lists, etc.) try converting all its values into dicts
            #Strings are also iterable, but theses should not be converted
            data = [self.__to_dict(v) for v in obj]
            return data
        elif hasattr(obj, "__dict__"):
            #If its an object that has a __dict__ attribute this can be used
            data = []
            for k, v in obj.__dict__.items():
                #Iterate through all items of the __dict__ and and try converting each value to a dict
                #The resulting key value pairs are stored as tuples in a list that is then converted to a final dict
                data.append((k, self.__to_dict(v)))
            return dict(data)
        else:
            return obj