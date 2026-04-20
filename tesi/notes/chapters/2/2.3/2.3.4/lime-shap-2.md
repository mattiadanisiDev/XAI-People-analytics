Il costo computazionale di **LIME** (Local Interpretable Model-Agnostic Explanations) e il suo confronto con **Tree SHAP** possono essere riassunti attingendo principalmente a due studi autorevoli: l'analisi comparativa di **Doumard et al.** e lo studio tecnico di **Yang** sulla complessità di Tree SHAP.

### Costo computazionale di LIME
LIME presenta una **complessità lineare rispetto al numero di feature** presenti nel dataset. Il suo costo computazionale dipende dai seguenti fattori:

*   **Numero di campioni perturbati ($N$):** Per ogni istanza da spiegare, LIME genera un nuovo dataset di vicinato composto da $N$ campioni perturbati. Il tempo totale è proporzionale a $N$ poiché il modello black-box deve generare una previsione per ciascuno di questi punti. In contesti sperimentali, questo numero viene spesso fissato (ad esempio a $N=100$) per bilanciare precisione e tempi.
*   **Complessità del modello black-box:** L'esecuzione di LIME mostra una **variabilità inter-modello quasi nulla**; ciò significa che il tempo necessario per calcolare una spiegazione rimane costante indipendentemente dal fatto che il modello originale sia una Regressione Logistica, una SVM o una Random Forest. Tuttavia, il costo complessivo è influenzato dalla velocità di inferenza del modello originale, poiché deve essere interrogato migliaia di volte per i campioni perturbati.

### Confronto con Tree SHAP
Il confronto tra i due metodi evidenzia differenze strutturali profonde in termini di efficienza:

1.  **Dipendenza dalle feature:** Mentre il costo di LIME cresce linearmente con il numero di feature, **Tree SHAP ha un tempo di esecuzione costante**, indipendentemente dalla dimensionalità del dataset.
2.  **Complessità algoritmica:** Tree SHAP è ottimizzato specificamente per modelli ad albero (come Random Forest o XGBoost) e opera con una complessità di **$O(MTLD^2)$**, dove $M$ è il numero di campioni, $T$ il numero di alberi, $L$ il numero massimo di foglie e $D$ la profondità massima.
3.  **Efficienza relativa:**
    *   In **bassa dimensione** (poche feature), LIME è computazionalmente più costoso rispetto ad altri metodi, incluso Tree SHAP.
    *   In **alta dimensione**, Tree SHAP rimane estremamente rapido, specialmente nella sua versione "approx", che risulta essere l'explainer con il minor tempo di esecuzione per istanza.

In sintesi, per i modelli basati su alberi, **Tree SHAP è significativamente più efficiente di LIME**, poiché sfrutta la struttura interna del modello anziché basarsi su campionamenti perturbati esterni.

Ecco gli snippet **BibTeX** per citare le fonti principali utilizzate per elaborare il confronto tecnico tra **LIME** e **Tree SHAP** nella risposta precedente:

```bibtex
@inproceedings{doumard2022comparative,
  author    = {Doumard, Emmanuel and Aligon, Julien and Escriva, Elodie and Excoffier, Jean-Baptiste and Monsarrat, Paul and Soul{\'e}-Dupuy, Chantal},
  title     = {A comparative study of additive local explanation methods based on feature influences},
  booktitle = {Proceedings of the Workshop on Explainable and Interpretable Machine Learning (XIML)},
  year      = {2022},
  url       = {https://ceur-ws.org/Vol-3130/paper4.pdf}
}

@article{yang2021fast,
  author  = {Yang, Jilei},
  title   = {Fast TreeSHAP: Accelerating SHAP Value Computation for Trees},
  journal = {arXiv preprint arXiv:2109.09847},
  year    = {2021},
  url     = {https://arxiv.org/abs/2109.09847}
}

@mastersthesis{boccuto2022tecniche,
  author  = {Boccuto, Alessandra},
  title   = {Tecniche di explainability applicate a modelli predittivi in ambito didattico},
  school  = {Alma Mater Studiorum - Universit{\`a} di Bologna},
  year    = {2022},
  type    = {Tesi di Laurea Magistrale},
  url     = {https://amslaurea.unibo.it/}
}
```

### Dettagli sulle fonti utilizzate:
*   **Doumard et al. (2022):** Utilizzato per l'analisi comparativa dei tempi di esecuzione in base alla dimensionalità (numero di feature) e per la valutazione della precisione locale.
*   **Yang (2021):** Utilizzato per i dettagli sulla complessità algoritmica di Tree SHAP ($O(MTLD^2)$) e per le informazioni sulle varianti ottimizzate *Fast TreeSHAP* v1 e v2.
*   **Boccuto (2022):** Utilizzato per l'inquadramento teorico dei metodi additivi e per la descrizione delle modalità di applicazione su dati tabulari.