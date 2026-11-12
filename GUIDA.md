# Come usare il vocabolario su Anki

Questa guida spiega cos'è Anki, come installarlo e caricare il vocabolario del corso di russo (parole e frasi d'esempio).

Un solo file: `russo.apkg` — contiene tutto il vocabolario già pronto.

---

## 1. Cos'è Anki e installazione

Anki è un'app di flashcard basata sulla ripetizione dilazionata: le carte vengono ripresentate più spesso quando c'è il rischio di dimenticarle e più raramente quando sono ormai consolidate, così lo studio si concentra dove serve davvero.

**Android** → si cerca **AnkiDroid** su Google Play. È gratuito.

**iPhone** → si cerca **AnkiMobile Flashcards** su App Store. Costa circa 25 €.

**Computer (Windows/Mac/Linux)** → si scarica **Anki Desktop**, gratuito, da apps.ankiweb.net.

Esiste anche una versione web gratuita su ankiweb.net, ma è meno comoda da usare ogni giorno.

> **Solo AnkiWeb dal browser, senza installare nulla sul telefono?** Non è possibile importare `russo.apkg` direttamente da ankiweb.net: serve prima uno dei client (AnkiDroid, AnkiMobile o **Anki Desktop**) per fare l'import una volta sola. Con Anki Desktop: si installa, si importa il file (passo 3), poi si attiva la sincronizzazione (Anki → Sincronizza, serve un account gratuito su ankiweb.net). Da quel momento le carte compaiono anche su ankiweb.net/study, utilizzabili da browser su qualsiasi computer.

---

## 2. Salvare il file

Quando si riceve il file `russo.apkg` (via email, WhatsApp, link…):

### Su telefono

- Lo si tiene premuto (o si tocca sui tre puntini accanto al file) e lo si salva nella cartella Download.
- Su iPhone, lo si salva nell'app **File** (in "Sul mio iPhone" o iCloud Drive).

### Su computer

- Lo si scarica e lo si salva in una cartella facile da ritrovare, ad esempio Download o Desktop.

---

## 3. Importare il vocabolario

### Su Android (AnkiDroid)

1. Si apre la cartella Download sul telefono.
2. Si tocca il file `russo.apkg`.
3. Se viene chiesto con quale app aprirlo, si sceglie **AnkiDroid**.
4. Compare un messaggio con il numero di carte importate. Si tocca **OK**.

### Su iPhone (AnkiMobile)

1. Si apre l'app **File** e si trova il file `russo.apkg`.
2. Si tiene premuto il file → si tocca **Condividi** → si sceglie **Copia in AnkiMobile**.
3. Anki si apre e mostra un messaggio di importazione completata. Si tocca **OK**.

> Se non si riesce a "condividere" con AnkiMobile, si può provare da Safari: si apre il link del file direttamente nel browser e Safari gestisce l'apertura automatica.

### Su computer (Anki Desktop)

1. Si scarica `russo.apkg` (di solito finisce nella cartella Download).
2. Si apre **Anki Desktop**.
3. Si va su **File → Importa file...** (oppure si trascina il file `russo.apkg` sulla finestra di Anki).
4. Si seleziona `russo.apkg` e si conferma: le carte vengono aggiunte subito, senza altre schermate.

---

## 4. Creare mazzi personalizzati (per lezione o per tema)

Tutte le carte arrivano in un unico mazzo "Russo", ma ogni carta ha delle **etichette (tag)** che indicano la lezione e il tema (ad esempio `lez-3`, `animali`, `cibo-e-bevande`...). Si possono usare per studiare solo un sottoinsieme di parole, senza bisogno di un file diverso per ogni lezione.

1. In Anki si apre **Sfoglia** (l'icona della lente/lista carte).
2. Nella barra di ricerca si scrive un tag, ad esempio: `tag:lez-3` oppure `tag:cibo-e-bevande`.
3. Si selezionano tutti i risultati (su AnkiDroid: si tocca e si tiene premuto su una carta, poi "Seleziona tutto").
4. Si sceglie **Crea filtro** / **Crea mazzo filtrato** (oppure "Cambia mazzo" per spostarle in un mazzo separato invece che filtrarle).
5. Si dà un nome al nuovo mazzo (es. "Lezione 3") e si conferma.

Si possono combinare più tag nella ricerca, ad esempio `tag:lez-1 OR tag:lez-2` per unire due lezioni, oppure `tag:cibo-e-bevande -tag:lez-1` per il tema "cibo e bevande" escludendo la lezione 1.

> Un mazzo filtrato "prende in prestito" le carte dal mazzo originale: i progressi restano collegati alla carta originale, quindi si può usare e cancellare senza perdere nulla.

---

## 5. Usare i diversi tipi di carta (template)

Ogni parola genera due carte, e tre se ha una frase d'esempio:

- **Russo → Italiano**: sul fronte la parola in russo, sul retro la traduzione e, se c'è, la frase.
- **Italiano → Russo**: sul fronte la traduzione, sul retro la parola in russo e, se c'è, la frase.
- **Frase → Traduzione**: sul fronte la frase russa con la parola da imparare evidenziata, sul retro la traduzione della frase. Esiste solo per le parole con una frase d'esempio.

Per allenarsi solo con un tipo di carta:

1. Si va in **Sfoglia**.
2. Si cerca `card:"Russo → Italiano"` (nome esatto del template) per vedere solo le carte in quella direzione. Si può combinare con un tag, es. `card:"Russo → Italiano" tag:lez-3`. Per le sole frasi: `card:"Frase → Traduzione"`.
3. Da lì si può creare un mazzo filtrato come al punto 4, oppure disattivare temporaneamente un template dalle impostazioni del **Tipo di nota** (Strumenti → Gestisci tipi di nota → Carte), se non si vuole vedere affatto uno dei tipi di carta.

---

## 6. Segnalare una modifica o un errore

Se si trova un errore (parola sbagliata, traduzione mancante, carta duplicata) o si vuole proporre un'aggiunta, il modo più semplice è mandare un messaggio con questi dati:

- **L'ID della carta**, se lo si vede: in Anki → Sfoglia, selezionando la carta e guardando il campo `ID` (o aggiungendo la colonna "ID" alla lista). È il modo più preciso per identificarla, perché non cambia mai anche se la parola viene corretta.
- In alternativa, **la parola in russo** (e in italiano, se nota) così com'è scritta nella carta.
- **Cosa non va o cosa si vorrebbe cambiare** (es. "la traduzione è sbagliata, dovrebbe essere...", "manca la parola X", "serve un tag per il tema Y").
- **Se possibile**, uno screenshot della carta in Anki: aiuta a trovarla subito.

Non serve modificare nulla in autonomia: basta segnalare, la carta verrà corretta alla fonte e arriverà aggiornata nella prossima versione di `russo.apkg` (vedi "Aggiornamenti e problemi frequenti" sotto — i progressi non si perdono).

---

## 7. Aggiornamenti e problemi frequenti

Quando arriva una nuova versione del file `russo.apkg`, la si importa seguendo di nuovo il **passo 3**. Le carte già esistenti vengono aggiornate senza cancellare i progressi.

> **Chi ha importato una versione precedente.** L'ultima versione di `russo.apkg` usa un nuovo tipo di nota, chiamato **Russo** (campi: ID, Russo, Italiano, FraseRusso, FraseItaliano). Anki lo aggiunge accanto al vecchio tipo «Russo TSV» e le parole risultano doppie. Per mantenere i progressi: in **Sfoglia** si cerca `note:"Russo TSV"`, si selezionano tutte le carte e si sceglie **Note → Cambia tipo di nota**, indicando «Russo» come nuovo tipo (Anki chiede di abbinare i campi: Front → Russo, Back → Italiano, ExampleRu → FraseRusso, ExampleIt → FraseItaliano, ID → ID). Si importa poi il nuovo file. Chi ha pochi progressi può invece eliminare il vecchio mazzo e reimportare.

| Problema | Cosa fare |
| --- | --- |
| Non compare nessuna carta dopo l'import | Si controlla che il mazzo "Russo" sia visibile nella schermata principale di Anki |
| Le carte sono vuote o mostrano codici strani | L'encoding non è corretto — si contatta chi ha mandato il file |
| L'app non riconosce il file `.apkg` | Ci si assicura che il file non sia stato rinominato durante il download |
| Non si riesce ad aprire il file `.apkg` su iPhone | Si prova da Safari invece che da altre app |
| Alcune parole hanno solo due carte | È normale: la carta «Frase → Traduzione» esiste solo per le parole con una frase d'esempio |
| Dopo un aggiornamento le parole sono doppie | Si sono importati due tipi di nota diversi (vedi il riquadro sopra): si spostano le carte vecchie sul nuovo tipo oppure si elimina il mazzo vecchio |

---

## 8. Alternativa: importare il file TSV (solo computer)

Al posto di `russo.apkg` si può importare `vocabolario-completo.tsv`, lo stesso vocabolario in forma di tabella. Le carte risultano identiche. Serve Anki Desktop 2.1.55 o successivo; per il telefono si sincronizza poi con AnkiWeb. Pacchetto e TSV creano due tipi di nota distinti: importandoli entrambi le parole risultano doppie, quindi se ne sceglie uno solo.

1. Si crea il tipo di nota `Russo` con i campi `ID`, `Russo`, `Italiano`, `FraseRusso`, `FraseItaliano` e le tre carte, copiando template e stile da `template-carte.html`.
2. Si importa il file da **File → Importa…** con tipo di nota e mazzo `Russo`, HTML attivo e **Aggiorna** per le note esistenti.

La procedura passo per passo è in `GUIDA-TSV.md`.
