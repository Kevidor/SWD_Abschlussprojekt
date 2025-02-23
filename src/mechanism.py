from mechanism_components import Joint, Link, Rotor
import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import tempfile
import pandas as pd
import os
class Mechanism:
    def __init__(self):
        self.joints = Joint.joints
        self.links = Link.links
        self.rotors = Rotor.rotors

        self.x = np.array([])
        self.A = np.array([])
        self.L = np.array([])
        
    def clear(self):
        self.joints = []
        self.links = []
        self.x = np.array([])
        self.A = np.array([])
        self.L = np.array([])

    def calc_DOF(self):
        n = len(self.joints)
        print(f"Joints: {n}")
        BC = len([j for j in self.joints if j.is_fixed])
        print(f"BC: {BC}")
        m = len(self.links)
        print(f"Links: {m}")
        dof = 2 * n - 2 * BC - m
        return dof

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
        self.create_joint_matrix()
        self.create_link_matrix()
        
        l = self.A @ self.x
        self.L = np.zeros((Link.link_count, 2))
        for i in range(Link.link_count):
            # length x
            self.L[i, 0] = l[i * 2].item()
            # length y
            self.L[i, 1] = l[i * 2 + 1].item()

        l = np.zeros((Link.link_count, 1))
        for i in range(Link.link_count):
            l[i] = (self.L[i,0] ** 2 + self.L[i,1] ** 2) ** 0.5

        return l
    
    def calc_error(self, l1: float):
        l2 = self.create_lenght_matrix()
        e = l2 - l1
        return e.flatten()
    
    def optimize_positions(self, angle: float = 10):
        l1 = self.create_lenght_matrix()
        
        self.rotors[0].update_rotation(angle)

        non_fixed_joints = [j for j in self.joints if not j.is_fixed]

        x0 = np.array([coord for j in non_fixed_joints for coord in (j.x, j.y)])

        def objective(x):
            for i, joint in enumerate(non_fixed_joints):
                joint.x, joint.y = x[i * 2], x[i * 2 + 1]
            
            return self.calc_error(l1)

        result = opt.least_squares(objective, x0)

        for i, joint in enumerate(non_fixed_joints):
            joint.x, joint.y = result.x[i * 2], result.x[i * 2 + 1]
        
        return result
    
    def create_animation(self ):
        fig, ax = plt.subplots()
        
        ax.set_xlim(-100,100)
        ax.set_ylim(-100,100)
        ax.set_aspect("equal")
        
        joint_scatter, = ax.plot([], [], 'ro', markersize=6)  # Red joints
        rotor_scatter, = ax.plot([],[],'g', markersize=3)
        link_lines = [ax.plot([], [], 'b-')[0] for _ in self.links]  # Blue links
        # Dictionary to store past positions of drawn joints
        drawn_joints = [i for i, joint in enumerate(self.joints) if joint.is_drawn]
        joint_trajectories = {i: ([], []) for i in drawn_joints}
        trajectory_lines = {i: ax.plot([], [], 'g-', linewidth=1)[0] for i in drawn_joints}

        def update(frame):
            """Update the echanism at each frame"""
            self.optimize_positions(1)

            x_vals = [joint.x for joint in self.joints]
            y_vals = [joint.y for joint in self.joints]
            joint_scatter.set_data(x_vals, y_vals)

            x_val_rot = [rotor.x for rotor in self.rotors]
            y_val_rot = [rotor.y for rotor in self.rotors]
            rotor_scatter.set_data(x_val_rot, y_val_rot)

            for i, link in enumerate(self.links):
                x_link = [link.joint1.x, link.joint2.x]
                y_link = [link.joint1.y, link.joint2.y]
                link_lines[i].set_data(x_link, y_link)

            # Update trajectories for drawn joints
            for i in drawn_joints:
                x_traj, y_traj = joint_trajectories[i]
                x_traj.append(self.joints[i].x)
                y_traj.append(self.joints[i].y)
                trajectory_lines[i].set_data(x_traj, y_traj)
    
            return [joint_scatter] + [rotor_scatter] + link_lines + list(trajectory_lines.values()) 
        
        ani = animation.FuncAnimation(fig, update, frames=360, interval=50, blit= False)
        gif_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".gif")
        ani.save(gif_temp.name, writer=animation.PillowWriter(fps=30))
        print("GIF saved as mechanism_animation.gif")
        return gif_temp.name
        
    def create_csv(self):
        data = []
        for i in range(360):
            self.optimize_positions(1),
            data.append({
                        "rotor_angle" : [rotor.angle for rotor in self.rotors],
                        "x" : [joint.x for joint in self.joints],
                        "y" : [joint.y for joint in self.joints]
                        })
        datra_frame = pd.DataFrame(data)
        return datra_frame.to_csv("Values.csv",index=True, header=True)

        
if __name__ == "__main__":
    # Initialize Mechanism
    mekanism = Mechanism()

    # Viergelenk
    #joint0 = Joint(None, "Joint0", 0, 0, True, False)
    #joint1 = Joint(None, "Joint1", 10, 35, False, True)
    #joint2 = Joint(None, "Joint2", -25, 10, False, True)
    #
    #rotor0 = Rotor(-30, 0, joint2)
    #
    #link0 = Link(None, joint0, joint1)
    #link1 = Link(None, joint1, rotor0.rot_joint)

    # Strandbeest
    joint0 = Joint(None, "Joint1", 0, 0, True, False)
    joint1 = Joint(None, "Joint3", 49.73, -1.55, False, True)
    joint2 = Joint(None, "Joint4", 18.2, 37.3, False, True)
    joint3 = Joint(None, "Joint5", -34.82, 19.9, False, True)
    joint4 = Joint(None, "Joint6", -30.5, -19.22, False, True)
    joint5 = Joint(None, "Joint7", -19.33, -84.03, False, True)
    joint6 = Joint(None, "Joint8", 0.67, -39.3, False, True)
    
    rotor0 = Rotor(38, 7.8, joint1)
    
    link0 = Link(None, joint0, joint2)
    link1 = Link(None, joint0, joint3)
    link2 = Link(None, joint0, joint6)
    link3 = Link(None, rotor0.rot_joint, joint2)
    link4 = Link(None, joint2, joint3)
    link5 = Link(None, joint3, joint4)
    link6 = Link(None, joint4, joint5)
    link7 = Link(None, joint5, joint6)
    link8 = Link(None, joint6, rotor0.rot_joint)
    link9 = Link(None, joint6, joint4)
    
    print(f"Remaining DOF: {mekanism.calc_DOF()}")
    
    mekanism.create_animation()

    #mekanism.create_joint_matrix()
    #mekanism.create_link_matrix()
    #l = mekanism.create_lenght_matrix()
    #
    #print("\n Initial Mechanism:")
    #print(f"x = \n{mekanism.x}")
    #print(f"A = \n{mekanism.A}")
    #print(f"L = \n{mekanism.L}")
    #print(f"l = \n{l}")
    #
    #print("\n")
    #rotor0.update_rotation(10)
    #print(rotor0)
    #
    #mekanism.create_joint_matrix()
    #mekanism.create_link_matrix()
    #l = mekanism.create_lenght_matrix()
    #
    #print("\n Rotated Mechanism:")
    #print(f"x = \n{mekanism.x}")
    #print(f"A = \n{mekanism.A}")
    #print(f"L = \n{mekanism.L}")
    #print(f"l = \n{l}")

    #print(mekanism.calc_error(10))
