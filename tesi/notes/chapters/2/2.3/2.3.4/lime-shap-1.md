Il costo computazionale di **LIME** per una spiegazione locale non dipende dalla dimensione del dataset di addestramento originale, ma è determinato principalmente dal **tempo necessario per calcolare le previsioni del modello black-box ($f(x)$)** e dal **numero di campioni perturbati ($N$)**.

### Fattori che determinano il costo computazionale

1.  **Numero di campioni perturbati ($N$):** La complessità di LIME è direttamente proporzionale a $N$ perché l'algoritmo deve generare $N$ variazioni del dato originale e, per ognuna di esse, ottenere una previsione dal modello black-box. Ad esempio, negli esperimenti citati nelle fonti, è stato utilizzato un valore di $N = 5000$ o addirittura $N = 15000$ per ottenere le spiegazioni.
2.  **Complessità del modello black-box:** Sebbene LIME sia model-agnostic (tratti il modello come una scatola nera), il costo totale è influenzato dal tempo di inferenza del modello stesso.
    *   **Modelli semplici:** Spiegare una **Random Forest** con 1000 alberi utilizzando 5000 campioni può richiedere meno di **3 secondi** su un laptop standard.
    *   **Modelli complessi:** Spiegare una singola previsione di una rete neurale profonda come **Inception** (per immagini) può richiedere circa **10 minuti**, poiché il calcolo di $f(z)$ per ogni campione perturbato è molto più oneroso.
3.  **Addestramento del modello surrogato:** Oltre alle chiamate al modello black-box, LIME deve addestrare un modello interpretabile (come un modello lineare sparse tramite **K-Lasso**) sul nuovo dataset di $N$ campioni. Il tempo richiesto dipende dal metodo di selezione delle $K$ feature (Lasso, selezione in avanti o all'indietro).

### Confronto con Tree SHAP
Le fonti fornite **non contengono informazioni specifiche sul costo computazionale di Tree SHAP** né un confronto diretto tra il costo di LIME e quello di Tree SHAP per i modelli ad albero. I documenti si concentrano quasi esclusivamente sulla metodologia, l'accuratezza e la fedeltà locale di LIME, menzionando SHAP solo in riferimenti bibliografici o in contesti legati alla vulnerabilità agli attacchi avversari.

**Informazione non presente nelle fonti:** In generale, Tree SHAP è noto per essere un algoritmo ottimizzato specificamente per modelli basati su alberi che calcola i valori Shapley in tempo polinomiale, ma per confermare come si confronti esattamente con LIME in termini di efficienza su dati tabulari sarebbe necessario consultare documentazione esterna.