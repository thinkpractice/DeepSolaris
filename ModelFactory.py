from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras.applications.vgg16 import VGG16

class ModelFactory(object):
    @classmethod
    def models(cls):
        return {"vgg16": lambda settings: VGG16(weights=settings.pre_trained_weights, include_top=settings.include_top)}

    @classmethod
    def base_model_for(cls, settings):
        return ModelFactory.models()[settings.model_name](settings)

    @classmethod
    def model_for(cls, settings):
        base_model = ModelFactory.base_model_for(settings)
        base_model.summary()
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(1024, activation='relu')(x)
        predictions = Dense(1, activation='sigmoid')(x)

        model = Model(inputs=base_model.input, outputs=predictions)
        for layer in base_model.layers:
            layer.trainable = settings.all_trainable
        return model