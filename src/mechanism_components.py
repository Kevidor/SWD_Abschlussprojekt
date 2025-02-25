from math import sin, cos, atan, atan2, radians, degrees
from serializable import Serializable
from database import DatabaseConnector

class Joint(Serializable):
    
    joints_count = 0
    joints = []
    db_connector = DatabaseConnector().get_table("joint")

    def __init__(self, index: int, name: str, x: float, y: float, is_fixed: bool = False, is_drawn: bool = False):
        self.index = index
        self.name = name
        self.x = x
        self.y = y
        self.is_fixed = is_fixed
        self.is_drawn = is_drawn
        Joint.joints_count += 1
        Joint.joints.append(self)

    def __str__(self):
        return f"Joint({self.x}, {self.y}, {self.is_fixed})"
    
    def __repr__(self):
        return f"Joint({self.x}, {self.y}, {self.is_fixed})"
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def delete(self):
        Joint.joints_count -= 1

    def to_dict(self):
        return{
                "index" : self.index,
                "x": self.x,
                "y" : self.y,
                "is_fixed" : self.is_fixed,
                "is_drawn" : self.is_drawn
        }
    @classmethod
    def clear(cls):
        cls.joints = []
        cls.joints_count = 0
    
    @classmethod
    def instantiate_from_dict(cls, data: dict):
        return cls(data['index'], data['name'], data['x'], data['y'], data['is_fixed'], data['is_drawn'])
    
    def get_index(self) -> str:
        return F"{self.index}"
    
    def __str__(self) -> str:
        return F"index {self.index} Joint: {self.name} with coordinates {self.x},{self.y} and with the extra parameter {self.is_fixed}, {self.is_drawn}"
        
class Link(Serializable):
    link_count = 0
    links = []
    db_connector = DatabaseConnector().get_table("joint")
    
    def __init__(self, index:str, joint1: Joint, joint2: Joint, line_style: str = "-", line_color: str = "black"):
        super().id = index
        self.line_style = line_style
        self.line_color = line_color
        self.joint1 = joint1
        self.joint2 = joint2
        Link.link_count += 1
        Link.links.append(self)

    def __str__(self):
        return f"Link({self.joint1}, {self.joint2})"
    
    def __repr__(self):
        return f"Link({self.joint1} - {self.joint2})"
    
    def __eq__(self, other):
        return self.joint1 == other.joint1 and self.joint2 == other.joint2
    
    def delete(self):
        Link.link_count -= 1
    
    def to_dict(self):
        return {
            "index" : self.index,
            "line_style" : self.line_style,
            "line_color": self.line_color,
            "joint1" : self.joint1.to_dict(), 
            "joint2" : self.joint2.to_dict() 
               }
    
    @classmethod
    def clear(cls):
        cls.links = []
        cls.link_count = 0
    
    @classmethod
    def instantiate_from_dict(cls, data: dict):
        return cls(data['index'], data['joint1'], data['joint2'], data['Linestyle'], data['Line_color'])

    def get_index(self) -> str:
        return F"{self.index}"
    
    def __str__(self) -> str:
        return F"index {self.index} link with coordinates {self.joint1},{self.joint2} and with the extra parameter {self.Linestyle},{self.Line_color}"
    
class Rotor(Serializable):
    rotors_count = 0
    rotors = []
    db_connector = DatabaseConnector().get_table("rotor")
    
    def __init__(self, x: float, y:float, rot_joint: Joint):
        self.x = x
        self.y = y
        self.rot_joint = rot_joint
        self.rot_joint.is_fixed = True
        self.lenght = ((rot_joint.x - x) ** 2 + (rot_joint.y - y) ** 2) ** 0.5
        self.angle = degrees(atan((rot_joint.y - y) / (rot_joint.x - x)))
        Rotor.rotors_count += 1
        Rotor.rotors.append(self)

    def update_rotation(self, add_angle: float = 1):
        self.angle += add_angle
        self.rot_joint.x = self.x + self.lenght * cos(radians(self.angle))
        self.rot_joint.y = self.y + self.lenght * sin(radians(self.angle))

    def __str__(self):
        return f"Rotor({self.lenght}, {self.angle}, {self.rot_joint})"
    
    def to_dict(self):
        return {
            "x" : self.x, 
            "y" : self.y, 
            "rot_joint" :self.rot_joint.to_dict()
            }
    
    @classmethod
    def clear(cls):
        cls.rotors = []
        cls.rotors_count = 0
    
    @classmethod
    def instantiate_from_dict(cls, data: dict) :
        return cls(data['x'], data['y'], data['rot_joint'])
    
    def __str__(self) -> str:
        return F"coordinates {self.x},{self.y} and with the joint {self.rot_joint}"
    

if __name__ == "__main__":
    joint0 = Joint(0, "Joint0", 0, 0).__dict__

    print(joint0)