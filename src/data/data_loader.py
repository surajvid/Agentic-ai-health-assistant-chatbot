import pandas as pd
from pathlib import Path


class DataLoader:
    """
    DataLoader handles loading structured datasets from the project's data folder.

    Supported formats:
        - CSV (.csv)
        - Excel (.xlsx)
        - Excel Macro-enabled (.xlsm)

    Always returns a pandas DataFrame.
    """

    def __init__(self, data_dir: str = "data"):
        """
        Initialize loader with data directory.
        """
        self.data_dir = Path(data_dir)

        if not self.data_dir.exists():
            raise FileNotFoundError(
                f"Data directory does not exist: {self.data_dir}"
            )

    def load_file(self, file_name: str, sheet_name: int | str = 0) -> pd.DataFrame:
        """
        Load dataset depending on file type.

        Parameters
        ----------
        file_name : str
            Name of the dataset file.
        sheet_name : int | str
            Excel sheet to load (default = first sheet).

        Returns
        -------
        pd.DataFrame
        """

        file_path = self.data_dir / file_name

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        suffix = file_path.suffix.lower()

        try:

            if suffix == ".csv":

                df = pd.read_csv(file_path)

            elif suffix in [".xlsx", ".xlsm"]:

                # Load only the specified sheet to avoid dict return
                df = pd.read_excel(
                    file_path,
                    sheet_name=sheet_name,
                    engine="openpyxl"
                )

            else:
                raise ValueError(f"Unsupported file format: {suffix}")

        except Exception as e:
            raise RuntimeError(
                f"Error loading file {file_name}: {str(e)}"
            )

        if df is None or df.empty:
            raise ValueError(f"Loaded dataset is empty: {file_name}")

        return df

    def list_available_files(self) -> list:
        """
        List available dataset files in the data directory.
        """
        return [
            file.name
            for file in self.data_dir.iterdir()
            if file.is_file()
        ]

    def preview_dataset(self, file_name: str, rows: int = 5) -> pd.DataFrame:
        """
        Quick preview of dataset.
        """
        df = self.load_file(file_name)
        return df.head(rows)