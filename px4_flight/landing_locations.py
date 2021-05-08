import matplotlib.pyplot as plt
from IPython.core.debugger import set_trace
import numpy as np

def main():
    standardData = -np.array([[14.0,-1.0],
                             [19.5,9.4],
                             [7.0,1.7],
                             [18.2,-9.9],
                             [6.0,4.0],
                             [15.6,0.2]])

    fastData = -np.array([[-0.4,12.9],
                         [7.3,-14.3],
                         [-0.9,-10.3],
                         [3.0,-20.3]])

    swayData = -np.array([[-0.6,4.0],
                         [4.9,-17.3]])

    turnData = -np.array([[-0.8,-4.0],
                         [-5.1,-1.2]])

    figure, axes = plt.subplots()
    plt.xlim(-45.0,45.0)
    plt.ylim(-45.0,45.0)

    circle1 = plt.Circle((0, 0), 20,fill=False,color='blue')
    circle2 = plt.Circle((0,0),10,fill=False,color='orange')

    axes.set_aspect(1)
    axes.add_artist(circle1)
    axes.add_artist(circle2)

    plt.scatter(standardData.T[1],standardData.T[0],label='standard')
    plt.scatter(fastData.T[1],fastData.T[0],label='fast')
    plt.scatter(swayData.T[1],swayData.T[0],label='sway')
    plt.scatter(turnData.T[1],turnData.T[0],label='turn')
    plt.plot(0,0,'x',color='black',label = 'center')
    # plt.axhline(0.0,color='gray')
    # plt.axvline(0.0,color='gray')
    plt.legend(bbox_to_anchor=(1.35,1))
    plt.tight_layout()

    plt.show()

if __name__ == '__main__':
	main()