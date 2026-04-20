In base ai documenti forniti, ecco le risposte dettagliate ai punti della tua ricerca sul framework **SHAP (SHapley Additive exPlanation)**:

### 1. Valori di Shapley e Adattamento al Machine Learning
I **valori di Shapley** hanno origine nella **teoria dei giochi cooperativi** e sono nati per assegnare equamente il merito ai "giocatori" (le feature) in un "gioco" (la previsione del modello).
*   **Nel Machine Learning:** SHAP adatta questo concetto visualizzando ogni previsione del modello come un gioco in cui le feature collaborano per spostare la previsione dal valore medio di base al valore finale calcolato.
*   **Meccanismo:** SHAP assegna a ogni feature un valore di importanza per una specifica previsione, basato sul cambiamento dell'aspettativa condizionata del modello quando quella feature viene inclusa.

### 2. Proprietà Formali (Assiomi) e Affidabilità
Il framework SHAP identifica una classe di metodi chiamati **"metodi di attribuzione additiva delle feature"** e dimostra che esiste un'unica soluzione in questa classe che soddisfa tre proprietà fondamentali:

*   **Accuratezza Locale (Local Accuracy):** Corrisponde all'additività o efficienza. Richiede che la somma delle attribuzioni delle feature ($\phi_i$) e del valore di base ($\phi_0$) sia uguale all'output del modello originale $f(x)$ per quell'input specifico. In altre parole, la spiegazione deve "sommare" correttamente al risultato finale.
*   **Assenza (Missingness):** Se una feature è mancante nell'input originale, il suo impatto attribuito deve essere zero.
*   **Consistenza (Consistency):** Se un modello cambia in modo che il contributo di una feature aumenti o rimanga uguale indipendentemente dagli altri input, l'attribuzione di quella feature non deve diminuire.

Queste proprietà sono cruciali perché garantiscono che le spiegazioni siano **uniche** e **allineate con l'intuizione umana**, evitando comportamenti imprevedibili presenti in altri metodi che violano questi assiomi.

### 3. TreeExplainer e Ottimizzazioni per Modelli ad Albero
**Nota importante:** I documenti forniti *non menzionano esplicitamente il nome "TreeExplainer"*, che è stato sviluppato successivamente dagli stessi autori. Tuttavia, i testi trattano ampiamente le **approssimazioni specifiche per tipo di modello** per migliorare l'efficienza rispetto al calcolo esatto, che avrebbe una complessità esponenziale ($2^M$).
*   Le fonti citano il metodo **Max SHAP**, un'ottimizzazione che permette di calcolare i valori di Shapley per funzioni "max" (comuni negli alberi e nel pooling) in tempo $O(M^2)$ invece di $O(M 2^M)$.
*   I documenti mostrano esperimenti su **modelli ad albero** (come i decision tree), evidenziando che i metodi SHAP sono più efficienti in termini di campionamento e più accurati rispetto a metodi come LIME o il semplice campionamento di Shapley.

### 4. Spiegazioni Locali vs. Globali
*   **SHAP Locale:** Il framework si concentra principalmente sulla spiegazione di una **singola previsione** $f(x)$. Attribuisce un valore $\phi_i$ a ogni feature per mostrare quanto abbia contribuito a quel particolare risultato.
*   **SHAP Globale:** Sebbene i documenti forniti si focalizzino sul calcolo locale, presentano SHAP come una **misura unificata dell'importanza delle feature**.
*   **Passaggio:** Le fonti suggeriscono che, integrando le informazioni locali su più campioni (come mostrato nei test di efficienza su dataset densi e sparsi), si possa ottenere una visione globale della discriminazione delle classi da parte del modello.

### 5. Limiti e Criticità di SHAP
Sebbene SHAP sia presentato come superiore ad altri metodi, i documenti ne evidenziano alcune criticità:
*   **Complessità Computazionale:** Il calcolo esatto dei valori di Shapley è **impegnativo**. Anche con Kernel SHAP, sono necessari molti campionamenti per ottenere stime accurate, specialmente per modelli complessi.
*   **Assunzione di Indipendenza delle Feature:** Molte approssimazioni computazionali di SHAP (come quelle usate in Kernel SHAP o Linear SHAP) assumono l'**indipendenza delle feature** o la linearità del modello per semplificare il calcolo delle aspettative condizionate. Se le feature sono fortemente correlate, queste assunzioni potrebbero non riflettere perfettamente la realtà del modello.
*   **Approssimazioni Necessarie:** Poiché la maggior parte dei modelli non può gestire pattern arbitrari di valori mancanti, SHAP deve **approssimare** l'assenza di una feature integrando sulla sua distribuzione (aspettativa condizionata), il che introduce un livello di approssimazione rispetto al valore teorico puro.