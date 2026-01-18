# Prompt per ripulitura colorbox LaTeX

A partire dalla box "[NOME BOX DI PARTENZA]" (linea [NUMERO]) fino alla fine del documento, ripulisci l'uso eccessivo di colorbox.

## REFERENCE
Le sezioni PRIMA di "[NOME BOX DI PARTENZA]" sono già state ripulite e rappresentano il criterio da seguire per capire quando mantenere o rimuovere le colorbox.

## CRITERI

### MANTIENI colorbox SOLO per:
1. Formule chiave (con `\boxed{}`)
2. Avvertenze critiche (con simboli `$\triangle$` o `$\bigstar$` + parole ATTENZIONE/ERRORE COMUNE)
3. Titoli di sezione importanti

### RIMUOVI colorbox da:
1. Spiegazioni e metodi step-by-step
2. Esempi pratici
3. Note informative
4. Definizioni introduttive
5. Trucchi mnemonici

## REGOLE FONDAMENTALI
- **ZERO perdita di contenuto**: rimuovi SOLO il wrapper `\colorbox{colore}{\parbox{...}{` e la chiusura `}}`, mantieni TUTTO il testo interno intatto
- **Commit ATOMICI**: un commit per ogni box/sezione modificata
- Verifica che ogni modifica non alteri il significato o rimuova informazioni

## METODO
1. Per ogni colorbox: rimuovi `\colorbox{colore}{\parbox{0.95\linewidth}{` (o simile) e il corrispondente `}}` finale
2. Mantieni il contenuto testuale con la stessa formattazione (`\textbf{}`, `\vspace{}`, elenchi, formule)
3. Se necessario, avvolgi il contenuto in `{\footnotesize ... }` per mantenere la dimensione del testo
