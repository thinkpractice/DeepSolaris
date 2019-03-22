import argparse
import json
import os


def get_batches(images, number_of_splits):
    number_of_images = len(images)
    images_per_batch = number_of_images // number_of_splits
    images_for_batch = []
    index = 0
    for image_index, image_dict in enumerate(images):
        images_for_batch.append(image_dict)
        index += 1
        if index == images_per_batch or image_index == (number_of_images - 1):
            batch_to_return = images_for_batch
            images_for_batch = []
            index = 0
            yield batch_to_return


def filename_for_batch(filename, output_path, index):
    filename, _ = os.path.splitext(os.path.basename(filename))
    path = os.path.join(output_path, filename)
    return "{}_part{}.json".format(path, index)


def split_json(filename, output_path, number_of_splits):
    print("Splitting file={} into {} parts".format(filename, number_of_splits))
    with open(os.path.expanduser(filename)) as json_file:
        json_data = json.load(json_file)
        images = json_data["images"]
        number_of_images_written = 0
        for batch_index, batch in enumerate(get_batches(images, number_of_splits)):
            batch_filename = filename_for_batch(filename, output_path, batch_index)
            with open(batch_filename, "w") as batch_file:
                batch_size = len(batch)
                print("Writing batch {} into file: {} with {} images".format(batch_index + 1,
                                                                             batch_filename, batch_size))
                json.dump({
                    "current_page_index": 0,
                    "images": batch
                }, batch_file)
                number_of_images_written += batch_size
        print("Written {} images out of {} to {} batches".format(number_of_images_written, len(images),
                                                                 number_of_splits))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="The input json file")
    parser.add_argument("-n", "--number_of_splits", required=True, type=int,
                        help="The number of files the input file should be split into")
    parser.add_argument("-d", "--output_dir", help="The output dir to write the json files to", default=os.getcwd())
    args = vars(parser.parse_args())
    split_json(args["input"], args["output_dir"], args["number_of_splits"])


if __name__ == "__main__":
    main()
