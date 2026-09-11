from pathlib import Path
import pandas as pd


class DataDownload:

    def __init__(self, config):
        self.config = config

    def download_data(self):
        """
        Download the Telco Customer Churn dataset and save it in the raw data folder.
        """

        url = (
            "https://raw.githubusercontent.com/"
            "blastchar/telco-customer-churn/"
            "master/WA_Fn-UseC_-Telco-Customer-Churn.csv"
        )

        raw_data_path = Path(
            self.config["data"]["raw_data_path"]
        )

        # Create data/raw folder if it does not exist
        raw_data_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        # Download CSV directly into a DataFrame
        data = pd.read_csv(url)

        # Save the raw data locally
        data.to_csv(
            raw_data_path,
            index=False
        )

        print(f"Data downloaded successfully to: {raw_data_path}")

        return raw_data_path



if __name__ == "__main__":

    config = {
        "data": {
            "raw_data_path": "data/raw/telco_churn.csv"
        }
    }

    downloader = DataDownload(config)

    downloader.download_data()