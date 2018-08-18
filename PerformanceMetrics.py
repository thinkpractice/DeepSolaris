from keras import backend as K

class PerformanceMetrics(object):
    @classmethod
    def precision(cls, y_true, y_pred):
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())
        return precision

    @classmethod
    def recall(cls, y_true, y_pred):
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = true_positives / (possible_positives + K.epsilon())
        return recall

    @classmethod
    def fbeta_score(cls, y_true, y_pred, beta=1):
        if beta < 0:
            raise ValueError('The lowest choosable beta is zero (only precision).')
        # If there are no true positives, fix the F score at 0 like sklearn.
        if K.sum(K.round(K.clip(y_true, 0, 1))) == 0:
            return 0
        p = PerformanceMetrics.precision(y_true, y_pred)
        r = PerformanceMetrics.recall(y_true, y_pred)
        bb = beta ** 2
        fbeta_score = (1 + bb) * (p * r) / (bb * p + r + K.epsilon())
        return fbeta_score

    @classmethod
    def fmeasure(cls, y_true, y_pred):
        return PerformanceMetrics.fbeta_score(y_true, y_pred, beta=1)