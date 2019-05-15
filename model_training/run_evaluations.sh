#!/bin/sh
workon DeepSolaris
python evaluate_single_vgg16_augmentation.py &> evaluate_single_vgg16_augmentation.log
python evaluate_single_vgg16_baseline.py &> evaluate_single_vgg16_baseline.log
python evaluate_single_vgg16_layer4.py &> evaluate_single_vgg16_layer4.log
python evaluate_single_vgg16_reduce_lr.py &> evaluate_single_vgg16_reduce_lr.log
