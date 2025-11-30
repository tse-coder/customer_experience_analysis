# create a file loader object
import pandas as pd
class FileLoader:
    def __init__(self, file_path, df):
        self.file_path = file_path
        self.df = df

    def load(self):
        try:
            df = pd.read_csv(self.file_path)
            return df
        except FileNotFoundError as fn:
            print(fn)
            return None
        except Exception as e:
            print(e)
            return None
    def save(self):
        try:
            self.df.to_csv(self.file_path, index=False)
            print(f"reviews saved to {self.file_path}")
            return True
        except Exception as e:
            print(e)
            return False
    