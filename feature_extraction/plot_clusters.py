import numpy as np
import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--num-clusters", type=int, required=True, help="Number of clusters to plot")
args = vars(parser.parse_args())

for i in range(args["num_clusters"]):
    print("Cluster {}".format(i))
    cluster_images = np.load("{}.npy".format(i))
    print("Shape: {}".format(cluster_images.shape))
    _, ax = plt.subplots(3, 3)
    i = 0
    for r in range(3):
        for c in range(3):
            image = cluster_images[0, i,:]
            print(image.shape)
            ax[r, c].imshow(image)
            i += 1
    plt.show()

