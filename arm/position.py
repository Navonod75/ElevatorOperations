import numpy as np
import matplotlib.pyplot as plt
# from arm import Arm

fig = plt.figure()
ax = fig.add_subplot(projection='3d')


joints = np.array([
    [0,0,0],
    [0,0,2],
    [1,1,4],
    [2,3,2]
])

def calc_pos(joint_angles, pos):
    res = np.array([
        [0,0,0],
        [0,0,1]])
    




    np.append(res, pos[:3])
    return res

ax.scatter(joints[:,0],joints[:,1],joints[:,2])

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()