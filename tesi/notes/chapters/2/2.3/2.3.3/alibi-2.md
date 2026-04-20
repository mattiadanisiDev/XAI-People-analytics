FONTE: vanlooveren2021counterfactualproto

DOMANDE:
•	Che cosa si intende per plausibilità (o in-distribution-ness) di un controfattuale? Perché controfattuali fuori distribuzione sono considerati problematici, soprattutto in contesti applicativi come l’HR?
•	Cos’è l’algoritmo CounterfactualProto implementato nella libreria Alibi (Van Looveren & Klaise 2021, “Interpretable Counterfactual Explanations Guided by Prototypes”)? Qual è l’intuizione principale del metodo (guida verso un prototipo di classe)?
•	Com’è strutturata la funzione di perdita di CounterfactualProto? Quali termini la compongono (es. termine di predizione, distanza elastic net L1+L2, termine prototipo) e a cosa serve ciascuno?
•	Come vengono costruiti i prototipi di classe in CounterfactualProto? Qual è la differenza tra l’uso di un autoencoder (encoder latente) e l’uso di un k-d tree sullo spazio originale? Quando è preferibile un approccio rispetto all’altro (presenza/assenza di autoencoder addestrato, tipo di dati)?
•	Come il termine prototipo contribuisce a ottenere controfattuali più plausibili e a velocizzare la convergenza dell’ottimizzazione rispetto all’approccio base di Wachter?

RISPOSTE:
Ecco le risposte dettagliate basate sulle fonti fornite:

**6. Plausibilità (In-distribution-ness) e problematicità dei controfattuali fuori distribuzione**
Per **plausibilità** (o *in-distribution-ness*) di un controfattuale si intende la sua capacità di **risiedere vicino alla distribuzione dei dati di addestramento del modello**. Un'istanza è considerata interpretabile non solo se rispetta la distribuzione generale del dataset, ma soprattutto se è vicina alle istanze di addestramento appartenenti alla sua **classe controfattuale** specifica. I controfattuali **fuori distribuzione** sono considerati problematici perché, pur portando a un cambiamento nella previsione, possono risultare **poco interpretabili o non realistici**. Ad esempio, in un modello di valutazione immobiliare, aumentare il numero di stanze senza cambiare la metratura potrebbe portare a una valutazione più alta, ma risulterebbe in una casa "fuori distribuzione" rispetto alle case costose reali, che solitamente hanno anche metrature più ampie. Sebbene le fonti non citino esplicitamente il settore HR (Risorse Umane), si può dedurre che in tale ambito controfattuali fuori distribuzione potrebbero suggerire cambiamenti di carriera o profili professionali impossibili o privi di senso logico nel mondo reale.

**7. L'algoritmo CounterfactualProto e la sua intuizione principale**
**CounterfactualProto** è un metodo agnostico rispetto al modello, implementato nella libreria **Alibi**, progettato per trovare spiegazioni controfattuali interpretabili utilizzando i **prototipi di classe**. L'intuizione principale del metodo è quella di **guidare le perturbazioni** delle caratteristiche dell'istanza originale verso un controfattuale che non solo modifichi la previsione del modello, ma che ricada all'interno della distribuzione della classe target desiderata. Utilizzando i prototipi come "ancore" nel processo di ottimizzazione, l'algoritmo assicura che il risultato sia rappresentativo di un'istanza tipica di quella classe.

**8. Struttura della funzione di perdita di CounterfactualProto**
La funzione di perdita $L$ è strutturata per bilanciare diversi obiettivi contemporaneamente:
*   **Termine di predizione ($L_{pred}$):** Incoraggia il modello a prevedere per l'istanza perturbata una classe diversa da quella originale.
*   **Distanza Elastic Net ($L_1 + L_2$):** Minimizza la differenza tra l'istanza originale ($x_0$) e quella controfattuale ($x_{cf}$) per garantire che le modifiche siano **sparse** (poche caratteristiche cambiate) e non eccessive.
*   **Termine Prototipo ($L_{proto}$):** Riduce la distanza tra l'istanza controfattuale e il prototipo della classe target, guidando la soluzione verso una zona dello spazio delle caratteristiche che sia **interpretabile e in-distribution**.
*   **Termine Autoencoder ($L_{AE}$ - opzionale):** Penalizza i controfattuali che si allontanano troppo dal *manifold* dei dati di addestramento misurando l'errore di ricostruzione tramite un autoencoder.

**9. Costruzione dei prototipi: Autoencoder vs k-d tree**
I prototipi vengono costruiti in modo diverso a seconda della disponibilità di un autoencoder:
*   **Con Autoencoder (Encoder latente):** Il prototipo di una classe è definito come la **codifica media** (nel latente) delle $K$ istanze di quella classe più vicine all'istanza originale. Si lavora quindi in uno spazio compresso.
*   **Con k-d tree:** In assenza di un encoder, si costruiscono dei k-d tree specifici per ogni classe utilizzando i dati di addestramento. Il prototipo viene identificato come l'elemento del k-d tree della classe target più vicino all'istanza originale nello **spazio delle caratteristiche originale**.
*   **Preferenza:** L'approccio con autoencoder è preferibile per dati complessi e ad alta dimensionalità come le **immagini** (es. MNIST), mentre l'uso dei k-d tree è adatto per **dati tabulari** o quando non si dispone di un autoencoder già addestrato.

**10. Contributo del termine prototipo alla plausibilità e alla convergenza**
Il termine prototipo migliora l'approccio base di Wachter (che usa solo $L_{pred}$ e la distanza elastica) in due modi fondamentali:
*   **Plausibilità:** A differenza di Wachter, che cerca solo di superare il confine di decisione del modello, CounterfactualProto spinge attivamente l'istanza verso il "centro" (prototipo) della classe target, garantendo che il controfattuale assomigli a esempi reali e sia quindi più plausibile.
*   **Velocità di convergenza:** Il termine $L_{proto}$ fornisce una direzione chiara all'ottimizzazione, riducendo drasticamente il tempo e le iterazioni necessarie (fino all'80-90% in meno nei test MNIST). Inoltre, per i modelli "black box", l'uso dei prototipi permette di eliminare $L_{pred}$, evitando il costoso calcolo numerico dei gradienti e velocizzando il processo di circa 100 volte.