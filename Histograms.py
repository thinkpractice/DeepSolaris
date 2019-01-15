import cv2 as cv

class Histograms(object):
    @classmethod
    def normalized_hist(cls, hist_image, channel, mask=None):
        hist = cv.calcHist([hist_image], [channel], mask, [256], [0, 255])  
        number_of_pixels = hist_image.size if mask is None else mask[mask > 0].size
        return hist / number_of_pixels

    @classmethod
    def all_bands_hist(cls, hist_image, mask=None):
        all_bands_hist = []
        for i in range(3):
            all_bands_hist.extend(Histograms.normalized_hist(hist_image, i, mask))
        return np.array(all_bands_hist)

    @classmethod
    def calculate_hist_for_images(cls, images):
        all_hists = np.array([[Histograms.normalized_hist(image, channel) for image in images] for channel in range(3)])

        return all_hists.reshape(all_hists.shape[0:3])

    @classmethod
    def summed_hist_for_images(cls, images):
        all_hists = Histograms.calculate_hist_for_images(images)
        return all_hists.sum(axis=1)
