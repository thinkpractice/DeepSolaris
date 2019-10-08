import numpy as np
import matplotlib.pyplot as plt


for i in range(8):
    print("Cluster {}".format(i))
    c = np.load("{}.npy".format(i))
    _, ax = plt.subplots(3, 3)
    i = 0
    for r in range(3):
        for co in range(3):
            ax[r, co].imshow(c[i,:])
            i += 1
    plt.show()

