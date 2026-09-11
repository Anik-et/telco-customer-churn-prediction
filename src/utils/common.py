from pathlib import Path
import yaml


def read_yaml(path: str):

    with open(Path(path), "r") as file:

        config = yaml.safe_load(file)

    return config