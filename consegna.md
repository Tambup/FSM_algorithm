## Definizioni/Caratteristiche
### Parte 1 (Slide 1-39)
* Operatori primitivi delle regex:
  * Concatenazione
  * Alternativa
  * Ripetizione (zero o più volte)
* Altri operatori:
  * Priorità (la massima precedenza è quella della ripetizione; la concatenazione ha precedenza sull’alternativa)
* Automi a stati finiti (FA):
  * Non esistono stati isolati (se l'insieme degli stati non è un singoletto)
  * Linguaggio accettato: Ogni FA accetta un linguaggio regolare, che è un insieme i cui elementi sono tutte le stringhe sull’alfabeto considerato che portano dallo stato iniziale a uno dei suoi stati di accettazione
* FA come modello comportamentale:
  * È un FA in cui l’**insieme degli stati di accettazione è vuoto**
  * Ogni **transizione** è dotata di **un evento in ingresso**
  * Ogni **transizione** è dotata di **un insieme di eventi in uscita**
  * Possono esistere **più transizioni distinte uscenti dal medesimo stato dotate del medesimo evento in ingresso**, cioè in generale un FA comportamentale è un FA **non deterministico (NFA)**
* Rete (finita) di FA comportamentali:
  * Costituita da almeno un FA comportamentale
  * Gli FA comportamentali sono disposti secondo una topologia distribuita orientata connessa
  * Ciascuna connessione orientata fra componenti distinti prende il nome di link (Possono esistere più link aventi il medesimo componente sorgente e il medesimo componente destinazione)
* Link (*in pratica sono messaggi fra le componenti*):
  * Ogni evento non nullo in ingresso a una transizione proviene da un link
  * Gli eventi prodotti in uscita da una medesima transizione sono inviati ciascuno a un link distinto (necessariamente vuoto)
  * Un link può servire in ingresso tante transizioni distinte del componente destinazione del link stesso
  * Un link può servire in uscita tante transizioni distinte del componente sorgente del link stesso
  * Una transizione dotata di evento in ingresso è abilitata allo scatto solo se tale evento è effettivamente disponibile sul link di provenienza
  * Una transizione che genera eventi in uscita è abilitata allo scatto solo se i link destinatari di tali eventi sono vuoti
  * Una transizione con evento in ingresso nullo e un insieme vuoto di eventi in uscita può sempre scattare, purché abilitata
* Osservabilità e rilevanza:
  * Siano &Omega; e F due insiemi di etichette, la cui unica intersezione è l’etichetta nulla (&epsilon;)
  * Una transizionea cui corrisponde un’etichetta non nulla di &Omega; si dice osservabile e le etichette non nulle in &Omega; prendono anche il nome di etichette/eventi osservabili
  * Una transizione a cui corrisponde un’etichetta non nulla di F si dice rilevante
  * Ogni etichetta non nulla in &Omega; e F deve essere l’immagine di almeno una transizione
  * La medesima etichetta in &Omega;, così come la medesima etichetta in F, può corrispondere a più transizioni, anche di componenti distinti
* Stato di una rete di FA comportamentali:
  * Lo stato di una rete di FA comportamentali è costituito dallo stato di tutti i componenti e di tutti i link
  * Lo stato iniziale della rete è quello in cui ciascun componente è nel suo stato iniziale e i link sono tutti vuoti
  * Uno stato della rete è finale se in esso tutti i link sono vuoti
  * Lo scatto di una transizione abilitata di un singolo componente determina un passaggio di stato della rete
  * Per traiettoria di una rete di automi si intende una sequenza di transizioni di componenti che porta dallo stato iniziale della rete a uno stato finale
* Spazio comportamentaledi una rete di automi:
  * È un FA deterministico(DFA) sull’alfabeto i cui simboli sono gli identificatori di tutte le transizioni dei componenti della rete; il linguaggio di tale DFA è l’insieme (che può contenere infiniti elementi) delle traiettorie della rete
  * Si ottiene applicando tutti i possibili passaggi di stato, a partire dallo stato iniziale della rete
  * A ogni passaggio di stato, lo stato destinazione (della rete) si ottiene creando una copia dello stato sorgente (della rete) e aggiornando entro la copia stessa lo stato del componente a cui la transizione che scatta si riferisce
  * Una sequenza di transizioni che porta da uno stato della rete a un altro prende il nome di cammino
  * Se Stati (e transizioni) non possono raggiungere alcuno stato finale vanno eliminati
  * Lo spazio comportamentale può essere annotato associando a ogni transizione osservabile la relativa etichetta in &Omega; (evento osservabile) e/o associando a ogni transizione rilevante la relativa etichetta in F (evento rilevante)
  * A ogni stato dello spazio comportamentale può essere assegnato un identificatore univoco; operazione detta **Ridenominazione**
  * Sullo spazio comportamentale deve effettuare la **potatura**, ovvero l'eliminazione degli stati (e transizioni) da cui non è possibile raggiungere alcuno stato finale
  
### Parte 2 (Slide 40-46)
* Osservazione lineare:
  * È una sequenza di eventi osservabili, ad esempio O = [o3, o2], verificatisi (nell’ordine stabilito dalla sequenza) lungo una traiettoria della rete di FA comportamentali
  * La stessa osservazione lineare può corrispondere a più traiettorie
* Spazio comportamentale relativo a una osservazione lineare:
  * È la porzione di spazio comportamentale che contiene tutte e sole le traiettorie che producono l’osservazione lineare data
  * Può essere costruito con un algoritmo analogo a quello di costruzione dello spazio comportamentale, dove ogni stato dello spazio, in aggiunta agli stati dei componenti e dei link, contiene anche un indice dell’osservazione lineare data
  * Lo stato iniziale dello spazio comportamentale relativo a un’osservazione lineare O contiene lo stato iniziale di tutti i componenti e di tutti i link nonché il valore 0 (zero) dell’indice dell’osservazione
  * Uno stato dello spazio comportamentale relativo a un’osservazione lineare è finalese tutti i link sono vuoti e il valore dell’indice è pari a length[O]
  * Sia p uno stato dello spazio comportamentale relativo a un’osservazione e q l’indice dell’osservazione in esso contenuto. A partire da p, una transizione osservabile non è abilitata se essa produce un evento osservabile diverso da O[q+1]. Quando q = length[O], nessuna transizione osservabile è abilitata
  * A ogni stato dell'osservazione lineare può essere assegnato un identificatore univoco; operazione detta **Ridenominazione**
  * Sull'osservazione lineare deve effettuare la **potatura**, ovvero l'eliminazione degli stati (e transizioni) da cui non è possibile raggiungere alcuno stato finale
 
 ### Parte 3 (Slide 47-55)
 * A ogni stato finale dello spazio di rilevanza relativo a un’osservazione corrisponde l’espressione regolare ottenuta concatenando le etichette di rilevanza lungo ciascuna traiettoria che porta dallo stato iniziale allo stato finale considerato. Se uno stato finale è raggiunto da più traiettorie l’espressione regolare associata è l’alternativa delle espressioni relative a tali traiettorie
 * Per definizione, la diagnosi relativa a un’osservazione lineare è l’alternativa delle espressioni regolari di rilevanza corrispondenti agli stati finali dello spazio comportamentale inerente all’osservazione stessa
   * La diagnosi relativa a una osservazione lineare può essere calcolata invocando l’algoritmo EspressioneRegolare(Nin), dove Nin è lo spazio comportamentale relativo all’osservazione -considerando i suoi stati finali come stati di accettazione dell’automa - e l’alfabeto dei simboli associati alle transizioni è quello delle etichette di rilevanza 

### Parte 4 (Slide 56-73)
* A ogni stato s dello spazio comportamentale che sia o lo stato iniziale dello spazio stesso o uno stato avente almeno una transizione osservabile entrante corrisponde la sua cosiddetta **«chiusura silenziosa»**, che è esclusiva di quello stato; s è lo stato d’ingresso della sua chiusura
* La chiusura silenziosa di s è costituita dal sottospazio dello spazio comportamentale che contiene tutti (e soli) gli stati raggiungibili a partire da s attraverso cammini contenenti esclusivamente transizioni non osservabili (dette anche silenziose)
* Sia S l’insieme degli stati contenuti nella chiusura silenziosa di uno stato s. Per **decorazione** di ciascuno stato s’ appartiene a S, che siafinale o dotato di transizioni osservabili uscenti entro lo spazio comportamentale (uno stato cosiffatto si dice stato d’uscita della chiusura silenziosa), si intende l’espressione regolare di rilevanza relativa a tutti i cammini che portano da s a s’ entro la chiusura silenziosa
* **Diagnosi relativa auna chiusura silenziosa** è l’alternativa delle decorazioni relative agli stati finali contenuti nella chiusura
* Ciascuna chiusura è univocamente identificata dal suo stato d’ingresso. Il numero delle chiusure distinte inerenti al medesimo spazio comportamentale è pari al numero di stati che, nello spazio comportamentale, sono dotati di transizioni osservabili entranti
* Le chiusure silenziose relative allo spazio comportamentale di una rete di FA comportamentali sono fra loro interconnesse mediante transizioni osservabili, uscenti da stati d’uscita della chiusura sorgente e dirette allo stato d’ingresso della chiusura destinazione (dove la chiusura sorgente può coincidere con la chiusura destinazione)
* **spazio delle chiusure**: Lo stato d’ingresso di una chiusura può appartenere anche ad altre chiusure, dove però non è uno stato d’ingresso. Nessuna interconnessione fra chiusure deve essere diretta a stati che non siano d’ingresso
* **Spazio delle chiusure decorato**: È semplicemente lo spazio delle chiusure in cui ciascuna chiusura è decorata
* **Diagnosticatore**: Al fine di costruire il diagnosticatore, è necessario che la decorazione di ciascuno stato d’uscita entro le chiusure sia ‘ricopiata’ sulla transizione osservabile da esso uscente, concatenando alla decorazione l’eventuale etichetta di rilevanza relativa alla transizione osservabile stessa
  * Per ottenere il diagnosticatoreè infine necessario associare a ciascuna chiusura che contenga degli stati finali la sua diagnosi
  * Può essere visto come un FA dove ogni stato corrisponde a una chiusura silenziosa
  * a ciascuno stato di accettazione è associata una diagnosi
  * ogni transizione è dotata di etichetta di osservabilità e di una espressione regolare
* Per **traiettoria del diagnosticatoresi** intende una sequenza di transizioni (osservabili) dello stesso che porta dallo stato iniziale (cioè quello corrispondente alla chiusura relativa allo stato iniziale dello spazio comportamentale) a uno stato di accettazione (cioè a uno stato del diagnosticatorecorrispondente a una chiusura che contiene qualche stato finale dello spazio comportamentale)
  * Pertanto una traiettoria del diagnosticatorenon comprende alcuna transizione interna alle chiusure dello spazio delle chiusure
  * Una traiettoria termina necessariamente in uno stato relativo a una chiusura dotata di stati finali dello spazio comportamentale; pertanto tale stato del diagnosticatoreha una diagnosi associata
