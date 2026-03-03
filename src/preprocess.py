import pandas as pd


def preprocess_data(
    df: pd.DataFrame, useless_columns: list[str], boolean_columns: list[str]
) -> pd.DataFrame:
    df.drop(columns=useless_columns, inplace=True)

    for column in boolean_columns:
        df[column] = df[column].map({"Yes": 1, "No": 0})

    # One-hot encoding: converts text categories into binary columns (0/1) so
    # the model can do math on them.
    # e.g. Department["Sales", "R&D", "HR"] → Department_R&D, Department_HR
    # (Sales is the dropped reference)
    # drop_first=True removes one column per group to avoid redundancy
    # (if R&D=0 and HR=0, it must be Sales)
    categorical_cols = df.select_dtypes(include="object").columns.tolist()
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    return df
