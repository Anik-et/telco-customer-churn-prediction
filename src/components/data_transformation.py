import pandas as pd


class DataTransformation:

    def transform(self, data):
        """
        Clean and transform raw data before feature engineering.
        """

        data = data.copy()

        # Convert TotalCharges to numeric.
        # Invalid/blank values become NaN.
        data["TotalCharges"] = pd.to_numeric( data["TotalCharges"], errors="coerce" )

        # Remove customer identifier.
        data.drop( columns=["customerID"], inplace=True )

        return data