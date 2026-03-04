import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier

from preprocess import preprocess_data
from settings import DATADIR, MODELDIR

if __name__ == "__main__":
    df = pd.read_csv(f"{DATADIR}/WA_Fn-UseC_-HR-Employee-Attrition.csv")
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

    xgb = XGBClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.05,
        eval_metric="logloss",
        random_state=42,
    )
    xgb.fit(X_train_bal, y_train_bal)

    xgb.save_model(f"{MODELDIR}/xgb_model.ubj")
    joblib.dump((X_test, y_test), f"{DATADIR}/test_data.pkl")
