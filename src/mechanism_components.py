from math import sin, cos, atan, atan2, radians, degrees
from serializable import Serializable
from database import DatabaseConnector

class Joint(Serializable):
    joints = []
    db_connector = DatabaseConnector().get_table("joint")

    def __init__(self, id: int, name: str, x: float, y: float, is_fixed: bool = False, is_drawn: bool = False):
        super().__init__(id)
        self.name = name
        self.x = x
        self.y = y
        self.is_fixed = is_fixed
        self.is_drawn = is_drawn

        Joint.joints.append(self)

    def __str__(self):
        return f"Joint({self.x}, {self.y})"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.id == other.id and self.name == other.name and self.x == other.x and self.y == other.y

    def to_dict(self):
        return {
                "id" : self.id,
                "x": self.x,
                "y" : self.y,
                "is_fixed" : self.is_fixed,
                "is_drawn" : self.is_drawn
            }
    
    @classmethod
    def clear(cls):
        cls.joints = []
    
    @classmethod
    def instantiate_from_dict(cls, data: dict):
        return cls(data['id'], data['name'], data['x'], data['y'], data['is_fixed'], data['is_drawn'])
    
    @classmethod
    def get_joint(self,id):
        for joint in self.joints:
            if joint.id == id:
                return joint
            
        
class Link(Serializable):
    links = []
    db_connector = DatabaseConnector().get_table("link")
    
    def __init__(self, id: int, joint1: Joint, joint2: Joint, line_style: str = "-", line_color: str = "black"):
        super().__init__(id)
        self.joint1 = joint1
        self.joint2 = joint2
        self.line_style = line_style
        self.line_color = line_color

        Link.links.append(self)

    def __str__(self):
        return f"Link({self.joint1}, {self.joint2})"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.id == other.id and self.joint1 == other.joint1 and self.joint2 == other.joint2
    
    def to_dict(self):
        return {
            "id" : self.id,
            "joint1" : self.joint1.to_dict(), 
            "joint2" : self.joint2.to_dict(),
            "line_style" : self.line_style,
            "line_color": self.line_color
            }
    
    @classmethod
    def clear(cls):
        cls.links = []
    
    @classmethod
    def instantiate_from_dict(cls, data: dict):
        return cls(data['id'], data['joint1'], data['joint2'], data['Linestyle'], data['Line_color'])
    
class Rotor(Serializable):
    rotors = []
    db_connector = DatabaseConnector().get_table("rotor")
    
    def __init__(self, id: int, x: float, y:float, rot_joint: Joint):
        super().__init__(id)
        self.x = x
        self.y = y
        self.rot_joint = rot_joint
        self.rot_joint.is_fixed = True
        self.lenght = ((rot_joint.x - x) ** 2 + (rot_joint.y - y) ** 2) ** 0.5
        self.angle = degrees(atan((rot_joint.y - y) / (rot_joint.x - x)))

        Rotor.rotors.append(self)

    def __str__(self):
        return f"Rotor({self.x}, {self.y}, {self.rot_joint})"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.id == other.id and self.x == other.x and self.x == other.x and self.rot_joint == other.rot_joint
    
    def update_rotation(self, add_angle: float = 1):
        self.angle += add_angle
        self.rot_joint.x = self.x + self.lenght * cos(radians(self.angle))
        self.rot_joint.y = self.y + self.lenght * sin(radians(self.angle))
    
    def to_dict(self):
        return {
            "id" : self.id,
            "x" : self.x, 
            "y" : self.y, 
            "rot_joint" :self.rot_joint.to_dict()
            }
    
    @classmethod
    def clear(cls):
        cls.rotors = []
    
    @classmethod
    def instantiate_from_dict(cls, data: dict) :
        return cls(data['x'], data['y'], data['rot_joint'])