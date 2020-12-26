# Descrizione dell'utilizzo della memoria ottenuto tramite [memory-profiler](https://pypi.org/project/memory-profiler/)

### N.B.: in tutti i risultati che seguono la memoria occupata da Closure.build è ampiamente sottostimata. La ragione di ciò sta nel fatto che tutto ciò che viene creato dentro closure viene in larga parte deallocato alla terminazione del metodo stesso. Dunque la memoria cresce durante la durata di build (anche di diverse decine di MB), ma alla fine del metodo il cambiamento è irrisorio/nullo.

Si sottolinea a tal proposito che alcuni residui possono essere presenti in quanto viene mantenuto solo ciò a cui è associata una regex. Dunque più sono questi elementi più è probabile che il cambiamento risulti visibile.

I cosiddetti "task" sono i compiti presenti nella consegna.

## Primo test
    task 1:
        + 0.37M in build CFANSpace

    task 2:
        + ~0M in build CFANSObservation

    task 4:
        + 0.32M in build CFANSpace
        + ~0M in build Closure


## Altra rete
    task 1:
        + 0.37M in build CFANSpace 
		
    task 2:
        + 0.37M in build CFANSObservation
	
    task 4:
        + 0.37M in build CFANSpace
        + ~0M in build Closure


## Benchmark
    task 1:
        + 0.63M in build CFANSpace
		
    task 2:
        + 0.63M in build CFANSObservation
	
    task 4:
        + 0.63M in build CFANSpace
        + 0.26M in build Closure


## Domotica
    task 1:
        + 0.63M in build CFANSpace
		
    task 2:
        + 0.32M in build CFANSObservation
	
    task 4:
        + 0.63M in build CFANSpace
        + ~0M in build Closure
