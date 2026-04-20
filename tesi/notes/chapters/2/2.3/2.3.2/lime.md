Ecco le risposte alle tue domande, basate sui documenti forniti:

### **Domanda 1 — Meccanismo di base**

**LIME (Local Interpretable Model-agnostic Explanations)** funziona approssimando localmente il comportamento di un modello complesso (black box) con un modello interprete più semplice. Il processo si articola in tre fasi principali:

1.  **Perturbazione locale:** Per spiegare una singola istanza $x$, LIME utilizza una "rappresentazione interpretabile" $x'$ (ad esempio, un vettore binario che indica la presenza o assenza di parole in un testo o di super-pixel in un'immagine). Vengono generati campioni sintetici perturbati $z'$ selezionando casualmente elementi diversi da zero da $x'$.
2.  **Generazione dei campioni:** Questi campioni perturbati $z'$ vengono riportati alla loro rappresentazione originale $z$ per ottenere la previsione $f(z)$ dal modello black box, che funge da "etichetta" per l'addestramento del modello surrogato.
3.  **Costruzione del modello surrogato:** LIME addestra un modello interpretabile $g$ (tipicamente un modello lineare sparso) su questo dataset di campioni perturbati.

La **funzione obiettivo** che LIME ottimizza è:
$$\xi(x) = \text{argmin}_{g \in G} L(f, g, \pi_x) + \Omega(g)$$
Dove **$L(f, g, \pi_x)$** è una misura di quanto il modello $g$ sia infedele nel predire l'output del modello originale $f$ nella località definita da $\pi_x$, e **$\Omega(g)$** è una misura della complessità del modello (ad esempio, il numero di pesi non nulli) che deve essere mantenuta bassa per garantire l'interpretabilità.

### **Domanda 2 — Fedeltà locale e kernel**

La **"fedeltà locale"** è definita come la capacità di una spiegazione di corrispondere al comportamento del modello originale nelle immediate vicinanze dell'istanza analizzata. Viene misurata attraverso la perdita pesata $L$, che valuta l'errore del modello surrogato rispetto a quello originale sui campioni perturbati.

Il **kernel esponenziale** $\pi_x(z) = \exp(-D(x, z)^2/\sigma^2)$ è una funzione di prossimità che assegna un **peso maggiore ai campioni più vicini** all'istanza originale $x$ e un peso minore a quelli lontani. Questo assicura che il modello surrogato si concentri sull'apprendimento del comportamento locale del classificatore, ignorando le dinamiche globali troppo complesse.

Sebbene i testi non usino esplicitamente il termine matematico **R²**, essi indicano che la fedeltà può essere stimata sul set di campioni perturbati $Z$ e presentata all'utente per valutare quanto sia affidabile l'approssimazione lineare in quel punto specifico.

### **Domanda 3 — Model-agnostic**

LIME è **model-agnostic** perché tratta il modello originale come una **scatola nera**, ovvero non fa alcuna assunzione sulla sua struttura interna (non ha bisogno di conoscere gradienti o pesi) e interagisce con esso solo tramite input e output.

*   **Vantaggi:** Questa flessibilità permette di spiegare **qualsiasi tipo di modello** (passato, presente o futuro), come foreste casuali o reti neurali profonde, utilizzando lo stesso framework. Consente inoltre di confrontare modelli diversi tra loro sulla base delle stesse feature interpretabili.
*   **Svantaggi:** Trattare il modello come black box significa che se la rappresentazione interpretabile non è abbastanza potente (es. non può catturare il tono di un'immagine), LIME non potrà spiegare certi comportamenti. Inoltre, se il modello originale è **altamente non lineare** anche nella località della previsione, l'approssimazione lineare di LIME potrebbe non essere fedele.

### **Domanda 4 — Limiti e instabilità**

I principali limiti identificati sono:

*   **Instabilità delle spiegazioni:** Poiché LIME si basa sul **campionamento casuale** per esplorare la località, è possibile ottenere spiegazioni diverse per la stessa istanza se il numero di campioni non è sufficiente o se il rumore di campionamento è elevato.
*   **Sensibilità all'ampiezza del kernel:** La scelta del parametro $\sigma$ (ampiezza del kernel) definisce quanto deve essere grande la "località"; i parametri di LIME sono spesso scelti in modo euristico, e scelte diverse possono portare a comportamenti non intuitivi o violazioni della fedeltà.
*   **Limiti dell'approssimazione lineare:** LIME fallisce nel fornire spiegazioni fedeli quando il modello originale presenta **interazioni non lineari complesse** anche in un intorno ristretto dell'istanza.

### **Domanda 5 — Confronto con SHAP**

Lundberg e Lee dimostrano che LIME appartiene alla classe dei **metodi additivi di attribuzione delle feature**, dove la spiegazione è una funzione lineare di variabili binarie.

**SHAP (SHapley Additive exPlanations)** generalizza e corregge LIME nei seguenti modi:

1.  **Unicità della soluzione:** SHAP dimostra che esiste un'unica soluzione (i **valori di Shapley**) che soddisfa tre proprietà desiderabili: fedeltà locale (local accuracy), mancanza di impatto per feature assenti (missingness) e coerenza (consistency).
2.  **Correzione dei parametri:** SHAP evidenzia che LIME, usando parametri euristici per il kernel e la perdita, può violare la coerenza e la fedeltà locale.
3.  **Kernel SHAP:** SHAP introduce il **"Shapley Kernel"**, una specifica funzione di peso e di perdita che, se applicata all'interno del framework di regressione lineare di LIME, permette di recuperare esattamente i valori di Shapley, garantendo così una base teorica più solida e risultati più allineati con l'intuizione umana.