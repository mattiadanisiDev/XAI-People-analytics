FONTE: miller2019explanation + wachter2017counterfactual

DOMANDE:
•	Che cosa si intende per spiegazione controfattuale nel contesto dell’Explainable AI? Qual è la formulazione concettuale del tipo “cosa dovrebbe cambiare affinché la predizione cambi?” e da quale origine filosofica/cognitiva deriva (es. Wachter, Mittelstadt, Russell 2017; Miller 2019)?
•	In che modo le spiegazioni controfattuali si collocano rispetto ad approcci come SHAP e LIME? In che senso sono considerate model-agnostic, locali e orientate all’azione (actionable)?

RISPOSTE:
Nel contesto dell’Explainable AI (XAI), una **spiegazione controfattuale** descrive quali fatti esterni dovrebbero cambiare affinché una decisione automatizzata possa produrre un risultato diverso, senza necessariamente rivelare la logica interna dell'algoritmo.

### 1. Definizione e Origini
La spiegazione controfattuale si presenta tipicamente nella forma: *"Ti è stato negato un prestito perché il tuo reddito era di 30.000€. Se il tuo reddito fosse stato di 45.000€, il prestito ti sarebbe stato concesso"*.

*   **Formulazione concettuale:** Il fulcro di questo approccio è il concetto di **"mondo possibile più vicino"** (*closest possible world*), ovvero identificare il cambiamento minimo necessario alle variabili di input affinché l'output cambi in modo desiderato. A differenza delle spiegazioni tradizionali che cercano di chiarire lo stato interno o la logica di un algoritmo, i controfattuali si concentrano sulla **dipendenza dai fatti esterni** che hanno portato a quella specifica decisione.
*   **Origini filosofiche e cognitive:**
    *   **Miller (2019):** Sottolinea che le spiegazioni umane sono intrinsecamente **contrastive**. Le persone non chiedono perché è accaduto l'evento P, ma perché è accaduto P invece di Q (dove Q è il *foil*, ovvero il caso di contrasto atteso). Miller attinge a filosofi come **Lipton** (1990) e **Hesslow** (1988) per definire la "condizione di differenza": spiegare P significa citare una differenza causale tra la storia di P e l'assenza di Q.
    *   **Wachter, Mittelstadt e Russell (2017/2018):** Collegano i controfattuali alla **storia filosofica della conoscenza**, in particolare alle condizioni modali di "sensibilità" (se P fosse falso, il soggetto non crederebbe a P) proposte da autori come Sosa e Nozick. Questo approccio si rifà alla teoria della causalità di **David Lewis** basata sui controfattuali.

### 2. Relazione con SHAP/LIME e Caratteristiche Chiave
Le spiegazioni controfattuali si distinguono nettamente da approcci come **LIME** (e per estensione SHAP) per il loro obiettivo e metodo.

*   **Rispetto a LIME/SHAP:** Mentre metodi come LIME generano **modelli locali semplificati** (approssimazioni lineari) per spiegare la logica interna di un modello complesso, i controfattuali non tentano di spiegare come il sistema "pensa". Le fonti evidenziano che i modelli locali possono essere instabili e difficili da interpretare per un profano; al contrario, il controfattuale fornisce solo l'informazione minima necessaria per alterare una decisione.
*   **Model-agnostic:** Sono considerate tali perché possono essere applicate a qualsiasi sistema di "black box" (reti neurali, SVM, ecc.) senza doverne conoscere i parametri interni o il funzionamento. Si basano esclusivamente sull'osservazione di come l'output varia al variare degli input.
*   **Locali:** Si riferiscono a **singole decisioni specifiche**. Non spiegano il comportamento globale del modello, ma chiariscono perché un individuo particolare ha ricevuto un determinato esito.
*   **Orientate all’azione (Actionable):** Sono progettate per aiutare il soggetto a **intraprendere azioni concrete**. Invece di limitarsi a far "capire", forniscono una guida su cosa l'utente può cambiare nel proprio comportamento o situazione (es. aumentare il reddito, ridurre le richieste) per ottenere il risultato desiderato in futuro. Questa caratteristica le rende particolarmente preziose in ambiti normativi come il **GDPR**, dove il diritto all'informativa mira a proteggere gli interessi del soggetto interessato.