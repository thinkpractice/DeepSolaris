import numpy as np
import matplotlib.pyplot as plt


for i in range(8):
    print("Cluster {}".format(i))
    cluster_images = np.load("{}.npy".format(i))
    print("Shape: {}".format(cluster_images.shape))
    _, ax = plt.subplots(3, 3)
    i = 0
    for r in range(3):
        for c in range(3):
            image = cluster_images[i,:]
            print(image.shape)
            ax[r, c].imshow(image)
            i += 1
    plt.show()

