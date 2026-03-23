# 🧠 XAI per la People Analytics — Previsione del Turnover Aziendale

> Progetto di tesi triennale sull'utilizzo dell'Explainable AI (XAI) per supportare decisioni HR significative e trasparenti.

---

## 📌 Descrizione

Questo progetto applica tecniche di **Intelligenza Artificiale Spiegabile (XAI)** al problema della previsione del turnover aziendale (*employee attrition*). L'obiettivo non è solo prevedere se un dipendente lascerà l'azienda, ma **spiegare il perché** in modo comprensibile anche a figure non tecniche come i manager HR.

Il dataset utilizzato è il noto **IBM HR Analytics Employee Attrition & Performance**, disponibile su Kaggle.

---

## 🎯 Obiettivi

- Addestrare un modello predittivo black-box (XGBoost) per identificare dipendenti a rischio di abbandono
- Applicare framework XAI per spiegare le predizioni a livello globale e locale
- Confrontare diversi approcci di spiegazione (SHAP, LIME, Alibi)
- Fornire uno strumento concreto e utilizzabile dal personale HR tramite dashboard interattiva

---

## 🚀 Come eseguire il progetto

### Prerequisiti

- **Python 3.11+**
- **[UV](https://docs.astral.sh/uv/)** — package manager

### 1. Clonare il repository e installare le dipendenze

```bash
git clone https://github.com/mattiadanisiDev/XAI-People-analytics.git
cd XAI-People-Analytics
uv sync
```

### 2. Scaricare il dataset

1. Accedere a [Kaggle — IBM HR Analytics](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset)
2. Scaricare il file `WA_Fn-UseC_-HR-Employee-Attrition.csv`
3. Salvarlo nella cartella `data/`

### 3. Configurare le variabili d'ambiente

Creare un file `.env` nella root del progetto:

```
MODELDIR=models
DATADIR=data
```

### 4. Addestrare il modello

```bash
python src/train.py
```

Questo script esegue l'intera pipeline: preprocessing, bilanciamento con SMOTE, addestramento XGBoost e salvataggio degli artefatti:
- `models/xgb_model.ubj` — modello addestrato
- `data/train_data.pkl` — dati di training (post-SMOTE)
- `data/test_data.pkl` — dati di test

### 5. Eseguire i notebook

```bash
jupyter notebook notebooks/
```

I notebook vanno eseguiti in questo ordine:

| # | Notebook | Descrizione |
|---|----------|-------------|
| 1 | `eda.ipynb` | Analisi esplorativa del dataset |
| 2 | `shap_explanation.ipynb` | Spiegazioni SHAP globali e locali |
| 3 | `lime_explanations.ipynb` | Spiegazioni LIME locali e confronto con SHAP |
| 4 | `alibi_counterfactuals.ipynb` | Analisi controfattuale ("cosa dovrebbe cambiare?") |

### 6. Avviare la dashboard interattiva

```bash
streamlit run src/dashboard.py
```

La dashboard si apre su `http://localhost:8501` e permette di:
- Selezionare un dipendente dal test set
- Visualizzare la probabilità di abbandono e i principali fattori di rischio
- Generare spiegazioni SHAP (modalità tecnica) o fattori leggibili (modalità HR)
- Calcolare controfattuali Alibi con azioni consigliate

---

## 🧩 Framework XAI utilizzati

| Framework | Utilizzo nel progetto |
|---|---|
| **SHAP** | Spiegazioni globali (quali feature guidano il turnover) e locali (perché questo dipendente è a rischio) |
| **LIME** | Spiegazioni locali model-agnostic, confronto con SHAP |
| **Alibi** | Spiegazioni controfattuali ("cosa dovrebbe cambiare perché il dipendente non sia più a rischio?") |

---

## 📊 Risultati principali

[Completare a fine progetto]

---

## 📚 Riferimenti

- [IBM HR Dataset — Kaggle](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset)
- [SHAP — Lundberg & Lee, 2017](https://github.com/slundberg/shap)
- [LIME — Ribeiro et al., 2016](https://github.com/marcotcr/lime)
- [Alibi — Seldon](https://github.com/SeldonIO/alibi)