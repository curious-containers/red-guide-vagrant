#!/usr/bin/env python3

import os
import sys
import argparse
import random

import h5py
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.nasnet import NASNetMobile
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import AUC


# Constants
WEIGHTS_FILE = 'weights.h5'
TRAIN_X_FILE = 'camelyonpatch_level_2_split_train_x.h5'
TRAIN_Y_FILE = 'camelyonpatch_level_2_split_train_y.h5'
VALID_X_FILE = 'camelyonpatch_level_2_split_valid_x.h5'
VALID_Y_FILE = 'camelyonpatch_level_2_split_valid_y.h5'
INPUT_SHAPE = (96, 96, 3)


# Arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    dest='data_dir', type=str,
    help='Data: Path to read-only directory containing PCAM *.h5 files.'
)
parser.add_argument(
    '--learning-rate', type=float, default=0.0001,
    help='Training: Learning rate. Default: 0.0001'
)
parser.add_argument(
    '--batch-size', type=int, default=64,
    help='Training: Batch size. Default: 64'
)
parser.add_argument(
    '--num-epochs', type=int, default=5,
    help='Training: Number of epochs. Default: 5'
)
parser.add_argument(
    '--steps-per-epoch', type=int, default=None,
    help='Training: Steps per epoch. Default: data_size / batch_size'
)
parser.add_argument(
    '--log-dir', type=str, default=None,
    help='Debug: Path to writable directory for a log file to be created. Default: log to stdout / stderr'
)
parser.add_argument(
    '--log-file-name', type=str, default='training.log',
    help='Debug: Name of the log file, generated when --log-dir is set. Default: training.log'
)
args = parser.parse_args()


# Redirect output streams for logging
if args.log_dir:
    log_file = open(os.path.join(os.path.expanduser(args.log_dir), args.log_file_name), 'w')
    sys.stdout = log_file
    sys.stderr = log_file

print('GPU available:', tf.test.is_gpu_available())


# Model
model = NASNetMobile(weights=None, input_shape=INPUT_SHAPE, classes=2)
model.compile(
    loss='categorical_crossentropy',
    optimizer=Adam(args.learning_rate),
    metrics=['accuracy', AUC()]
)
model.summary()


# Input
def data_generator(x, y, batch_size=None):
    index = range(len(x))
    labels = np.array([[1, 0], [0, 1]])

    while True:
        index_sample = index
        if batch_size is not None:
            index_sample = sorted(random.sample(index, batch_size))

        x_data = x[index_sample] / 256.0
        y_data = y[index_sample]
        y_data = labels[y_data[:, 0, 0, 0]]
        yield x_data, y_data


data_dir = os.path.expanduser(args.data_dir)

train_x = h5py.File(os.path.join(data_dir, TRAIN_X_FILE), 'r', libver='latest', swmr=True)['x']
train_y = h5py.File(os.path.join(data_dir, TRAIN_Y_FILE), 'r', libver='latest', swmr=True)['y']
valid_x = h5py.File(os.path.join(data_dir, VALID_X_FILE), 'r', libver='latest', swmr=True)['x']
valid_y = h5py.File(os.path.join(data_dir, VALID_Y_FILE), 'r', libver='latest', swmr=True)['y']


# Training
data_size = len(train_x)
steps_per_epoch = data_size // args.batch_size

if args.steps_per_epoch:
    steps_per_epoch = args.steps_per_epoch

model.fit_generator(
    data_generator(train_x, train_y, batch_size=args.batch_size),
    steps_per_epoch=steps_per_epoch,
    epochs=args.num_epochs,
    validation_data=data_generator(valid_x, valid_y, batch_size=args.batch_size),
    validation_steps=1
)

# Output
model.save_weights(WEIGHTS_FILE)

if args.log_dir:
    sys.stdout.close()
