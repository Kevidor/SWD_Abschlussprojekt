from math import sin, cos, radians

class Joint:
    joints_count = 0

    def __init__(self, x: float, y: float, is_fixed: bool = False):
        self.x = x
        self.y = y
        self.is_fixed = is_fixed
        Joint.joints_count += 1

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

    def __init__(self, joint1: Joint, joint2: Joint):
        self.joint1 = joint1
        self.joint2 = joint2
        Link.link_count += 1

    def __str__(self):
        return f"Link({self.joint1}, {self.joint2})"
    
    def __repr__(self):
        return f"Link({self.joint1} - {self.joint2})"
    
    def __eq__(self, other):
        return self.joint1 == other.joint1 and self.joint2 == other.joint2
    
    def delete(self):
        Link.link_count -= 1
    
class Rotor:
    def __init__(self, x: float, y:float, lenght: float, angle: float = 0):
        self.center_joint = Joint(x, y, True)
        self.lenght = lenght
        self.angle = angle
        self.rot_joint = Joint(self.center_joint.x + self.lenght * cos(radians(self.angle)),
                               self.center_joint.y + self.lenght * sin(radians(self.angle))
                            )
    def update_rotation(self, add_angle: float = 1):
        self.angle += add_angle
        self.rot_joint.x = self.center_joint.x + self.lenght * cos(radians(self.angle))
        self.rot_joint.y = self.center_joint.y + self.lenght * sin(radians(self.angle))

    def __str__(self):
        return f"Rotor({self.rot_joint}, {self.angle})"