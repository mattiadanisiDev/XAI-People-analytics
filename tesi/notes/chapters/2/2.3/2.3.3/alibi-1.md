FONTE: wachter2017counterfactual

DOMANDE:
•	Qual è la formulazione matematica classica della ricerca di un controfattuale? Come è strutturata la funzione obiettivo originaria proposta da Wachter et al. (bilanciamento tra vicinanza all’istanza originale e cambiamento della predizione)?
•	Che cosa si intende per sparsity di un controfattuale e perché è rilevante per l’interpretabilità da parte di un utente umano? Qual è il ruolo della regolarizzazione L1 nell’ottenere controfattuali sparsi?
•	In che modo le spiegazioni controfattuali si prestano a un uso in contesti ad alto impatto decisionale (es. GDPR “right to explanation”, ambito HR), e quali cautele etiche sono state segnalate in letteratura (es. rischio di suggerire interventi discriminatori o paternalistici)?


RISPOSTA:
Ecco le risposte ai tuoi quesiti basate sulle fonti fornite:

### Formulazione matematica e funzione obiettivo
La formulazione matematica classica proposta da Wachter et al. per la ricerca di un controfattuale consiste nel trovare un punto sintetico $x'$ il più vicino possibile all’istanza originale $x_i$, tale che la predizione del modello $f_w(x')$ corrisponda a un nuovo target desiderato $y'$.

La **funzione obiettivo** è strutturata per bilanciare la vicinanza all’originale e il raggiungimento della nuova predizione attraverso la seguente formula:
$$\arg \min_{x'} \max_{\lambda} \lambda (f_w(x') - y')^2 + d(x_i, x')$$
In questa equazione, il primo termine $(f_w(x') - y')^2$ rappresenta la distanza tra la predizione del controfattuale e il target desiderato, mentre il secondo termine $d(x_i, x')$ è una **funzione di distanza** che misura quanto il controfattuale sia lontano dal punto originale. Il parametro **$\lambda$** viene aumentato iterativamente fino a quando non si trova una soluzione che porti alla predizione desiderata $y'$.

### Sparsity e regolarizzazione L1
Per **sparsity** (scarsità) di un controfattuale si intende una soluzione in cui viene modificato solo un **numero limitato di variabili**, mentre la maggior parte rimane invariata.
*   **Rilevanza per l'utente**: La sparsity è fondamentale per l'interpretabilità umana poiché le spiegazioni sparse sono molto più facili da comunicare e da comprendere per un non esperto. Questo è coerente con il fatto che la memoria di lavoro umana può gestire solo circa sette elementi distinti; fornire troppi cambiamenti simultanei renderebbe la spiegazione incomprensibile.
*   **Ruolo della regolarizzazione L1**: Wachter et al. suggeriscono l'uso della **norma L1** (o distanza di Manhattan), pesata per la deviazione assoluta mediana (MAD), come metrica di distanza. La norma L1 è nota in ambito matematico per la sua tendenza a indurre soluzioni sparse, favorendo cambiamenti in poche variabili piuttosto che piccoli cambiamenti distribuiti su molte variabili (come farebbe invece la norma L2).

### Contesti ad alto impatto decisionale e cautele etiche
Le spiegazioni controfattuali si prestano a contesti come il **GDPR** e le **risorse umane (HR)** perché offrono tre vantaggi principali per l'interessato: aiutarlo a **comprendere** perché è stata presa una decisione, fornirgli basi per **contestare** decisioni avverse e indicargli come **alterare** il proprio comportamento per ottenere un risultato desiderato in futuro.

Tuttavia, le fonti segnalano diverse **cautele etiche e limitazioni**:
*   **Interventi discriminatori**: I controfattuali possono rivelare dipendenze da variabili protette. Ad esempio, nel dataset LSAT, alcuni controfattuali suggerivano che uno studente avrebbe ottenuto un punteggio migliore se la sua **razza** fosse stata diversa, evidenziando un pregiudizio algoritmico. Sebbene questo aiuti a identificare la discriminazione, non la risolve direttamente.
*   **Assunzioni ingenue (mancanza di causalità)**: Spesso questi modelli assumono ingenuamente che le variabili siano indipendenti. Nella realtà, cambiare una variabile (es. il reddito) può dipendere dal cambiamento di un'altra (es. la carriera); senza un accurato modello causale, il controfattuale potrebbe suggerire un mondo "possibile" che non è realisticamente realizzabile o che risulta irrilevante per un intervento pratico.
*   **Paternalismo e Mutabilità**: Sebbene il termine specifico "paternalistico" non compaia esplicitamente nelle fonti citate, esse avvertono che la rilevanza di un controfattuale dipende dalla **mutabilità** delle variabili. Suggerire modifiche a variabili che l'utente non può cambiare (o che non dovrebbe essere costretto a cambiare per ragioni etiche o legali) limita l'utilità e la correttezza della spiegazione.

Nel complesso, i controfattuali sono considerati un "primo passo" utile per bilanciare trasparenza e segreti industriali, ma non sostituiscono la necessità di analisi statistiche su larga scala per garantire l'equità dei sistemi.