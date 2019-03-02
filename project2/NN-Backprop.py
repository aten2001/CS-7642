import sys

sys.path.append("./ABAGAIL/ABAGAIL.jar")

import base
from java.lang import Math
from shared import Instance
import random as rand
import time
import os
import csv
from func.nn.activation import RELU, LogisticSigmoid
from func.nn.backprop import RPROPUpdateRule, BatchBackPropagationTrainer
from shared import SumOfSquaresError, DataSet, Instance
from func.nn.backprop import BackPropagationNetworkFactory
"""
Backprop NN training
"""
# Adapted from https://github.com/JonathanTay/CS-7641-assignment-2/blob/master/NN0.py

# TODO: Move this to a common lib?
OUTPUT_DIRECTORY = './output'

base.make_dirs(OUTPUT_DIRECTORY)

# Network parameters found "optimal" in Assignment 1
OUTFILE = OUTPUT_DIRECTORY + '/NN_OUTPUT/NN_{}_LOG.csv'


def main(layers, training_iterations, test_data_file, train_data_file, validate_data_file):
    """Run this experiment"""
    training_ints = base.initialize_instances(train_data_file)
    testing_ints = base.initialize_instances(test_data_file)
    validation_ints = base.initialize_instances(validate_data_file)
    factory = BackPropagationNetworkFactory()
    measure = SumOfSquaresError()
    data_set = DataSet(training_ints)
    # relu = RELU()
    relu = LogisticSigmoid()
    # 50 and 0.000001 are the defaults from RPROPUpdateRule.java
    rule = RPROPUpdateRule(0.064, 50, 0.000001)
    oa_names = ["Backprop"]
    classification_network = factory.createClassificationNetwork(layers, relu)
    base.train(BatchBackPropagationTrainer(data_set, classification_network, measure, rule), classification_network,
               'Backprop', training_ints, validation_ints, testing_ints, measure, training_iterations,
               OUTFILE.format('Backprop'))
    return


if __name__ == "__main__":
    with open(OUTFILE.format('Backprop'), 'a+') as f:
        f.write('{},{},{},{},{},{},{},{},{},{},{}\n'.format('iteration', 'MSE_trg', 'MSE_val', 'MSE_tst', 'acc_trg',
                                                            'acc_val', 'acc_tst', 'f1_trg', 'f1_val', 'f1_tst',
                                                            'elapsed'))
    DS_NAME = 'Diabetes'
    TEST_DATA_FILE = 'data/{}_test.csv'.format(DS_NAME)
    TRAIN_DATA_FILE = 'data/{}_train.csv'.format(DS_NAME)
    VALIDATE_DATA_FILE = 'data/{}_validate.csv'.format(DS_NAME)
    main([19, 10, 1], 5001, TEST_DATA_FILE,
         TRAIN_DATA_FILE, VALIDATE_DATA_FILE)
