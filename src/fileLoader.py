# create a file loader object
import pandas as pd
class FileLoader:
    def __init__(self, file_path):
        self.file_path = file_path

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
    