# Progetto: Cheat Sheet Fondamenti di Elettronica (CSFdE)

## Struttura del documento

Il file principale è `CSFdE.tex`. È un documento LaTeX composto da **box** (riquadri) realizzati con `tikzpicture` + `mybox` + `fancytitle`.

### Template di una box

```latex
\begin{tikzpicture}
    \node [mybox] (box){%
        \begin{minipage}{0.3\textwidth}

            \small
            % Contenuto qui

        \end{minipage}
    };
    \node[fancytitle, right=10pt] at (box.north west) {\color{white}Titolo Box};
\end{tikzpicture}
```

### Spaziatura tra box

- Tra box nella stessa pagina: `\vspace{0.3cm}`
- Cambio sezione/pagina: `\newpage`
- Separatore nei commenti: `%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%`

## Regole critiche

### Overflow verticale

Le box hanno spazio verticale limitato. Se una box diventa troppo lunga:
- **Spezzare** in due o più box contigue (stessa pagina o pagina successiva)
- Dare a ciascuna un titolo descrittivo (es. "Contention - Teoria" e "Contention - Calcolo")
- NON tentare di comprimere il contenuto

### Trovare la posizione giusta

Quando l'utente chiede di aggiungere contenuto:
1. Cercare con `Grep` la sezione/box pertinente
2. Leggere il contesto circostante per capire dove inserire
3. Inserire nella posizione logica corretta (dopo la box correlata, prima della sezione successiva)

## Convenzione formule MOS (CRITICO)

Il parametro $K$ è definito **CON** il fattore $\frac{1}{2}$ incluso:

$$K = \frac{1}{2} \mu C_{OX} \frac{W}{L}$$

### Conseguenze su TUTTE le formule

| Formula | Corretta (K include 1/2) | SBAGLIATA (K senza 1/2) |
|---------|--------------------------|-------------------------|
| Saturazione | $I = K(V_{GS}-V_T)^2$ | ~~$I = \frac{K}{2}(V_{GS}-V_T)^2$~~ |
| Ohmica | $I = K[2(V_{GS}-V_T)V_{DS} - V_{DS}^2]$ | ~~$I = K[(V_{GS}-V_T)V_{DS} - \frac{V_{DS}^2}{2}]$~~ |
| $R_{DS,on}$ | $\frac{1}{2K(V_{GS}-V_T)}$ | ~~$\frac{1}{K(V_{GS}-V_T)}$~~ |
| $I_{sat}$ | $K \cdot V_{OV}^2$ | ~~$\frac{K}{2} V_{OV}^2$~~ |

### Formule per nMOS

- Sat: `$I_D = K_n(V_{GS} - V_T)^2$`
- Ohm: `$I_D = K_n\left[2(V_{GS} - V_T)V_{DS} - V_{DS}^2\right]$`
- R_DS,on: `$R_{DS,on,n} = \frac{1}{2K_n(V_{GS,n} - V_{Tn})}$`

### Formule per pMOS

Due notazioni equivalenti usate nel documento:

**Con moduli** (nella box "pMOS - Metodo operativo"):
- Sat: `$I_D = K_p(|V_{GS}| - |V_T|)^2$`
- Ohm: `$I_D = K_p\left[2 V_{OV} \cdot |V_{DS}| - |V_{DS}|^2\right]$`

**Con V_SG/V_SD** (nella box formule e nelle sezioni contention/logica):
- Sat: `$I_p = |K_p|(V_{SG,p} - |V_{Tp}|)^2$`
- Ohm: `$I_p = |K_p|\left[2(V_{SG,p} - |V_{Tp}|)V_{SD,p} - V_{SD,p}^2\right]$`
- R_DS,on: `$R_{DS,on,p} = \frac{1}{2|K_p|(V_{SG,p} - |V_{Tp}|)}$`

### K equivalente (serie/parallelo)

- $N$ MOS uguali in **serie**: $K_{eq} = \frac{K}{N}$
- $N$ MOS uguali in **parallelo**: $K_{eq} = N \cdot K$

## Stile delle colorbox

| Colore | Uso |
|--------|-----|
| `red!25` / `red!30` | Metodo sistematico, warning critici |
| `yellow!30` | Regole chiave, tabelle importanti |
| `green!25` / `green!20` | Procedure, checklist, quando usare cosa |
| `cyan!20` / `cyan!25` | Formule, definizioni |
| `orange!25` | Attenzione, esempi, setup |
| `violet!15` | Metodi di calcolo alternativi |
| `red!20` | Livelli di tensione, sanity check |

## Lingua

Tutto il contenuto delle box è in **italiano**.

## Workflow

1. Quando l'utente chiede di aggiungere qualcosa, trovare la posizione corretta nel file
2. Scrivere il contenuto seguendo il template box e le convenzioni formule
3. Verificare che la box non vada in overflow; se sì, spezzare
4. Controllare coerenza delle formule con la convenzione K (include 1/2)
5. Commit solo quando richiesto esplicitamente dall'utente
