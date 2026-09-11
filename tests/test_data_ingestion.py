from src.utils.config import read_yaml
from src.components.data_ingestion import DataIngestion


# Load configuration
config = read_yaml("config.yaml")

# Create ingestion object
ingestion = DataIngestion(config)

# Load data
data = ingestion.load_data()


# Tests
assert data is not None
assert data.shape == (7043, 21)
assert "Churn" in data.columns
assert "customerID" in data.columns

print("All DataIngestion tests passed successfully.")