#!/bin/bash

set -e
set -u

while getopts ":i:m:p:o:" opt; do
  case $opt in
    i) annotation_file="$OPTARG"
    ;;
    m) model="$OPTARG"
    ;;
    p) dataset_paths="$OPTARG"
    ;;
    o) output_dir="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

base_name="$(basename $annotation_file)"
labeled_annotation_file="${base_name}_labeled.csv" 
annotations_with_filename_file="${output_dir}/${base_name}_with_filename.csv" 
filtered_annotations_file="${output_dir}/${base_name}_filtered.csv"

python label_annotations.py -i $annotation_file -o $labeled_annotation_file
python add_filenames_to_annotations.py -i $labeled_annotation_file -o $annotations_with_filename_file -p $dataset_paths
python filter_annotations.py -i $annotations_with_filename_file -o $filtered_annotations_file
python annotations_to_numpy.py -i $filtered_annotations_file -o $output_dir
python evaluate_dataset.py -i $output_dir -m $model

