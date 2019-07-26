import argparse

from cbds.deeplearning import Project


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--project-path", default=r"/media/megatron/Projects/DeepSolaris", help="The project path to use")
    parser.add_argument("-d", "--dataset", required=True, help="The dataset to train/validate on")
    parser.add_argument("-t", "--test-size", default=0.25, help="The fraction of the complete data to use as test set")
    parser.add_argument("-v", "--validation-size", default=0.10, help="The fraction of the training set to use for validation")
    args = vars(parser.parse_args())

    with Project(project_path=args["project_path"]) as project:
        dataset = project.dataset(args["dataset"])
        train_val_dataset, test_dataset = dataset.split(test_size=args["test_size"], first_name="{}_train_val".format(args["dataset"]), second_name="{}_test".format(args["dataset"]))
        train_dataset, validation_dataset = dataset.split(test_size=args["validation_size"], first_name="{}_train".format(args["dataset"]), second_name="{}_val".format(args["dataset"]))
        train_dataset.save_dataset()
        test_dataset.save_dataset()
        validation_dataset.save_dataset()


if __name__ == "__main__":
    main()

