#!/usr/bin/env python
# (C) Copyright 2024 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#


import json

import hydra
from anemoi.utils.config import load_raw_config
from omegaconf import OmegaConf

from . import Command


class Train(Command):

    accept_unknown_args = True

    def add_arguments(self, command_parser):
        command_parser.add_argument(
            "--config",
            action="append",
            type=str,
            help="A list of extra config files to load",
            default=[],
        )

    def run(self, args, overrides=[]):

        hydra.initialize(config_path="../config", version_base="1.1")

        cfg = hydra.compose(config_name="config", overrides=overrides)

        # Add project config
        # cfg = OmegaConf.merge(cfg, OmegaConf.create(...))

        # Add experiment config
        # cfg = OmegaConf.merge(cfg, OmegaConf.create(...))

        # Add user config
        cfg = OmegaConf.merge(
            cfg,
            OmegaConf.create(
                load_raw_config(
                    "training.yaml",
                    default={},
                )
            ),
        )

        # Add extra config files specified in the command line

        for config in args.config:
            print(f"Loading config {config}")
            cfg = OmegaConf.merge(cfg, OmegaConf.load(config))

        # We need to reapply the overrides
        cfg = OmegaConf.merge(cfg, OmegaConf.from_dotlist(overrides))

        print(json.dumps(OmegaConf.to_container(cfg, resolve=True), indent=4))

        # AIFSTrainer(cfg).train()


command = Train
