class DataValidation:

    def __init__(self, required_columns, expected_dtypes):
        self.required_columns = required_columns
        self.expected_dtypes = expected_dtypes

    def check_empty_data(self, data):
        return data.empty

    def check_required_columns(self, data):

        missing_columns = [
            column
            for column in self.required_columns
            if column not in data.columns
        ]

        return missing_columns

    def check_duplicates(self, data):
        return data.duplicated().sum()

    def check_missing_values(self, data):
        return data.isnull().sum()

    def check_data_types(self, data):

        incorrect_dtypes = {}

        for column, expected_dtype in self.expected_dtypes.items():

            actual_dtype = str(data[column].dtype)

            if actual_dtype != expected_dtype:

                incorrect_dtypes[column] = {
                    "expected": expected_dtype,
                    "actual": actual_dtype
                }

        return incorrect_dtypes

    def validate_data(self, data):

        if self.check_empty_data(data):
            raise ValueError("Dataset is empty.")

        missing_columns = self.check_required_columns(data)

        incorrect_dtypes = self.check_data_types(data)

        duplicate_count = self.check_duplicates(data)

        missing_values = self.check_missing_values(data)

        validation_report = {
            "missing_columns": missing_columns,
            "incorrect_dtypes": incorrect_dtypes,
            "duplicate_count": duplicate_count,
            "missing_values": missing_values
        }

        return validation_report