from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras.applications import *

class ModelFactory(object):
    @classmethod
    def base_models(cls):
        return {"vgg16": lambda settings: VGG16(weights=settings.pre_trained_weights, include_top=settings.include_top),
                "vgg19": lambda settings: VGG19(weights=settings.pre_trained_weights, include_top=settings.include_top),
                "xception": lambda settings: Xception(weights=settings.pre_trained_weights, include_top=settings.include_top),
                "resnet50": lambda settings: ResNet50(weights=settings.pre_trained_weights, include_top=settings.include_top),
                "inception_v3": lambda settings: InceptionV3(weights=settings.pre_trained_weights, include_top=settings.include_top),
                "inception_resnet_v2": lambda settings: InceptionResNetV2(weights=settings.pre_trained_weights, include_top=settings.include_top),
                "mobilenet": lambda settings: MobileNet(weights=settings.pre_trained_weights, include_top=settings.include_top),
                "mobilenet_v2": lambda settings: MobileNetV2(weights=settings.pre_trained_weights, include_top=settings.include_top),
                "densenet121": lambda settings: DenseNet121(weights=settings.pre_trained_weights, include_top=settings.include_top),
                "densenet169": lambda settings: DenseNet169(weights=settings.pre_trained_weights, include_top=settings.include_top),
                "densenet201": lambda settings: DenseNet201(weights=settings.pre_trained_weights, include_top=settings.include_top),
                "nasnet_mobile": lambda settings: NASNetMobile(weights=settings.pre_trained_weights, include_top=settings.include_top),
                "nasnet_large": lambda settings: NASNetLarge(weights=settings.pre_trained_weights, include_top=settings.include_top),
                }

    @classmethod
    def available_base_models(cls):
        return ModelFactory.base_models().keys()

    @classmethod
    def base_model_for(cls, settings):
        return ModelFactory.base_models()[settings.model_name](settings)

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