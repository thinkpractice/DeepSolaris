from cbds.deeplearning import Project, ImageGenerator
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--project-path", default=r"/media/megatron/Projects/DeepSolaris", help="The project path to use")
    parser.add_argument("-d", "--training-set", required=True, help="The dataset to train on")
    parser.add_argument("-t", "--test-set", default=0.25, help="The dataset to test on")
    parser.add_argument("-v", "--validation-set", default=0.10, help="The dataset to validate on")
    parser.add_argument("-s", "--sample-size", required=True, help="The sample fraction of the training set") 
    parser.add_argument("-e", "--epochs", default=10, help="The number of epochs to train the model")
    parser.add_argument("-b", "--batch_size", default=32, help="The batch_size to train with")
    parser.add_argument("-l", "--learning_rate", default=1e-4, help="The learning rate to train with")
    parser.add_argument("-m", "--model-name", required=True, help="The model to evaluate")
    args = vars(parser.parse_args())

    with Project(project_path=args["project_path"]) as project:
        dataset = project.dataset(args["training_set"])
        train_dataset = dataset.sample(sample_size=args["sample_size"], random_state=42)
        test_dataset = project.dataset(args["test_set"])
        validation_dataset = project.dataset(args["validation_set"])

        train_generator = ImageGenerator(train_dataset)\
                          .with_rescale(1/255.)\
                          .with_seed(42)\
                          .with_rotation_range(30)\
                          .with_width_shift_range(0.1)\
                          .with_height_shift_range(0.1)\
                          .with_zoom_range(0.2)\
                          .with_shear_range(0.2)\
                          .with_horizontal_flip(True)\
                          .with_fill_mode("reflect")

        test_generator = ImageGenerator(test_dataset)\
                         .with_rescale(1/255.)\
                         .with_seed(84)

        validation_generator = ImageGenerator(validation_dataset)\
                                .with_rescale(1/255.)\
                                .with_seed(84)

        image_shape = dataset.data[0].shape

        model = project.model(args["model_name"])
        model.plot()
        cnn_model.summary()

        with model.run().with_epochs(args["epochs"])\
                .with_batch_size(args["batch_size"])\
                .with_loss_function("binary_crossentropy")\
                .with_optimizer(RMSPropSettings(lr=args["learning_rate"]))\
                .with_metric_callbacks([ClassificationReportCallback(), ConfusionMatrixCallback(), PlotRocCallback()])\
                .with_class_weights(train_dataset.class_weights)\
                .with_train_dataset(train_generator)\
                .with_test_dataset(test_generator)\
                .with_evaluation_dataset(test_dataset)\
                .with_evaluation_dataset(validation_dataset) as run:
                run.train()
                run.evaluate()


if __name__ == "__main__":
    main()

