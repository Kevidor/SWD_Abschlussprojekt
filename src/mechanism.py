from math import sin, cos, radians
from tinydb import TinyDB, Query

db = TinyDB('mechanism_db.json')

def save_joints(joints):
    db.table('joints').truncate()
    for joint in joints:
        db.table('joints').insert({'x': joint.x, 'y': joint.y, 'is_fixed': joint.is_fixed})

def load_joints():
    return [Joint(j['x'], j['y']) for j in db.table('joints').all()]

def save_links(links):
    db.table('links').truncate()
    for link in links:
        db.table('links').insert({'joint1': {'x': link.joint1.x, 'y': link.joint1.y, 'is_fixed': link.joint1.is_fixed},
                                                'joint2': {'x': link.joint2.x, 'y': link.joint2.y, 'is_fixed': link.joint2.is_fixed}})

def load_links():
    return [Link(Joint(l['joint1']['x'], l['joint1']['y'], l['joint1']["is_fixed"]), 
                 Joint(l['joint2']['x'], l['joint2']['y'], l['joint2']["is_fixed"])) for l in db.table('links').all()]


class Joint:
    def __init__(self, x: float, y: float, is_fixed: bool = False):
        #self.name = name
        self.x = x
        self.y = y
        self.is_fixed = is_fixed

    def __str__(self):
        return f"Joint({self.x}, {self.y}, {self.is_fixed})"
    
    def __repr__(self):
        return f"Joint({self.x}, {self.y}, {self.is_fixed})"

class Link:
    def __init__(self, joint1: Joint, joint2: Joint):
        self.joint1 = joint1
        self.joint2 = joint2

    def __str__(self):
        return f"Link({self.joint1}, {self.joint2})"
    
    def __repr__(self):
        return f"Link({self.joint1} - {self.joint2})"
    
class Rotor:
    def __init__(self, joint: Joint, lenght: float, angle: float = 0):
        self.center_joint = joint
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