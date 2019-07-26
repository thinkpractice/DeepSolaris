#!/usr/bin/env bash
set project_path=$1
set dataset=$2
set test_set="$dataset_test"
set validation_set="$dataset_val"
set model_filename=$3
set model_name=$4

python split_train_test_validation.py -p $project_path -d $dataset
python evaluate_validation_set_performance.py -p $project_path -d $dataset -t $test_set -v $validation_set -s 0.1 -m $model_filename -n $model_name
python evaluate_validation_set_performance.py -p $project_path -d $dataset -t $test_set -v $validation_set -s 0.2 -m $model_filename -n $model_name
python evaluate_validation_set_performance.py -p $project_path -d $dataset -t $test_set -v $validation_set -s 0.3 -m $model_filename -n $model_name
python evaluate_validation_set_performance.py -p $project_path -d $dataset -t $test_set -v $validation_set -s 0.4 -m $model_filename -n $model_name
python evaluate_validation_set_performance.py -p $project_path -d $dataset -t $test_set -v $validation_set -s 0.5 -m $model_filename -n $model_name
python evaluate_validation_set_performance.py -p $project_path -d $dataset -t $test_set -v $validation_set -s 0.6 -m $model_filename -n $model_name
python evaluate_validation_set_performance.py -p $project_path -d $dataset -t $test_set -v $validation_set -s 0.7 -m $model_filename -n $model_name
python evaluate_validation_set_performance.py -p $project_path -d $dataset -t $test_set -v $validation_set -s 0.8 -m $model_filename -n $model_name
python evaluate_validation_set_performance.py -p $project_path -d $dataset -t $test_set -v $validation_set -s 0.9 -m $model_filename -n $model_name
python evaluate_validation_set_performance.py -p $project_path -d $dataset -t $test_set -v $validation_set -s 1.0 -m $model_filename -n $model_name


