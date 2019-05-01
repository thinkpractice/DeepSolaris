from sklearn.model_selection import RandomizedSearchCV
from cbds.deeplearning import Project, ImageGenerator

def create_models():
    return []

def main():
    with Project(project_path=r"/media/megatron/Projects/DeepSolaris") as project:
        dataset = project.dataset("Heerlen-HR")
        #dataset.import_numpy_dataset(r"/media/megatron/9827-B092/hr_2018_18m_all.npy", r"/media/megatron/9827-B092/hr_2018_18m_all_labels.npy")


        train_dataset, test_dataset = dataset.split(test_size=0.2)
        train_generator = ImageGenerator(train_dataset)\
                            .with_shuffle_data(True)\
                            # .with_rotation_range(45)\
                            # .with_width_shift_range(0.1)\
                            # .with_height_shift_range(0.1)\
                            # .with_shear_range(0.1)\
                            # .with_zoom_range(0.1)\
                            # .with_channel_shift_range(0.1)\
                            # .with_horizontal_flip(0.1)\
                            .with_rescale(1./255)
        test_generator = ImageGenerator(test_dataset)\
                            .with_rescale(1./255)

        print("Number of training items: {}".format(len(train_dataset)))
        print("Number of testing items: {}".format(len(test_dataset)))


        for name, cnn_model in create_models():
            model = project.model(name)
            model.create_model(cnn_model)
            keras_model = model.get_keras_classifier_model()

            randomized_search = RandomizedSearchCV()

            
            # run = model.run()\
            #     .with_epochs(5)\
            #     .with_loss_function("binary_crossentropy")\
            #     .with_sgd_optimizer(lr=0.0001, momentum=0.9, decay=0.0001 / 20, nesterov=True)\
            #     .with_metric_callbacks([ClassificationReportCallback(), ConfusionMatrixCallback(), PlotRocCallback()])\
            #     .with_train_dataset(train_generator)\
            #     .with_test_dataset(test_generator)\
            #     .with_evaluation_dataset(test_generator)
            #
            # run.train()
            # run.evaluate()


if __name__ == "__main__":
    main()