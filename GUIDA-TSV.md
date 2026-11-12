# Importare il vocabolario su Anki da file TSV

Questa guida spiega come importare in Anki il file `anki/vocabolario-completo.tsv` (non il pacchetto `russo.apkg`) e come creare le carte, sia per le parole singole sia per le parole con frase d'esempio.

Il procedimento ha tre parti, da fare **una sola volta** sul computer: creare il tipo di nota, importare il file, controllare le carte. Per gli aggiornamenti successivi basta reimportare il file (passo 5).

---

## 1. Cosa serve

- **Anki Desktop** versione 2.1.55 o successiva (gratuito, da apps.ankiweb.net). Le versioni più vecchie non leggono le righe di intestazione del file e non hanno la schermata di importazione descritta qui. La versione si controlla in **Aiuto → Informazioni su Anki**.
- Il file `vocabolario-completo.tsv`.
- Il file `template-carte.html` (lo stesso da cui si genera `russo.apkg`, quindi le carte sono identiche nei due metodi), da cui si copiano i template e lo stile delle carte. Va aperto in un editor di testo o nel browser (con il tasto destro → «Visualizza sorgente»): non è un mazzo da importare.

> L'importazione del TSV e la modifica dei template si fanno su Anki Desktop. Per studiare dal telefono si sincronizza poi con AnkiWeb (vedi passo 7).

---

## 2. Com'è fatto il file TSV

Ogni riga è una nota, con sei colonne separate da tabulazione:

| Colonna | Campo Anki      | Contenuto                                                                                                                                   |
| ------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| 1       | `ID`            | Identificativo stabile della parola (es. `kot`). Non compare sulle carte: serve ad Anki per riconoscere la nota quando si reimporta il file |
| 2       | `Russo`         | La parola o l'espressione in russo                                                                                                          |
| 3       | `Italiano`      | La traduzione. Se la parola ha più significati sono separati da ` / `                                                                       |
| 4       | `FraseRusso`    | La frase d'esempio, con la parola evidenziata. Può essere vuota                                                                             |
| 5       | `FraseItaliano` | La traduzione della frase. Può essere vuota                                                                                                 |
| 6       | Tag             | Temi e lezioni, separati da spazio (es. `animali lez-3`)                                                                                    |

Il file contiene in cima cinque righe che iniziano con `#`: non sono parole, ma istruzioni per Anki (separatore, HTML attivo, tipo di nota e mazzo di destinazione, colonna dei tag). Non vanno cancellate.

Se una parola compare in più liste, nel TSV ha una sola riga: i significati vengono uniti (separati da ` / `) e si tiene una sola frase d'esempio, la prima in ordine di lista.

---

## 3. Creare il tipo di nota «Russo» (una sola volta)

Il tipo di nota definisce i campi e le carte. Il nome e i nomi dei campi devono essere **esattamente** quelli indicati, maiuscole comprese.

### 3.1 Creare il tipo di nota

1. In Anki si apre **Strumenti → Gestisci tipi di nota**.
2. Si clicca **Aggiungi**, si sceglie **Aggiungi: Base** e si conferma.
3. Si dà il nome `Russo` e si conferma.

### 3.2 Impostare i campi

1. Con `Russo` selezionato, si clicca **Campi…**.
2. Si rinomina il campo `Fronte` (o `Front`) in `ID` e il campo `Retro` (o `Back`) in `Russo`.
3. Si aggiungono tre campi, con **Aggiungi**: `Italiano`, `FraseRusso`, `FraseItaliano`.
4. L'ordine finale deve essere: `ID`, `Russo`, `Italiano`, `FraseRusso`, `FraseItaliano`. Si può cambiare con **Riposiziona**.
5. Con il campo `Russo` selezionato, si attiva **Ordina per questo campo nel browser**, così nella lista delle carte si vede la parola e non l'ID.
6. Si conferma con **Salva**.

L'`ID` è il primo campo perché Anki usa il primo campo per riconoscere le note già importate.

### 3.3 Creare le tre carte e lo stile

1. Nella finestra «Tipi di nota» si clicca **Carte…**.
2. Si apre `template-carte.html` e si lavora con i tre tipi di carta, uno alla volta.
3. **Carta 1** (c'è già, si chiama «Carta 1»):
   - si copia nel riquadro **Template fronte** il contenuto del blocco `russo-italiano-fronte`;
   - si copia nel riquadro **Template retro** il contenuto del blocco `russo-italiano-retro`;
   - si rinomina il tipo di carta in **Russo → Italiano** (menu **Opzioni → Rinomina tipo di carta**).
4. **Carta 2**: si aggiunge con **Opzioni → Aggiungi tipo di carta**, si copiano fronte e retro dai blocchi `italiano-russo-fronte` e `italiano-russo-retro` e si rinomina in **Italiano → Russo**.
5. **Carta 3**: stessa procedura, con i blocchi `frase-traduzione-fronte` e `frase-traduzione-retro`, e nome **Frase → Traduzione**.
6. Si apre la scheda **Stile** e si sostituisce tutto il contenuto con il blocco `<style>` del file (senza i tag `<style>` e `</style>`). Lo stile è unico per tutte e tre le carte.
7. Si chiude con **Salva**.

Nei template si copia solo il contenuto dei blocchi, senza i tag `<template>` e `</template>`.

### Come funzionano le parole singole e quelle con frase

Un solo tipo di nota basta per entrambi i casi:

- **Parola con frase**: genera tre carte (Russo → Italiano, Italiano → Russo, Frase → Traduzione). La frase compare anche sul retro delle prime due.
- **Parola senza frase** (colonne 4 e 5 vuote): genera solo le prime due carte, senza spazi vuoti. La terza carta non viene creata, perché il suo fronte, che contiene solo la frase, resta vuoto.

---

## 4. Importare il file

1. In Anki si apre **File → Importa…** e si sceglie `vocabolario-completo.tsv`.
2. Nella finestra di importazione si controlla che compaia:
   - **Tipo di nota**: `Russo`
   - **Mazzo**: `Russo`
   - **Separatore campi**: tabulazione
   - **Consenti HTML nei campi**: attivo (serve per l'evidenziazione delle parole nelle frasi)
3. Si controlla la **corrispondenza dei campi**: la colonna 1 va in `ID`, la 2 in `Russo`, la 3 in `Italiano`, la 4 in `FraseRusso`, la 5 in `FraseItaliano`, la 6 in **Tag**.
4. Alla voce **Note esistenti** (o «Aggiorna note esistenti») si sceglie **Aggiorna**.
5. Si clicca **Importa**. Alla fine Anki mostra un riepilogo, con il numero di note aggiunte.

Se Anki non preseleziona il tipo di nota o il mazzo, si scelgono a mano dai menu a tendina: le intestazioni `#notetype` e `#deck` sono solo dei suggerimenti.

---

## 5. Aggiornare il vocabolario

Quando arriva una nuova versione di `vocabolario-completo.tsv`:

1. Si ripete il passo 4 con il file nuovo, lasciando **Aggiorna** tra le note esistenti.
2. Le note con lo stesso `ID` vengono aggiornate (traduzione, frasi, tag) e **i progressi di studio restano**. Le parole nuove vengono aggiunte.
3. Le parole eliminate dal file **non** vengono cancellate da Anki: se serve, si eliminano a mano da **Sfoglia**.

> L'`ID` non va mai modificato: se cambia, Anki considera la riga una parola nuova e quella vecchia resta nel mazzo con i suoi progressi.

---

## 6. Aggiungere nuove parole alle liste

Questa parte riguarda chi mantiene i file nella cartella `lezioni/`. Per rigenerare il TSV si lancia dalla cartella del progetto:

```bash
python3 scripts/generate_anki_from_liste.py --solo-tsv
```

L'opzione `--solo-tsv` crea soltanto `anki/vocabolario-completo.tsv`. Senza l'opzione si rigenera anche `russo.apkg`, il pacchetto per chi usa il telefono.

Nei file delle lezioni, le righe possono avere:

- **4 colonne** per una parola singola: `russo`, `italiano`, `categoria`, `id`;
- **6 colonne** per una parola con frase: le stesse quattro più `frase-russo` e `frase-italiano`.

Nella frase la parola da evidenziare va racchiusa tra `<b>` e `</b>`, ad esempio `У меня <b>кот</b>.`: nel TSV diventa l'evidenziazione colorata. L'`ID` va scelto una volta sola e non va più cambiato.

---

## 7. Studiare dal telefono

Il tipo di nota e le carte create sul computer si portano sul telefono con la sincronizzazione:

1. Si crea un account gratuito su ankiweb.net.
2. In Anki Desktop si preme **Sincronizza** e si accede con l'account.
3. Su **AnkiDroid** o **AnkiMobile** si accede con lo stesso account e si preme **Sincronizza**: arrivano mazzo, tipo di nota, template e progressi.

Dopo ogni nuova importazione sul computer si sincronizza di nuovo.

---

## 8. Studiare per tema, lezione o direzione

Ogni nota ha tag di tema e di lezione (`animali`, `lez-3`…). Da **Sfoglia** si possono cercare e raggruppare:

- `tag:lez-3` per una lezione, `tag:lez-1 OR tag:lez-2` per più lezioni;
- `tag:cibo-e-bevande` per un tema;
- `card:"Russo → Italiano"` per una sola direzione, anche insieme a un tag (es. `card:"Russo → Italiano" tag:lez-3`);
- `card:"Frase → Traduzione"` per allenarsi solo sulle frasi.

Per studiare un sottoinsieme in modo separato si usa **Strumenti → Crea mazzo filtrato…** con la stessa ricerca.

---

## 9. Ordine in cui compaiono le carte

Ogni parola ha fino a tre carte. Se le carte nuove compaiono in ordine sparso (per esempio la carta «Frase → Traduzione» di una parola, poi «Italiano → Russo» di un'altra, e le carte della stessa parola in giorni diversi), la causa sono le opzioni del mazzo, non un errore del file.

Le impostazioni si trovano nella schermata **Mazzi**, con l'ingranaggio accanto a «Russo» → **Opzioni**, nella sezione **Ordine di presentazione**:

- **Ordine di recupero delle nuove carte** stabilisce *quali* carte nuove vengono prese ogni giorno, fino al limite giornaliero.
- **Ordine delle nuove carte** stabilisce in che *ordine* vengono mostrate quelle prese.

Con **Casuale (note)** per il recupero e **Casuale** per l'ordine, le carte nuove vengono scelte e rimescolate una per una: i tre tipi di carta di una parola si separano e si alternano a quelli di altre parole. Combinazioni più utili:

| Obiettivo | Ordine di recupero | Ordine delle nuove carte |
| --- | --- | --- |
| Parole nell'ordine del file (alfabetico), con le carte della stessa parola vicine | Posizione crescente | Ordine di recupero |
| Parole in ordine casuale, ma con le carte di ciascuna vicine | Casuale (note) | Nota casuale, poi tipo di carta |
| Tutto in ordine casuale, anche i tipi di carta | Casuale (note) | Casuale |

I nomi delle voci possono variare un po' secondo la versione di Anki. Accanto a ciascuna voce c'è una freccia circolare che la riporta al valore predefinito.

Altre cose da sapere:

- Le modifiche valgono per le carte nuove ancora da proporre: le carte già studiate non cambiano.
- Le opzioni sono legate al **preset** («Predefinito»), che vale per tutti i mazzi che lo usano: cambiandolo per «Russo» si cambia anche per gli altri mazzi con lo stesso preset.
- Nella sezione **Seppellimento** l'opzione per le carte nuove «sorelle» (le altre carte della stessa parola) fa comparire una sola carta per parola al giorno: le altre ricompaiono il giorno dopo. Per vedere insieme tutte le carte di una parola si disattiva.
- Il file è ordinato alfabeticamente in russo, quindi con l'ordine «sequenziale» le parole arrivano in ordine alfabetico, non di lezione. Per studiare una lezione alla volta si usano i tag (passo 8).

---

## 10. Problemi frequenti

| Problema | Cosa fare |
| --- | --- |
| Sulle carte compaiono scritte come `<span class="target-word">` | L'HTML non è attivo. Si reimporta il file controllando che **Consenti HTML nei campi** sia attivo |
| La parola non è evidenziata in rosso sul giallo | Lo stile non è stato copiato nella scheda **Stile** del tipo di nota (passo 3.3, punto 6) |
| Tutto il contenuto finisce in un solo campo | Il separatore non è la tabulazione. Nella finestra di importazione si imposta **Tabulazione** |
| I campi sono sfalsati (la traduzione nel campo sbagliato) | La corrispondenza dei campi non è quella del passo 4: si corregge nella finestra, prima di cliccare **Importa** |
| Dopo un aggiornamento ci sono parole doppie | Alla voce **Note esistenti** era selezionato «Duplica» invece di **Aggiorna**. Si annulla l'importazione da **Modifica → Annulla** oppure si eliminano i doppioni da **Sfoglia → Note → Trova duplicati** |
| Alcune parole hanno solo due carte | È normale: sono le parole senza frase d'esempio (la carta «Frase → Traduzione» richiede una frase) |
| Ogni parola compare due volte nel mazzo | Si sono importati sia il TSV sia il pacchetto `russo.apkg`. Hanno gli stessi campi e le stesse carte, ma per Anki sono due tipi di nota distinti (il secondo compare con un nome come «Russo-xxxxx»), quindi le note non si fondono. Si sceglie un solo metodo: si elimina uno dei due mazzi e, da **Strumenti → Gestisci tipi di nota**, il tipo di nota che resta inutilizzato |
| «Tipo di nota non trovato» o la finestra di importazione non preseleziona `Russo` | Il tipo di nota non è stato creato o ha un nome diverso. Si controlla il passo 3.1 oppure si sceglie `Russo` dal menu a tendina |
| Il file non si importa o mancano le righe di intestazione | La versione di Anki è troppo vecchia: serve la 2.1.55 o successiva |
