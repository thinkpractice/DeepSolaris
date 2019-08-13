#!/bin/bash

set -e

while getopts ":i:m:p:o:" opt; do
  case $opt in
    i) annotation_file="$OPTARG"
    ;;
    m) model="$OPTARG"
    ;;
    p) dataset_paths="$OPTARG"
    ;;
    o) output_dir="$OPTARG"
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

labeled_annotation_file=
annotations_with_filename_file=
filtered_annotations_file=

python label_annotations.py -i $annotation_file -o $labeled_annotation_file
python add_filename_to_annotations.py -i $labeled_annotation_file -o $annotations_with_filename_file -p $dataset_paths
python filter_annotations.py -i $annotation_with_filename_file -o $filtered_annotations_file
python annotations_to_numpy.py -i $filtered_annotations_file -o $output_dir
python evaluate_dataset.py -i $output_dir -m $model

