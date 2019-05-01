from cbds.deeplearning import Project
from cbds.deeplearning.models import vgg16
from cbds.deeplearning.metrics import ClassificationReportCallback, ConfusionMatrixCallback, PlotRocCallback
from cbds.deeplearning import ImageGenerator
from keras.layers import GlobalAveragePooling2D, Dense, Dropout, Flatten
from keras.layers.normalization import BatchNormalization
from keras.models import Model

def vgg16_model():
    base_model = vgg16(input_shape=(187,187,3), include_top=False, weights="imagenet", )
    for layer in base_model.layers:
        layer.trainable = True
    
    last_conv_layer = base_model.get_layer("block4_conv3")
    x = GlobalAveragePooling2D()(last_conv_layer.output)
    x = Dense(512, activation="relu")(x)  
    x = BatchNormalization(axis=-1)(x)
    x = Dropout(0.25)(x)
    predictions = Dense(1, activation="sigmoid")(x)
    return Model(base_model.input, predictions)

with Project(project_path=r"/media/megatron/Projects/DeepSolaris") as project:
    dataset = project.dataset("Heerlen-HR")
    dataset.import_numpy_dataset(r"/media/megatron/9827-B092/hr_2018_18m_all.npy", r"/media/megatron/9827-B092/hr_2018_18m_all_labels.npy")


    train_dataset, test_dataset = dataset.split(test_size=0.2)
    train_generator = ImageGenerator(train_dataset)\
                        .with_shuffle_data(True)\
                        .with_rotation_range(45)\
                        .with_width_shift_range(0.1)\
                        .with_height_shift_range(0.1)\
                        .with_shear_range(0.1)\
                        .with_zoom_range(0.1)\
                        .with_channel_shift_range(0.1)\
                        .with_horizontal_flip(0.1)\
                        .with_rescale(1./255)
    test_generator = ImageGenerator(test_dataset)\
                        .with_rescale(1./255)

    print("Number of training items: {}".format(len(train_dataset)))
    print("Number of testing items: {}".format(len(test_dataset)))

    model = project.model("vgg16_small")

    vgg16_small = vgg16_model()
    model.create_model(vgg16_small)

    run = model.run()\
        .with_epochs(5)\
        .with_loss_function("binary_crossentropy")\
        .with_sgd_optimizer(lr=0.0001, momentum=0.9, decay=0.0001 / 20, nesterov=True)\
        .with_metric_callbacks([ClassificationReportCallback(), ConfusionMatrixCallback(), PlotRocCallback()])\
        .with_train_dataset(train_generator)\
        .with_test_dataset(test_generator)\
        .with_evaluation_dataset(test_generator)

    run.train()
    run.evaluate()



