In LIME, la perturbazione dei dati tabulari e la successiva pesatura dei campioni seguono un processo specifico per garantire che il modello interpretabile catturi il comportamento locale del "black box".

### 1. Funzionamento della perturbazione (Campionamento)
Per i dati tabulari, LIME non campiona necessariamente nelle immediate vicinanze dell'istanza da spiegare, ma genera nuovi campioni basandosi sulla distribuzione dei dati di addestramento.

*   **Feature Numeriche:** La perturbazione avviene estraendo valori da una **distribuzione normale (Gaussiana)**. La media e la deviazione standard utilizzate per questa distribuzione sono ricavate direttamente dai valori di quella specifica feature nel dataset di addestramento,.
*   **Indipendenza delle feature:** Un limite importante di questo approccio è che il campionamento avviene ignorando le correlazioni tra le feature, il che può generare punti dati "improbabili" o poco realistici nel mondo reale.
*   **Centro di massa:** I campioni vengono estratti considerando il "centro di massa" dei dati di addestramento, piuttosto che campionare solo intorno all'istanza di interesse. Questo metodo aumenta la probabilità che i punti campionati producano predizioni differenti dal modello originale, permettendo a LIME di apprendere una spiegazione locale efficace.

### 2. Pesatura dei campioni perturbati
Una volta generati i campioni e ottenute le predizioni dal modello black box, LIME assegna a ogni campione un peso basato sulla sua **prossimità** all'istanza originale,.

*   **Kernel Esponenziale:** Per definire quanto un campione sia "vicino" e quindi quanto debba influenzare il modello locale, si utilizza un **kernel di livellamento esponenziale**. Matematicamente, la misura di prossimità $\pi_x(z)$ è definita come:
    $$\pi_x(z) = \exp(-D(x, z)^2 / \sigma^2)$$
    dove $D$ è una funzione di distanza (solitamente calcolata su dati normalizzati) e $\sigma$ è l'ampiezza del kernel,.
*   **Ampiezza del Kernel ($\sigma$):** L'ampiezza determina la dimensione del "vicinato". Ad esempio, nell'implementazione Python di LIME, l'ampiezza del kernel è impostata di default a $0,75$ volte la radice quadrata del numero di colonne (feature) dei dati.
    *   Un'**ampiezza ridotta** significa che solo i campioni molto vicini all'istanza originale hanno un peso significativo.
    *   Un'**ampiezza elevata** permette anche a campioni più lontani di influenzare il modello locale.

In sintesi, mentre il campionamento si basa sulle statistiche globali delle feature (come media e deviazione standard per le numeriche), la **fedeltà locale** della spiegazione è garantita dal sistema di pesatura che privilegia i campioni più simili all'istanza di interesse,.