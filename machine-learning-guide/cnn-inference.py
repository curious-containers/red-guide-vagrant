#!/usr/bin/env python3

import os
import argparse

import h5py
from tensorflow.keras.applications.nasnet import NASNetMobile


PREDICTIONS_FILE = 'predictions.csv'
INPUT_SHAPE = (96, 96, 3)


parser = argparse.ArgumentParser()
parser.add_argument(
    dest='data_file', type=str,
    help='Path to a PCAM *.h5 file.'
)
parser.add_argument(
    dest='weights_file', type=str,
    help='Path model *.h5 file.'
)
parser.add_argument(
    dest='start_index', type=int,
    help='Start index of data_file slice.'
)
parser.add_argument(
    dest='end_index', type=int,
    help='End index of data_file slice.'
)
args = parser.parse_args()

model = NASNetMobile(weights=None, input_shape=INPUT_SHAPE, classes=2)
model.load_weights(args.weights_file)

data_file = os.path.expanduser(args.data_file)
x = h5py.File(data_file, 'r', libver='latest', swmr=True)['x']
index = list(range(args.start_index, args.end_index))
x_data = x[index] / 256.0

predictions = model.predict(x_data)

with open(PREDICTIONS_FILE, 'w') as f:
    print(',p0,p1', file=f)
    for i, (p0, p1) in zip(index, predictions):
        print('{},{},{}'.format(i, p0, p1), file=f)
