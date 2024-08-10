import pandas as pd

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    # Example preprocessing
    df['processed_column'] = df['original_column'].apply(lambda x: x * 2)
    return df
