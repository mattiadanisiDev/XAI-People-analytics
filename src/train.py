import pandas as pd
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

from preprocess import preprocess_data


if __name__ == "__main__":
    df = pd.read_csv("data/WA_Fn-UseC_-HR-Employee-Attrition.csv")
    df = preprocess_data(
        df=df,
        useless_columns=[
            "EmployeeCount",
            "Over18",
            "StandardHours",
            "EmployeeNumber",
        ],
        boolean_columns=["Attrition"],
    )

    X = df.drop(columns=["Attrition"])
    y = df["Attrition"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    smote = SMOTE(random_state=42)
    X_train_bal, y_train_bal = smote.fit_resample(X_train, y_train)

    print(y_train_bal.value_counts())
