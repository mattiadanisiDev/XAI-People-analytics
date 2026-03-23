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

### Download del dataset

1. Accedere a [Kaggle — IBM HR Analytics](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset)
2. Scaricare il file `WA_Fn-UseC_-HR-Employee-Attrition.csv`
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