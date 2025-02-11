from mechanism_components import Joint, Link
import numpy as np

class Mechanism:
    def __init__(self):
        self.joints = []
        self.links = []
        self.x = np.array([])
        self.A = np.array([])
        self.L = np.array([])

    #def add_joint(self, x: float, y: float, is_fixed: bool = False):
    #    self.joints.append(Joint(x, y, is_fixed))
    
    def add_joint(self, joint: Joint):
        self.joints.append(joint)

    def add_link(self, joint1: Joint, joint2: Joint): 
        self.links.append(Link(joint1, joint2))

    def create_joint_matrix(self):
        self.x = np.zeros((Joint.joints_count * 2, 1))
        for i, joint in enumerate(self.joints):
            # joint x
            self.x[i * 2] = joint.x
            # joint y
            self.x[i * 2 + 1] = joint.y
    
    def create_link_matrix(self):
        self.A = np.zeros((Link.link_count * 2, Joint.joints_count * 2))
        for i, link in enumerate(self.links):
            # link x
            self.A[i * 2, self.joints.index(link.joint1) * 2] = 1
            self.A[i * 2, self.joints.index(link.joint2) * 2] = -1
            # link y
            self.A[i * 2 + 1, self.joints.index(link.joint1) * 2 + 1] = 1
            self.A[i * 2 + 1, self.joints.index(link.joint2) * 2 + 1] = -1
    
    def create_lenght_matrix(self):
        l = self.A @ self.x
        self.L = np.zeros((Link.link_count, 2))
        for i in range(Link.link_count):
            # length x
            self.L[i, 0] = l[i * 2].item()
            # length y
            self.L[i, 1] = l[i * 2 + 1]

        l = np.zeros((Link.link_count, 1))
        for i in range(Link.link_count):
            l[i] = (self.L[i,0] ** 2 + self.L[i,1] ** 2) ** 0.5

        return l

if __name__ == "__main__":
    mekanism = Mechanism()

    joint0 = Joint(0,0)
    joint1 = Joint(10, 35)
    joint2 = Joint(-25, 10)

    mekanism.add_joint(joint1)
    mekanism.add_joint(joint0)
    mekanism.add_joint(joint2)

    mekanism.add_link(joint0, joint1)
    mekanism.add_link(joint1, joint2)

    mekanism.create_joint_matrix()
    mekanism.create_link_matrix()
    l = mekanism.create_lenght_matrix()
    
    print(f"x = \n{mekanism.x}")
    print(f"A = \n{mekanism.A}")
    print(f"L = \n{mekanism.L}")
    print(f"l = \n{l}")
