import os
import warnings

warnings.filterwarnings("ignore")
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import shap
import streamlit as st
from dotenv import load_dotenv
from xgboost import XGBClassifier
import tensorflow as tf

tf.compat.v1.disable_eager_execution()
from alibi.explainers import CounterfactualProto

load_dotenv()
MODELDIR = os.getenv("MODELDIR", "models")
DATADIR = os.getenv("DATADIR", "data")

# ---------------------------------------------------------------------------
# Risorse caricate una sola volta all'avvio
# ---------------------------------------------------------------------------


@st.cache_resource
def load_artifacts():
    model = XGBClassifier()
    model.load_model(os.path.join(MODELDIR, "xgb_model.ubj"))
    X_train, y_train = joblib.load(os.path.join(DATADIR, "train_data.pkl"))
    X_test, y_test = joblib.load(os.path.join(DATADIR, "test_data.pkl"))
    explainer = shap.TreeExplainer(model)
    return model, X_train, X_test, y_test, explainer


def _build_cf_explainer(_model, _X_train):
    """CounterfactualProto — costruito una sola volta e salvato in session_state."""

    def predict_fn(X):
        return _model.predict_proba(X)

    feature_range = (
        _X_train.values.min(axis=0).astype(np.float32),
        _X_train.values.max(axis=0).astype(np.float32),
    )
    cf = CounterfactualProto(
        predict=predict_fn,
        shape=(1, _X_train.shape[1]),
        kappa=0.1,
        beta=0.1,
        gamma=100.0,
        theta=10.0,
        use_kdtree=True,
        max_iterations=500,
        feature_range=feature_range,
        c_init=1.0,
        c_steps=5,
    )
    cf.fit(_X_train.values.astype(np.float32))
    return cf, predict_fn


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

FEATURE_LABELS_IT = {
    "Age": "Età",
    "DailyRate": "Retribuzione giornaliera",
    "DistanceFromHome": "Distanza da casa (km)",
    "Education": "Livello di istruzione",
    "EnvironmentSatisfaction": "Soddisfazione ambientale",
    "HourlyRate": "Retribuzione oraria",
    "JobInvolvement": "Coinvolgimento nel lavoro",
    "JobLevel": "Livello professionale",
    "JobSatisfaction": "Soddisfazione lavorativa",
    "MonthlyIncome": "Reddito mensile (€)",
    "MonthlyRate": "Tariffa mensile",
    "NumCompaniesWorked": "Aziende precedenti",
    "OverTime_Yes": "Straordinari",
    "PercentSalaryHike": "Aumento salariale (%)",
    "RelationshipSatisfaction": "Soddisfazione relazionale",
    "StockOptionLevel": "Stock option",
    "TotalWorkingYears": "Anni di esperienza totali",
    "TrainingTimesLastYear": "Formazioni nell'ultimo anno",
    "WorkLifeBalance": "Equilibrio vita-lavoro",
    "YearsAtCompany": "Anni in azienda",
    "YearsInCurrentRole": "Anni nel ruolo attuale",
    "YearsSinceLastPromotion": "Anni dall'ultima promozione",
    "YearsWithCurrManager": "Anni con il manager attuale",
    "BusinessTravel_Travel_Frequently": "Trasferte frequenti",
    "BusinessTravel_Travel_Rarely": "Trasferte rare",
}

KEY_FEATURES = [
    "Age",
    "MonthlyIncome",
    "OverTime_Yes",
    "JobSatisfaction",
    "EnvironmentSatisfaction",
    "WorkLifeBalance",
    "YearsAtCompany",
    "YearsWithCurrManager",
    "BusinessTravel_Travel_Frequently",
    "TrainingTimesLastYear",
    "JobInvolvement",
    "DistanceFromHome",
    "StockOptionLevel",
    "NumCompaniesWorked",
]

SCALE_FEATURES = {
    "JobSatisfaction": (4, "/4"),
    "EnvironmentSatisfaction": (4, "/4"),
    "WorkLifeBalance": (4, "/4"),
    "RelationshipSatisfaction": (4, "/4"),
    "JobInvolvement": (4, "/4"),
    "JobLevel": (5, "/5"),
    "Education": (5, "/5"),
    "StockOptionLevel": (3, "/3"),
}
BINARY_FEATURES = {
    "OverTime_Yes",
    "BusinessTravel_Travel_Frequently",
    "BusinessTravel_Travel_Rarely",
    "Gender_Male",
}
CURRENCY_FEATURES = {"MonthlyIncome", "DailyRate", "HourlyRate", "MonthlyRate"}

CF_ACTION_OVERRIDES = {
    "OverTime_Yes": {-1: "Elimina o riduci gli straordinari"},
    "BusinessTravel_Travel_Frequently": {-1: "Riduci le trasferte frequenti"},
    "BusinessTravel_Travel_Rarely": {-1: "Riduci le trasferte"},
    "TrainingTimesLastYear": {+1: "Aumenta le sessioni di formazione annue"},
    "StockOptionLevel": {+1: "Aumenta il livello di stock option"},
    "MonthlyIncome": {+1: "Valuta un aumento retributivo"},
    "JobSatisfaction": {+1: "Intervento su soddisfazione lavorativa"},
    "EnvironmentSatisfaction": {+1: "Migliora l'ambiente di lavoro"},
    "WorkLifeBalance": {+1: "Supporta l'equilibrio vita-lavoro"},
    "JobInvolvement": {+1: "Aumenta il coinvolgimento nel progetto"},
    "YearsWithCurrManager": {+1: "Rafforza la relazione con il manager"},
}


def value_hint(feature_name: str, val: float) -> str:
    """Restituisce una stringa leggibile per il valore di una feature."""
    if feature_name in BINARY_FEATURES:
        return "Sì" if round(val) == 1 else "No"
    if feature_name in SCALE_FEATURES:
        _, unit = SCALE_FEATURES[feature_name]
        return f"{int(round(val))}{unit}"
    if feature_name in CURRENCY_FEATURES:
        return f"€{int(val):,}".replace(",", ".")
    if val == int(val):
        return str(int(val))
    return f"{val:.1f}"


def risk_label(prob: float) -> tuple[str, str]:
    """Restituisce (etichetta, colore) in base alla probabilità di abbandono."""
    if prob >= 0.7:
        return "🔴 Alto rischio", "red"
    elif prob >= 0.4:
        return "🟡 Rischio moderato", "orange"
    else:
        return "🟢 Basso rischio", "green"


def build_top_factors(
    sv, feature_names: list[str], instance_df: pd.DataFrame, n: int = 5
) -> list[dict]:
    """Estrae i top-n fattori SHAP ordinati per impatto assoluto."""
    shap_vals = sv.values  # shape (n_features,)
    idxs = np.argsort(np.abs(shap_vals))[::-1][:n]
    factors = []
    for rank, i in enumerate(idxs):
        feat = feature_names[i]
        sv_i = float(shap_vals[i])
        val = float(instance_df.iloc[0][feat])
        factors.append(
            {
                "rank": rank,
                "label_it": FEATURE_LABELS_IT.get(feat, feat),
                "value_hint": value_hint(feat, val),
                "direction": "risk" if sv_i > 0 else "prot",
            }
        )
    return factors


def action_text(
    feature_name: str, original_val: float, cf_val: float, delta: float
) -> str:
    """Restituisce una stringa d'azione italiana per un cambio controfattuale."""
    direction = +1 if delta > 0 else -1
    overrides = CF_ACTION_OVERRIDES.get(feature_name, {})
    if direction in overrides:
        return overrides[direction]
    verb = "Aumenta" if delta > 0 else "Riduci"
    return (
        f"{verb} {FEATURE_LABELS_IT.get(feature_name, feature_name).lower()}"
    )


def build_cf_table(
    original: np.ndarray,
    cf_arr: np.ndarray,
    feature_names: list[str],
    threshold: float = 0.05,
) -> pd.DataFrame:
    """Costruisce una tabella leggibile delle variazioni controfattuali (modalità tecnica)."""
    rows = []
    for i, feat in enumerate(feature_names):
        delta = float(cf_arr[i]) - float(original[i])
        if abs(delta) < threshold:
            continue
        orig_val = round(float(original[i]), 2)
        cf_val = round(float(cf_arr[i]), 2)
        if orig_val in (0.0, 1.0) and abs(cf_val - round(cf_val)) < 0.3:
            cf_val = round(cf_val)
        rows.append(
            {
                "Feature": FEATURE_LABELS_IT.get(feat, feat),
                "Valore attuale": orig_val,
                "Valore suggerito": cf_val,
                "Variazione": round(delta, 2),
            }
        )
    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values("Variazione", key=abs, ascending=False)
    return df


def build_cf_table_hr(
    original: np.ndarray,
    cf_arr: np.ndarray,
    feature_names: list[str],
    threshold: float = 0.05,
) -> pd.DataFrame:
    """Costruisce una tabella HR-friendly delle azioni consigliate."""
    rows = []
    for i, feat in enumerate(feature_names):
        delta = float(cf_arr[i]) - float(original[i])
        if abs(delta) < threshold:
            continue
        orig_val = float(original[i])
        cf_val = float(cf_arr[i])
        rows.append(
            {
                "Fattore": FEATURE_LABELS_IT.get(feat, feat),
                "Situazione attuale": value_hint(feat, orig_val),
                "Azione consigliata": action_text(
                    feat, orig_val, cf_val, delta
                ),
                "_abs_delta": abs(delta),
            }
        )
    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values("_abs_delta", ascending=False).drop(
            columns=["_abs_delta"]
        )
    return df


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

st.set_page_config(page_title="HR Attrition XAI", layout="wide")
st.title("Analisi del Rischio di Abbandono — HR People Analytics")

model, X_train, X_test, y_test, shap_explainer = load_artifacts()

# Sidebar
with st.sidebar:
    st.header("Seleziona un dipendente")
    idx = st.selectbox(
        "Indice nel set di test (0–293)",
        options=list(range(len(X_test))),
        index=214,
    )
    actual_label = "Ha lasciato" if y_test.iloc[idx] == 1 else "È rimasto"
    st.info(f"**Esito reale:** {actual_label}")

    st.divider()
    tech_mode = st.toggle(
        "🔬 Modalità tecnica",
        value=False,
        help="Mostra spiegazioni SHAP e valori numerici dettagliati",
    )

if tech_mode:
    st.caption(
        "Strumento di supporto decisionale basato su XGBoost + SHAP + Alibi"
    )
else:
    st.caption(
        "Strumento di supporto decisionale per la gestione del personale"
    )

instance_df = X_test.iloc[[idx]]
instance_arr = instance_df.values.astype(np.float32)
prob_left = float(model.predict_proba(instance_arr)[0][1])
label, color = risk_label(prob_left)

# Pre-compute SHAP values (needed in both modes)
shap_values = shap_explainer(instance_df)
sv = shap_values[..., 1] if shap_values.values.ndim == 3 else shap_values

# ---------------------------------------------------------------------------
# Tab layout
# ---------------------------------------------------------------------------

if tech_mode:
    tab1, tab2 = st.tabs(["📊 Previsione e SHAP", "🔄 Cosa cambierebbe?"])
else:
    tab1, tab2 = st.tabs(["📊 Analisi del rischio", "🔄 Azioni consigliate"])

# ── Tab 1 ───────────────────────────────────────────────────────────────────
with tab1:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Probabilità di abbandono")
        metric_label = "P(Lascia)" if tech_mode else "Rischio di abbandono"
        st.metric(label=metric_label, value=f"{prob_left:.1%}")
        st.markdown(f"**{label}**")

        st.subheader("Profilo del dipendente")
        available = [f for f in KEY_FEATURES if f in X_test.columns]
        profile = instance_df[available].T.rename(
            columns={instance_df.index[0]: "Valore"}
        )
        profile.index = [FEATURE_LABELS_IT.get(f, f) for f in available]
        st.dataframe(profile, use_container_width=True)

    with col2:
        if tech_mode:
            st.subheader("Spiegazione SHAP — contributo delle feature")
            fig, ax = plt.subplots(figsize=(8, 6))
            shap.plots.waterfall(sv[0], max_display=15, show=False)
            st.pyplot(plt.gcf(), use_container_width=True)
            plt.close()
            st.caption(
                "Le barre rosse aumentano il rischio di abbandono; "
                "le barre blu lo riducono. "
                "Il valore f(x) è il log-odds della previsione."
            )
        else:
            st.subheader("Principali fattori che influenzano il rischio")
            factors = build_top_factors(
                sv[0], X_test.columns.tolist(), instance_df, n=5
            )

            # Impact labels based on rank within top-5
            n = len(factors)
            impact_labels = []
            for rank in range(n):
                tercile = rank / max(n - 1, 1)
                if tercile < 0.34:
                    impact_labels.append("alto impatto")
                elif tercile < 0.67:
                    impact_labels.append("medio impatto")
                else:
                    impact_labels.append("lieve impatto")

            risk_factors = [f for f in factors if f["direction"] == "risk"]
            prot_factors = [f for f in factors if f["direction"] == "prot"]

            lines = []
            if risk_factors:
                lines.append("**🔴 Fattori di rischio**")
                for i, f in enumerate(risk_factors):
                    impact = impact_labels[factors.index(f)]
                    lines.append(
                        f"&nbsp;&nbsp;{i+1}. 🔴 **{f['label_it']}** — {f['value_hint']} &nbsp;*({impact})*"
                    )
            if prot_factors:
                if lines:
                    lines.append("")
                lines.append("**🟢 Fattori protettivi**")
                offset = len(risk_factors)
                for i, f in enumerate(prot_factors):
                    impact = impact_labels[factors.index(f)]
                    lines.append(
                        f"&nbsp;&nbsp;{offset+i+1}. 🟢 **{f['label_it']}** — {f['value_hint']} &nbsp;*({impact})*"
                    )

            st.markdown("\n\n".join(lines))

# ── Tab 2 ───────────────────────────────────────────────────────────────────
with tab2:
    if prob_left < 0.5:
        st.success(
            "Rischio basso — questo dipendente non è classificato a rischio di abbandono. "
            "Nessun controfattuale necessario."
        )
    else:
        if tech_mode:
            st.subheader("Modifiche minime per invertire la previsione")
            st.write(
                "La tabella mostra le variazioni minime al profilo del dipendente "
                "che porterebbero il modello a prevedere **Rimane** anziché Lascia."
            )
        else:
            st.subheader("Azioni consigliate per ridurre il rischio")
            st.write(
                "La tabella indica le aree di intervento prioritarie per ridurre "
                "il rischio che il dipendente lasci l'azienda."
            )

        if "cf_explainer" not in st.session_state:
            cf, fn = _build_cf_explainer(model, X_train)
            st.session_state.cf_explainer = cf
            st.session_state.cf_predict_fn = fn
        cf_explainer = st.session_state.cf_explainer
        predict_fn = st.session_state.cf_predict_fn

        with st.spinner(
            "Calcolo del controfattuale in corso (può richiedere ~30 secondi)…"
        ):
            explanation = cf_explainer.explain(instance_arr, target_class=[0])

        if explanation.cf is None:
            st.warning(
                "Il modello non ha trovato un controfattuale entro le iterazioni massime. "
                "Prova con un altro dipendente."
            )
        else:
            cf_arr = explanation.cf["X"][0]
            prob_cf = float(predict_fn(explanation.cf["X"])[0][1])

            col_a, col_b = st.columns(2)
            if tech_mode:
                col_a.metric("P(Lascia) originale", f"{prob_left:.1%}")
                col_b.metric(
                    "P(Lascia) controfattuale",
                    f"{prob_cf:.1%}",
                    delta=f"{prob_cf - prob_left:.1%}",
                    delta_color="inverse",
                )
            else:
                col_a.metric("Rischio attuale", f"{prob_left:.1%}")
                col_b.metric(
                    "Rischio dopo le azioni",
                    f"{prob_cf:.1%}",
                    delta=f"{prob_cf - prob_left:.1%}",
                    delta_color="inverse",
                )

            if tech_mode:
                delta_df = build_cf_table(
                    instance_arr[0], cf_arr, X_test.columns.tolist()
                )
                if delta_df.empty:
                    st.info("Nessuna variazione significativa trovata.")
                else:
                    st.dataframe(
                        delta_df, use_container_width=True, hide_index=True
                    )
                    st.caption(
                        "⚠️ I valori frazionari su feature binarie (es. 0,2 invece di 0) "
                        "sono artefatti dell'ottimizzatore — interpretali come indicatori "
                        "di direzione, non come valori esatti."
                    )
            else:
                hr_df = build_cf_table_hr(
                    instance_arr[0], cf_arr, X_test.columns.tolist()
                )
                if hr_df.empty:
                    st.info("Nessuna variazione significativa trovata.")
                else:
                    st.dataframe(
                        hr_df, use_container_width=True, hide_index=True
                    )
