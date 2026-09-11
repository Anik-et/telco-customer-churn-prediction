import yaml


def read_yaml(path):
    with open(path, "r") as file:
        config = yaml.safe_load(file)

    return config