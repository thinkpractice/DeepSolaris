from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras.applications import *

class ModelFactory(object):
    @classmethod
    def base_models(cls):
        return {"vgg16": lambda pre_trained_weights, include_top: VGG16(weights=pre_trained_weights, include_top=include_top),
                "vgg19": lambda pre_trained_weights, include_top: VGG19(weights=pre_trained_weights, include_top=include_top),
                "xception": lambda pre_trained_weights, include_top: Xception(weights=pre_trained_weights, include_top=include_top),
                "resnet50": lambda pre_trained_weights, include_top: ResNet50(weights=pre_trained_weights, include_top=include_top),
                "inception_v3": lambda pre_trained_weights, include_top: InceptionV3(weights=pre_trained_weights, include_top=include_top),
                "inception_resnet_v2": lambda pre_trained_weights, include_top: InceptionResNetV2(weights=pre_trained_weights, include_top=include_top),
                "mobilenet": lambda pre_trained_weights, include_top: MobileNet(weights=pre_trained_weights, include_top=include_top),
                "mobilenet_v2": lambda pre_trained_weights, include_top: MobileNetV2(weights=pre_trained_weights, include_top=include_top),
                "densenet121": lambda pre_trained_weights, include_top: DenseNet121(weights=pre_trained_weights, include_top=include_top),
                "densenet169": lambda pre_trained_weights, include_top: DenseNet169(weights=pre_trained_weights, include_top=include_top),
                "densenet201": lambda pre_trained_weights, include_top: DenseNet201(weights=pre_trained_weights, include_top=include_top),
                "nasnet_mobile": lambda pre_trained_weights, include_top: NASNetMobile(weights=pre_trained_weights, include_top=include_top),
                "nasnet_large": lambda pre_trained_weights, include_top: NASNetLarge(weights=pre_trained_weights, include_top=include_top),
                }

    @classmethod
    def available_base_models(cls):
        return ModelFactory.base_models().keys()

    @classmethod
    def base_model_for(cls, model_name):
        return ModelFactory.base_models()[model_name]

    @classmethod
    def base_model_for_settings(cls, settings):
        return ModelFactory.base_model_for(settings.model_name)(settings.pre_trained_weights, settings.include_top)

    @classmethod
    def build_model(cls, base_model, all_trainable):
        base_model.summary()
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(1024, activation='relu')(x)
        predictions = Dense(1, activation='sigmoid')(x)
        model = Model(inputs=base_model.input, outputs=predictions)
        for layer in base_model.layers:
            layer.trainable = all_trainable
        return model

    @classmethod
    def model_for_settings(cls, settings):
        if settings.model_name == "vgg16_gap":
            return cls.vgg16_gap(settings.last_vgg_layer)

        base_model = ModelFactory.base_model_for_settings(settings)
        return cls.build_model(base_model, settings)

    @classmethod
    def model_for(cls, model_name, all_trainable=False):
        base_model = ModelFactory.base_model_for(model_name)(None, False)
        return cls.build_model(base_model, all_trainable)

    @classmethod
    def load_model_from_file(cls, model_name, filename):
        model = ModelFactory.model_for(model_name)
        model.load_weights(filename)
        model.summary()
        return model

    @classmethod
    def vgg16_gap(cls, last_vgg_layer="block3_conv3"):
        base_model = ModelFactory.model_for("vgg16")
        last_conv_layer = base_model.get_layer(last_vgg_layer)
        x = GlobalAveragePooling2D(last_conv_layer.output)
        predictions = Dense(2, activation="softmax", init="uniform")(x)
        return Model(inputs=base_model.input, outputs=predictions)
