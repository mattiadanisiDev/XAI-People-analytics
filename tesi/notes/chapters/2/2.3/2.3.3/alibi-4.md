FONTE: vanlooveren2021counterfactualproto + wachter2017counterfactual

DOMANDE:
    •	Quali sono le proprietà desiderabili di un buon controfattuale secondo la letteratura? In particolare: validità, prossimità (proximity), sparsity, plausibilità/realismo (in-distribution), diversità, actionability.
	•	Quali sono i limiti principali delle spiegazioni controfattuali in generale e di CounterfactualProto in particolare? In particolare: problema della non unicità (Rashomon controfattuale), dipendenza dagli iperparametri, gestione di variabili categoriche e immutabili (es. età, genere), rischio di controfattuali non azionabili.

RISPOSTE:
In base alla letteratura fornita, le proprietà desiderabili e i limiti delle spiegazioni controfattuali, con un focus particolare su **CounterfactualProto**, possono essere così sintetizzati:

### 4. Proprietà desiderabili di un buon controfattuale

Secondo le fonti, un controfattuale di alta qualità deve soddisfare diverse proprietà chiave per essere utile ed efficace:

*   **Validità:** La previsione del modello sull'istanza controfattuale ($x_{cf}$) deve essere uguale o molto vicina all'**output desiderato** o alla classe target predefinita.
*   **Prossimità (Proximity):** Il controfattuale deve rappresentare il **minimo cambiamento possibile** rispetto all'istanza originale (il cosiddetto "mondo possibile più vicino"). Questo assicura che la spiegazione sia rilevante e non richieda sforzi eccessivi per essere raggiunta.
*   **Sparsità (Sparsity):** Le perturbazioni applicate devono modificare il **minor numero possibile di caratteristiche** (feature). Un controfattuale sparso è più facile da comprendere per un essere umano, poiché evidenzia solo i fattori critici per il cambiamento della decisione.
*   **Plausibilità/Realismo (In-distribution):** L'istanza generata deve essere **interpretabile**, il che significa che deve trovarsi vicino alla **distribuzione dei dati di addestramento** del modello. Se un controfattuale rispetta il "manifold" dei dati, evita di essere una soluzione "out-of-distribution" che, pur cambiando la previsione, risulta irrealistica (ad esempio, un'immagine di un numero che non somiglia a nessuna cifra reale).
*   **Diversità:** Poiché possono esistere diversi modi per ottenere lo stesso risultato, è desiderabile fornire un **insieme di controfattuali diversi** tra loro, offrendo all'utente più opzioni basate su vari "mondi vicini".
*   **Actionability (Azionabilità):** Le modifiche suggerite devono riguardare variabili che l'utente può **effettivamente cambiare**. Questo si ottiene spesso fissando le variabili immutabili (come l'etnia o l'età) ai loro valori originali durante il processo di ottimizzazione.

### 11. Limiti delle spiegazioni controfattuali e di CounterfactualProto

Nonostante i vantaggi, questa metodologia presenta diverse criticità:

*   **Problema della non unicità (Rashomon controfattuale):** Non esiste un unico controfattuale "corretto". Questa molteplicità di soluzioni può rendere difficile per un utente decidere quale percorso seguire e può portare a spiegazioni soggettive che dipendono dalla funzione di distanza scelta.
*   **Dipendenza dagli iperparametri:** Metodi come CounterfactualProto dipendono fortemente dalla calibrazione di vari parametri, come il peso della sparsità ($\beta$), il peso del termine del prototipo ($\theta$) o il numero di vicini ($K$ o $k$) per definire il prototipo stesso. Trovare l'intervallo corretto per questi iperparametri (ad esempio il parametro $c$ per la perdita di predizione) può essere **estremamente dispendioso in termini di tempo**.
*   **Gestione di variabili categoriche e immutabili:**
    *   **Categoriche:** Definire perturbazioni significative per dati categorici è complesso perché manca una nozione naturale di distanza o ordine. CounterfactualProto tenta di risolvere questo problema con embedding basati su metriche di distanza come ABDM o MVDM, ma questo aggiunge complessità al processo.
    *   **Immutabili:** Gli algoritmi standard spesso non distinguono tra variabili che l'utente può cambiare e quelle che non può cambiare (es. **genere, età, razza**). Se non vengono esplicitamente vincolate, il modello potrebbe suggerire cambiamenti assurdi, come "cambiare razza" per ottenere un prestito, rendendo la spiegazione inutile o eticamente problematica.
*   **Rischio di controfattuali non azionabili:** Se un controfattuale è molto sparso ma non tiene conto delle **interdipendenze causali** tra le variabili, potrebbe suggerire un cambiamento che è fisicamente o logicamente impossibile (ad esempio, aumentare il reddito senza cambiare la carriera).
*   **Limiti specifici di CounterfactualProto:** Sebbene i prototipi guidino la ricerca verso zone più interpretabili dello spazio dei dati, ciò può comportare un **trade-off con la sparsità**: le soluzioni guidate dai prototipi tendono a essere meno sparse rispetto a quelle che minimizzano solo la distanza $L_1$, poiché cercano di assomigliare a una distribuzione di classe reale. Inoltre, il metodo richiede l'accesso a un **encoder addestrato** o la costruzione di **alberi k-d** sull'intero dataset, il che richiede risorse computazionali aggiuntive.