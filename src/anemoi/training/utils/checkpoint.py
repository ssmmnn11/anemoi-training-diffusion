# (C) Copyright 2024 European Centre for Medium-Range Weather Forecasts.
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

import json
from pathlib import Path
from zipfile import ZipFile

import torch

from anemoi.training.train.forecaster import GraphForecaster


def load_and_prepare_model(lightning_checkpoint_path: str) -> tuple[torch.nn.Module, dict]:
    """Load the lightning checkpoint and extract the pytorch model and its metadata.

    Parameters
    ----------
        lightning_checkpoint_path : str
            path to lightning checkpoint

    Returns
    -------
        Tuple[torch.nn.Module, Dict]
            pytorch model, metadata
    """
    module = GraphForecaster.load_from_checkpoint(lightning_checkpoint_path)
    model = module.model

    save_metadata = model.metadata
    model.metadata = None
    model.config = None

    metadata = dict(**save_metadata)
    return model, metadata


def save_inference_checkpoint(model: torch.nn.Module, metadata: dict, save_path: str) -> None:
    """Save a pytorch checkpoint for inference with the model metadata.

    Args:
        model (torch.nn.Module): pytorch model
        metadata (Dict): metadata
        save_path (str): path to inference/anemoi checkpoint
    """
    inference_filepath = Path(save_path).parent / Path("inference-" + str(Path(save_path).name))
    torch.save(model, inference_filepath)

    with ZipFile(inference_filepath, "a") as zipf:
        base = Path(inference_filepath).stem
        zipf.writestr(
            f"{base}/ai-models.json",
            json.dumps(metadata),
        )
