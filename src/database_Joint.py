from typing import Self
from serializable import Serializable
from database import DatabaseConnector

class Joint_db(Serializable):
    
    db_connector = DatabaseConnector().get_table("joint")
    
    def __init__(self,index:str, name : str, x: int, y :int, is_fixed : bool, is_drawn :bool):
        super().__init__(index)
        self.name = name
        self.x = x
        self.y = y
        self.is_fixed = is_fixed
        self.is_drawn = is_drawn
    
    @classmethod
    def instantiate_from_dict(cls, data: dict) -> Self:
        return cls(data['index'], data['name'], data['x'], data['y'], data['is_fixed'], data['is_drawn'])
    
    def get_index(self) -> str:
        return F"{self.index}"
    
    def __str__(self) -> str:
        return F"index {self.index} Joint: {self.name} with coordinates {self.x},{self.y} and with the extra parameter {self.is_fixed}, {self.is_drawn}"
    
    
    


    
        