from typing import Self
from serializable import Serializable
from database import DatabaseConnector
from mechanism_components import Link,Rotor,Joint
import pandas as pd

class Project_db(Serializable):
    
    db_connector = DatabaseConnector().get_table("Project")
    
    def __init__(self, index : str):
        super().__init__(index)        
        self.joint = Joint.joints
        self.link = Link.links
        self.rotor = Rotor.rotors
        
    @classmethod
    def instantiate_from_dict(cls, data: dict) -> Self:
        return cls(data['name'], data['joint'], data['link'], data['rotor'])

    def get_index(self) -> str:
        return F"{self.name}"
    
    def __str__(self) -> str:
        return F"Projectname {self.name} with this KOnfiguration {self.joint}, {self.link}, {self.rotor}"