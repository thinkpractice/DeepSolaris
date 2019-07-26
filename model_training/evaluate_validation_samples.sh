#!/usr/bin/env bash
project_path=$1
dataset=$2
test_set="${dataset}_test"
validation_set="${dataset}_val"
model_filename=$3
model_name=$4

echo $project_path

python split_train_test_validation.py -p $project_path -d $dataset
python evaluate_validation_set_performance.py -p $project_path -d $dataset -t $test_set -v $validation_set -s 0.1 -e 20 #-m $model_filename -n $model_name
python evaluate_validation_set_performance.py -p $project_path -d $dataset -t $test_set -v $validation_set -s 0.2 -e 20 #-m $model_filename -n $model_name
python evaluate_validation_set_performance.py -p $project_path -d $dataset -t $test_set -v $validation_set -s 0.3 -e 20 #-m $model_filename -n $model_name
python evaluate_validation_set_performance.py -p $project_path -d $dataset -t $test_set -v $validation_set -s 0.4 -e 20 #-m $model_filename -n $model_name
python evaluate_validation_set_performance.py -p $project_path -d $dataset -t $test_set -v $validation_set -s 0.5 -e 20 #-m $model_filename -n $model_name
python evaluate_validation_set_performance.py -p $project_path -d $dataset -t $test_set -v $validation_set -s 0.6 -e 20 #-m $model_filename -n $model_name
python evaluate_validation_set_performance.py -p $project_path -d $dataset -t $test_set -v $validation_set -s 0.7 -e 20 #-m $model_filename -n $model_name
python evaluate_validation_set_performance.py -p $project_path -d $dataset -t $test_set -v $validation_set -s 0.8 -e 20 #-m $model_filename -n $model_name
python evaluate_validation_set_performance.py -p $project_path -d $dataset -t $test_set -v $validation_set -s 0.9 -e 20 #-m $model_filename -n $model_name
python evaluate_validation_set_performance.py -p $project_path -d $dataset -t $test_set -v $validation_set -s 1.0 -e 20 #-m $model_filename -n $model_name


