# Outline della Tesi (compilativa, max 40 pagine)

# Explainable AI per HR People Analytics: SHAP, LIME e Controfattuali a confronto

---

## 1. Introduzione (~3 pagine)

### 1.1 Contesto e motivazione
- Il costo del turnover aziendale e la crescente rilevanza della People Analytics
- Perché un semplice modello black-box non è abbastanza e come la XAI può venire in nostro soccorso
- La necessità di spiegabilità per i non tecnici (manager HR)

### 1.2 Obiettivi della tesi
- Fornire un quadro teorico sull'XAI applicata alla previsione del turnover
- Confrontare tre framework XAI (SHAP, LIME, Alibi) attraverso un caso studio illustrativo
- Discutere quale approccio esplicativo è più adatto al contesto HR
---

## 2. Quadro teorico (~12 pagine)

*Cuore della tesi compilativa: rassegna della letteratura su People Analytics, ML e XAI.*

### 2.1 People Analytics e turnover
- Definizione di People Analytics e sua evoluzione nelle organizzazioni
- Fattori di attrition (soddisfazione, retribuzione, work-life balance, crescita professionale)
- Limiti degli approcci tradizionali (survey, exit interview) e vantaggi dei dati strutturati

### 2.2 Machine learning per la previsione del turnover

### 2.3 Explainable AI (XAI)
- Definizione
- Concetto di Interpretabilità
- caratteristiche di una buona spiegazione
- Quando la interpretabilità è importante e quando no
- differenza tra interpretability and explecability

#### 2.3.1 SHAP (SHapley Additive exPlanations)
- Fondamenti nella teoria dei giochi cooperativi (valori di Shapley)
- Proprietà formali: additività, consistenza, simmetria
- TreeExplainer: ottimizzazione per modelli ad albero

#### 2.3.2 LIME (Local Interpretable Model-agnostic Explanations)
- Perturbazione locale e modello surrogato lineare
- Fedeltà locale e limiti dell'approssimazione lineare
- Instabilità dovuta al campionamento casuale

#### 2.3.3 Spiegazioni controfattuali (Alibi CounterfactualProto)
- Definizione: "cosa dovrebbe cambiare affinché la predizione cambi?"
- Prototipi guidati (k-d tree) vs autoencoder
- Sparsity (L1) e plausibilità delle spiegazioni

#### 2.3.4 Confronto teorico SHAP e LIME
- Tabella sinottica: ambito (globale/locale), fedeltà, stabilità, velocità, interpretabilità, dipendenza dal modello

---

## 3. Caso studio illustrativo (~15 pagine)

*Il caso studio applica i concetti del Cap. 2 al dataset IBM HR. Non è un contributo sperimentale originale, ma una dimostrazione pratica su un benchmark noto.*

### 3.1 Dataset e setup
- IBM HR Employee Attrition dataset: 1.470 dipendenti, 35 feature, 16,1% attrition
- Analisi esplorativa: distribuzione delle classi, correlazioni tra feature di tenure
- Modello XGBoost con hyperparameter tuning (RandomizedSearchCV, 150 iterazioni, F1)
- Confronto SMOTE vs scale_pos_weight: vincitore scale_pos_weight

### 3.2 Performance del modello
- Metriche sul test set: Accuracy, Precision, Recall, F1-Score, AUC-ROC
- Matrice di confusione e curva ROC
- Ottimizzazione della soglia: default (0.50) vs soglia recall-focused
- Perché il recall conta più della precision nel contesto HR

### 3.3 Spiegazioni SHAP
- Importanza globale delle feature (summary plot)
- Tre casi studio locali:
  - Vero Positivo (Dip. 214): fattori di rischio cumulativi, profilo intervenibile
  - Falso Positivo (Dip. 223): il modello sovrastima i fattori retributivi
  - Falso Negativo (Dip. 240): limite del modello, fattori esterni non misurabili

### 3.4 Spiegazioni LIME
- Importanza globale aggregata (mean |LIME weight|)
- Stessi tre casi studio: confronto con le spiegazioni SHAP
- Concordanze e discordanze nel ranking delle feature

### 3.5 Analisi controfattuale (Alibi)
- Dip. 214: quali interventi avrebbero prevenuto l'abbandono (overtime, travel, manager tenure)
- Dip. 223: bias del modello verso nuovi assunti giovani, artefatti del controfattuale
- Leve azionabili vs fattori immutabili

### 3.6 Dashboard
- Panoramica sulla dashboard streamlit

---

## 4. Discussione (~5 pagine)

### 4.1 Sintesi dei risultati
- Il modello come strumento di supporto, non di sostituzione del giudizio HR
- L'XAI rende trasparente quando fidarsi del modello e quando no
- Confronto pratico dei tre framework: quale risponde a quale domanda
  - SHAP → "perché il modello ha deciso così?"
  - LIME → "quali regole semplici approssimano la decisione?"
  - Controfattuali → "cosa dovrebbe cambiare per un esito diverso?"

### 4.2 Limiti del caso studio
- Dataset sintetico (IBM): generalizzabilità limitata
- Dimensione ridotta (1.470 dipendenti, 237 attrition)
- Assenza di feature qualitative (clima organizzativo, leadership, offerte esterne)

### 4.3 Implicazioni per la pratica HR
- Come un manager HR può utilizzare questi strumenti
- Dalla predizione all'azione: il valore delle spiegazioni locali
- Considerazioni etiche: bias demografici, privacy, discriminazione algoritmica

---

## 5. Conclusioni e sviluppi futuri
### 5.1 Sviluppi futuri
- Applicazione su dati aziendali reali
- Integrazione di feature qualitative
- Estensione ad altri modelli per verificare la generalizzabilità delle spiegazioni XAI

---

## Regole di scrittura della tesi

Le seguenti regole si applicano a ogni contributo testuale alla tesi e non sono negoziabili:

1. **Nessun fatto senza fonte.** Qualsiasi affermazione sostantiva (dato, trend, definizione, fenomeno documentato in letteratura, riferimento normativo) deve essere accompagnata da una citazione. Se la fonte non è ancora disponibile, **non inventarla e non ometterla silenziosamente**: inserire nel testo un commento LaTeX del tipo `% CITE NEEDED: <descrizione breve di cosa serve citare>` e segnalare esplicitamente all'utente, nel messaggio di risposta, che è necessario reperire la fonte. L'utente provvederà a cercarla, fornirla e indicare dove inserirla.

2. **Tono generale, senza esempi numerici illustrativi.** Mantenere un registro argomentativo e generale. Evitare esempi inventati, percentuali di fantasia, nomi fittizi di dipendenti o scenari concreti che non siano tratti direttamente dalla letteratura o dal caso studio del Cap. 3. Formulazione corretta: *"l'informazione che un dipendente è ad alto rischio di dimissione risulta di scarsa utilità operativa se non si conoscono le leve su cui intervenire"*. Formulazione scorretta: *"sapere che un dipendente ha, ad esempio, il 78\% di probabilità di dimettersi..."*.

---

## Nota sulla formattazione della tesi

**Stile citazione**: **authortitle** (biblatex)
- Formato: Author (Year), "Title"
- Backend: biber
- Ordinamento: none (ordine di apparizione)
- File bibliografia: `biblio.bib`

Questo stile è stato scelto per fornire citazioni complete che includono sia l'autore che il titolo della fonte, facilitando l'identificazione rapida della letteratura nel contesto HR e XAI.

---

## Bibliografia

## appendice (~1 pagina)
- A. Elenco completo delle feature del dataset IBM HR
- B. Spazio degli iperparametri e configurazione del modello
