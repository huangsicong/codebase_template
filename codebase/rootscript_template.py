# Copyright (c) 2018-present, Royal Bank of Canada.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
# Author: Sicong Huang

#!/usr/bin/env python3
""" An template for creating a root script. A root script should do a type of tasks."""
from __future__ import absolute_import, division, print_function
import os
import numpy as np
from datetime import datetime
import subprocess
import time
import torch
from torch import optim
from .hparams.registry import get_hparams
from .data.load_data import *
from .utils.experiment_utils import *
from .algorithms.train_vae import train_and_test
from .algorithms.train_mnist_CNN import get_mnist_representation
import argparse
import random
import sys
from .utils.vae_utils import prepare_vae
from .utils.aae_utils import aae_bridge

sys.stdout.flush()
parser = argparse.ArgumentParser()
parser.add_argument("--hparam_set", default="default", type=str)
parser.add_argument("--overwrite", default=False, type=bool)
parser.add_argument("--e_name")
args = parser.parse_args()
args_dict = vars(args)
hparams = get_hparams(args.hparam_set)
set_random_seed(hparams.random_seed)


def main(writer, hparams):

    # template to time your code
    for i in range(2):
        # whatever loop
        end_time = datetime.now()
        hour_summery = compute_duration(hparams.messenger.start_time, end_time)
        note_taking("Iteration {} finished. Took {} hours".format(
            i, hour_summery))
    logging(
        args_dict,
        hparams.to_dict(),
        hparams.messenger.results_dir,
        hparams.messenger.dir_path,
        stage="final")


if __name__ == '__main__':

    writer = initialze_run(hparams, args)
    start_time = datetime.now()
    hparams.messenger.start_time = start_time
    dir_path = os.path.dirname(os.path.realpath(__file__))
    git_label = subprocess.check_output(
        ["cd " + dir_path + " && git describe --always && cd .."],
        shell=True).strip()
    if hparams.verbose:
        note_taking("The git label is {}".format(git_label))
    main(writer, hparams)
    end_time = datetime.now()
    hour_summery = compute_duration(start_time, end_time)
    writer_json_path = hparams.messenger.tboard_path + "/tboard_summery.json"
    writer.export_scalars_to_json(writer_json_path)
    writer.close()
    note_taking(
        "Experiment finished, results written at: {}. Took {} hours".format(
            hparams.messenger.results_dir, hour_summery))
