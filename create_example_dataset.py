import numpy as np

deepsolaris_images = np.load(r"/home/tdjg/Documents/DeepSolaris/deepsolaris_heerlen.npy")
deepsolaris_labels = np.load(r"/home/tdjg/Documents/DeepSolaris/deepsolaris_heerlen_labels.npy")

positives = deepsolaris_images[deepsolaris_labels == 1, :, :, :]
positive_labels = deepsolaris_labels[deepsolaris_labels == 1]
negatives = deepsolaris_images[deepsolaris_labels == 0, :, :, :]
negative_labels = deepsolaris_labels[deepsolaris_labels == 0]

print("Positives shape: {} - {}".format(positives.shape, positive_labels.shape))
print("Negatives shape: {} - {}".format(negatives.shape, negative_labels.shape))

positive_idx = np.random.choice(positives.shape[0], 500, replace=False)
positives_selection = positives[positive_idx,:,:,:]
positives_label_selection = positive_labels[positive_idx]

negative_idx = np.random.choice(negatives.shape[0], 500, replace=False)
negatives_selection = negatives[negative_idx,:,:,:]
negatives_label_selection = negative_labels[positive_idx]


print("Positives selection shape: {} - {}".format(positives_selection.shape, positives_label_selection.shape))
print("Negatives selection shape: {} - {}".format(negatives_selection.shape, negatives_label_selection.shape))

deepsolaris_selection = np.concatenate((positives_selection, negatives_selection), axis=0)
deepsolaris_selection_labels = np.concatenate((positives_label_selection, negatives_label_selection), axis=0)

np.save("deepsolaris_images_selection.npy", deepsolaris_selection)
np.save("deepsolaris_labels_selection.npy", deepsolaris_selection_labels)

