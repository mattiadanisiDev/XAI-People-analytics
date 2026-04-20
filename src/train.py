import os
import joblib
import pandas as pd
from dotenv import load_dotenv
from sklearn.model_selection import (
    train_test_split,
    RandomizedSearchCV,
    StratifiedKFold,
)
from sklearn.metrics import f1_score, classification_report, roc_auc_score
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
from xgboost import XGBClassifier

from preprocess import preprocess_data

load_dotenv()

DATADIR = os.getenv("DATADIR")
MODELDIR = os.getenv("MODELDIR")


if __name__ == "__main__":
    df = pd.read_csv(f"{DATADIR}/WA_Fn-UseC_-HR-Employee-Attrition.csv")
    df = preprocess_data(
        df=df,
        drop_columns=[
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
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    # --- Hyperparameter search space ---
    param_grid = {
        "n_estimators": [100, 200, 300, 500, 700],
        "max_depth": [3, 4, 5, 6, 7, 8],
        "learning_rate": [0.01, 0.03, 0.05, 0.08, 0.1, 0.15],
        "subsample": [0.6, 0.7, 0.8, 0.9, 1.0],
        "colsample_bytree": [0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
        "min_child_weight": [1, 2, 3, 5, 7],
        "gamma": [0, 0.05, 0.1, 0.2, 0.3],
        "reg_alpha": [0, 0.001, 0.01, 0.1, 1.0],
        "reg_lambda": [0.5, 1.0, 1.5, 2.0, 3.0],
    }

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    N_ITER = 150

    # ==========================================
    # Strategy 1: SMOTE inside CV (no leakage)
    # ==========================================
    print("=" * 60)
    print("Strategy 1: SMOTE (inside CV pipeline) + RandomizedSearchCV")
    print("=" * 60)

    smote_pipeline = ImbPipeline(
        [
            ("smote", SMOTE(random_state=42)),
            ("xgb", XGBClassifier(eval_metric="logloss", random_state=42)),
        ]
    )

    # Prefix param names with "xgb__" for the pipeline step
    smote_param_grid = {f"xgb__{k}": v for k, v in param_grid.items()}

    search_smote = RandomizedSearchCV(
        smote_pipeline,
        smote_param_grid,
        n_iter=N_ITER,
        scoring="f1",
        cv=cv,
        random_state=42,
        n_jobs=-1,
        verbose=1,
    )
    search_smote.fit(X_train, y_train)

    model_smote = search_smote.best_estimator_.named_steps["xgb"]
    cv_f1_smote = search_smote.best_score_

    # ==========================================
    # Strategy 2: scale_pos_weight (native)
    # ==========================================
    print()
    print("=" * 60)
    print("Strategy 2: scale_pos_weight + RandomizedSearchCV")
    print("=" * 60)

    neg = (y_train == 0).sum()
    pos = (y_train == 1).sum()
    spw = neg / pos

    xgb_spw = XGBClassifier(
        eval_metric="logloss",
        random_state=42,
        scale_pos_weight=spw,
    )
    search_spw = RandomizedSearchCV(
        xgb_spw,
        param_grid,
        n_iter=N_ITER,
        scoring="f1",
        cv=cv,
        random_state=42,
        n_jobs=-1,
        verbose=1,
    )
    search_spw.fit(X_train, y_train)

    model_spw = search_spw.best_estimator_
    cv_f1_spw = search_spw.best_score_

    # ==========================================
    # Evaluate both on held-out test set
    # ==========================================
    print()
    print("=" * 60)
    print("Test Set Evaluation")
    print("=" * 60)

    results = []
    for label, model, cv_f1 in [
        ("SMOTE", model_smote, cv_f1_smote),
        ("scale_pos_weight", model_spw, cv_f1_spw),
    ]:
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]
        test_f1 = f1_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_proba)
        results.append((label, model, test_f1, auc))
        print(f"\n--- {label} (CV F1={cv_f1:.4f}) ---")
        print(f"  AUC-ROC: {auc:.4f}  |  F1: {test_f1:.4f}")
        print(
            classification_report(
                y_test, y_pred, target_names=["Stayed", "Left"]
            )
        )

    # --- Pick the best strategy by test-set F1 ---
    best_label, best_model, best_f1, best_auc = max(
        results, key=lambda r: r[2]
    )
    print(f"Winner: {best_label}  (F1={best_f1:.4f}, AUC-ROC={best_auc:.4f})")

    # Save appropriate training data for LIME/SHAP background
    if best_label == "SMOTE":
        smote = SMOTE(random_state=42)
        X_train_save, y_train_save = smote.fit_resample(X_train, y_train)
    else:
        X_train_save, y_train_save = X_train, y_train

    # --- Save artifacts ---
    booster = best_model.get_booster()
    booster.save_model(fname=f"{MODELDIR}/xgb_model.ubj")
    joblib.dump((X_test, y_test), f"{DATADIR}/test_data.pkl")
    joblib.dump((X_train_save, y_train_save), f"{DATADIR}/train_data.pkl")

    print(f"\nModel saved to {MODELDIR}/xgb_model.ubj")
    print(f"Test data saved to {DATADIR}/test_data.pkl")
    print(f"Train data saved to {DATADIR}/train_data.pkl")
    print(f"Best params: {best_model.get_params()}")
