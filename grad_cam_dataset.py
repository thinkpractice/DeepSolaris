import argparse
import sh
from imutils.paths import list_images
from keras.models import load_model
import progressbar


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", required=True, help="The dataset for which the gradcam images should be calculated")
    parser.add_argument("-m", "--model", required=True, help="The model to visualize")
    parser.add_argument("-o", "--output-directory", required=True, help="The output directory")
    parser.add_argument("-t", "--target-size", default=(187,187), nargs='+', type=int, help="The target size for the network input")
    args = vars(parser.parse_args())

    model = load_model(args["model"])
    model.summary()
    images = [image_path for image_path in list_images(args["dataset"])]
    
    widgets = ["Generating gradcam images: ", progressbar.Percentage(), " ", progressbar.Bar(), " ", progressbar.ETA()]
    pbar = progressbar.ProgressBar(maxval=len(images), widgets=widgets).start()
    for i, image_filename in enumerate(images):
        cmd = "grad_cam.py -i {image_file} -m {model} -o {output_directory} -t {target_size_first} {target_size_second}".format(image_file=image_filename, model=args["model"], output_directory=args["output_directory"], target_size_first=args["target_size"][0], target_size_second=args["target_size"][1])
        print("Running {}".format(cmd))
        grad_cam = sh.Command("python")
        grad_cam(cmd.split(" "))
        pbar.update(i)
    pbar.finish()

if __name__ == "__main__":
    main()

