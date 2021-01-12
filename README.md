# FSM_algorithm

## Documentazione
Tutta la documentazione è presente dentro la cartella doc.  
Per ottenerla come insime di pagine web si esegua, dentro la cartella doc, il seguente comando:

```
sphinx-build -b html source build
```

dove build è la cartella di destinazione. Può essere sostituita con un altro nome. Tuttavia la cartella source non dovrebbe cambiare nome.

In caso di errori nelle dipendenze si suggerisce di installare, come segue sphinx e il tema usato:

```
pip install sphinx
pip install sphinx_rtd_theme
```

Queste due dipendenze **non sono incluse** fra le dipendenze del progetto, in quanto **non necessarie per l'esecuzione**.

## Compatibilità
Il software è pensato, e testato, per andare con python3.6 o maggiore (ad oggi python3.9).

## Utilizzo
Per utilizzare il programma si esegua __main__.py.
Può essere utilizzando eseguendo

```
./__main__.py
```

oppure

```
python3 __main__.py
```

Si consiglia di inserire i file di input e output al di fuori della cartella del progetto.
