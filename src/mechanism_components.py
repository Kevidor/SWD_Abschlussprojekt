from math import sin, cos, atan, atan2, radians, degrees

class Joint:
    joints_count = 0
    joints = []

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

class Link:
    link_count = 0
    links = []

    def __init__(self, index:str, joint1: Joint, joint2: Joint, line_style: str = "-", line_color: str = "black"):
        self.index = index
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
    
#class Rotor:
#    def __init__(self, x: float, y:float, lenght: float = 1.0, angle: float = 0):
#        #self.center_joint = Joint(None, None, x, y, True)
#        self.x = x
#        self.y = y
#        self.lenght = lenght
#        self.angle = angle
#        self.rot_joint = Joint(None, None,
#                               self.x + self.lenght * cos(radians(self.angle)),
#                               self.y + self.lenght * sin(radians(self.angle))
#                            )
#    def update_rotation(self, add_angle: float = 1):
#        self.angle += add_angle
#        self.rot_joint.x = self.x + self.lenght * cos(radians(self.angle))
#        self.rot_joint.y = self.y + self.lenght * sin(radians(self.angle))
#
#    def __str__(self):
#        return f"Rotor({self.rot_joint}, {self.angle})"
    
class Rotor:
    rotors_count = 0
    rotors = []

    def __init__(self, x: float, y:float, rot_joint: Joint):
        self.x = x
        self.y = y
        self.rot_joint = rot_joint
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