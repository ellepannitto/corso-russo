# Importare i File in Anki

Questa guida descrive il flusso consigliato per importare i file `TSV` presenti in questa cartella dentro Anki e aggiornarli nel tempo.

## File disponibili

Categorie principali:

- `00-alfabeto.tsv`
- `01-natura-e-luoghi.tsv`
- `02-animali.tsv`
- `03-cibo-e-bevande.tsv`
- `04-verbi.tsv`
- `05-persone-e-famiglia.tsv`
- `06-corpo.tsv`
- `07-abbigliamento.tsv`
- `08-casa-e-oggetti.tsv`
- `09-tempo-e-date.tsv`
- `10-meteo-e-stagioni.tsv`
- `11-aggettivi.tsv`
- `12-avverbi.tsv`
- `13-domande-e-connettori.tsv`
- `14-scuola-e-lingua.tsv`
- `15-viaggi-e-trasporti.tsv`
- `16-feste.tsv`
- `17-espressioni-utili.tsv`

Categorie extra:

- `18-vocabolario-base.tsv`
- `19-frasi-base.tsv`

Template:

- `99-template-vuoto.tsv`

## Struttura dei campi

Ogni file usa 5 colonne separate da tab:

1. `ID`
2. `Front`
3. `Back`
4. `Notes`
5. `Tags`

Convenzione dei contenuti:

- `Front` = russo
- `Back` = italiano

## Strategia consigliata

Usa un tipo di nota dedicato, per esempio `Russo TSV`, con questi campi:

1. `ID`
2. `Front`
3. `Back`
4. `Notes`

Le tag possono essere importate dal file nella sezione dedicata dell'import.

## Creazione del Tipo di Nota

In Anki:

1. Apri `Strumenti` > `Gestisci tipi di nota`.
2. Duplica `Basic`.
3. Rinomina il nuovo tipo in `Russo TSV`.
4. Apri `Campi`.
5. Aggiungi i campi `ID` e `Notes`.
6. Riordina i campi in questo ordine:
   - `ID`
   - `Front`
   - `Back`
   - `Notes`

## Modello delle Carte

Puoi iniziare con un modello semplice:

- Fronte: `{{Front}}`
- Retro: `{{FrontSide}}<hr id=answer>{{Back}}<br><br>{{Notes}}`

Se non vuoi mostrare `Notes` sempre, puoi toglierlo dal retro.

## Primo Import

Per importare un file, ad esempio `03-cibo-e-bevande.tsv`:

1. Apri Anki.
2. Scegli `File` > `Importa`.
3. Seleziona il file TSV.
4. Imposta:
   - `Tipo di nota`: `Russo TSV`
   - separatore: `tab`
   - mazzo: quello che vuoi usare
5. Mappa i campi cosi':
   - colonna 1 -> `ID`
   - colonna 2 -> `Front`
   - colonna 3 -> `Back`
   - colonna 4 -> `Notes`
6. Imposta la colonna 5 come `Tags`.
7. Completa l'import.

## Reimport e Aggiornamenti

Per aggiornare i contenuti in futuro:

1. Mantieni invariato il valore `ID` delle carte gia' esistenti.
2. Modifica liberamente `Front`, `Back`, `Notes` e `Tags`.
3. Reimporta lo stesso file in Anki.

Regola pratica:

- se cambi un testo ma lasci lo stesso `ID`, quella riga rappresenta la stessa carta
- se cambi anche `ID`, Anki la considerera' una carta diversa

## Organizzazione Consigliata

Puoi scegliere una di queste due strategie:

1. Un mazzo unico `Russo` con tag per categoria.
2. Un mazzo per file:
   - `Russo::Alfabeto`
   - `Russo::Vocabolario`
   - `Russo::Verbi`
   - `Russo::Frasi`

La seconda opzione e' spesso piu' comoda all'inizio.

## Convenzione per gli ID

Mantieni gli ID leggibili e stabili, per esempio:

- `alfabeto-a`
- `vocab-privet`
- `verbo-byt`
- `frase-kak-dela`

Evita di rinominare gli ID solo per motivi estetici.

## GitHub + Anki

Il flusso consigliato e':

1. modifichi i file `.tsv`
2. fai commit nel repository
3. pubblichi su GitHub
4. importi o reimporti in Anki dal file locale aggiornato

GitHub e' la fonte sorgente dei dati.
Anki e' il sistema di studio.

## Controlli Rapidi Prima dell'Import

Prima di importare:

- verifica che l'header sia `ID Front Back Notes Tags`
- verifica che ogni riga abbia 5 colonne
- verifica che gli `ID` non siano duplicati nello stesso file
- evita tab o ritorni a capo non voluti dentro una cella

## Nota Importante

L'import standard di Anki non e' un sistema di sincronizzazione avanzata del database. Per questo conviene trattare i file `TSV` come sorgente canonica e mantenere gli `ID` stabili nel tempo.
