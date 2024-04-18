import pandas as pd
from icecream import ic

def read_parquet(s3_path):
    df = pd.read_parquet(s3_path)
    column_names = df.columns.tolist()
    ic(column_names)