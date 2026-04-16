import numpy as np
import matplotlib.pyplot as plt

#good_run = target 6

def plot_path(x,y,z):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    # ax.scatter(x,y,z)

    for i in range(1,len(x)):
        ax.plot([x[i-1], x[i]], [y[i-1],y[i]],zs=[z[i-1],z[i]], color="blue")

    ax.plot([x[0], x[-1]], [y[0], y[-1]], [z[0], z[-1]], color="purple")
    ax.scatter(x[0], y[0], z[0], color="lightgreen")
    ax.scatter(x[-1], y[-1], z[-1], color="red")


    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

   


# pos = ["positions_zero_succes.txt", "positions_four_succes.txt", "positions_zero_semi_fail.txt", "positions_good_run.txt", "first_positions.txt"]
pos = ["positions_0_1231.txt"]
for i in pos:
    x,y,z = [],[],[]

    with open(i) as file:
        for line in file:
            line =  line.split(",")
            x.append(float(line[0]))
            y.append(float(line[1]))
            z.append(float(line[2]))
    plot_path(x,y,z)

plt.show()

    # print(x)
