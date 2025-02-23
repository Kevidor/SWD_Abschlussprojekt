from typing import Self
from serializable import Serializable
from database import DatabaseConnector

class Link_db(Serializable):
    
    db_connector = DatabaseConnector().get_table("Link")
    
    def __init__(self, index : str, joint1 : int, joint2 : int, Linestyle : str, Line_color : str):
        super().__init__(index)
        self.joint1 = joint1 
        self.joint2 = joint2
        self.Linestyle = Linestyle
        self.Line_color = Line_color

        
    @classmethod
    def instantiate_from_dict(cls, data: dict) -> Self:
        return cls(data['index'], data['joint1'], data['joint2'], data['Linestyle'], data['Line_color'])

    def get_index(self) -> str:
        return F"{self.index}"
    
    def __str__(self) -> str:
        return F"index {self.index} link with coordinates {self.joint1},{self.joint2} and with the extra parameter {self.Linestyle},{self.Line_color}"
    