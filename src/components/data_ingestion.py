import pandas as pd


class DataIngestion:

    def __init__(self, config):
        self.config = config
        self.raw_data = None

    def load_data(self):
        self.raw_data = pd.read_csv(
            self.config["data"]["raw_data_path"]
        )

        return self.raw_data