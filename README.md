# Corso di russo — vocabolario per Anki

Il vocabolario vive nelle liste in `lezioni/`. Lo script `scripts/generate_anki_from_liste.py` le legge e genera i file da dare a Anki, in `anki/`:

| File | A cosa serve |
| --- | --- |
| `anki/russo.apkg` | Pacchetto pronto da importare (telefono o computer), con tipo di nota e carte già dentro |
| `anki/vocabolario-completo.tsv` | Stesso vocabolario in forma di tabella, da importare in Anki Desktop |
| `anki/template-carte.html` | Template e stile delle carte, da cui si generano le carte di entrambi i metodi |
| `anki/guida.html` (+ `guida.css`) | Guida completa per chi studia, con le istruzioni per `.apkg` e TSV |

`GUIDA.md` e `GUIDA-TSV.md` sono le stesse istruzioni in Markdown, rispettivamente per il pacchetto e per il TSV.

## Cos'è il file TSV

Un file **TSV** (*tab-separated values*) è una tabella in puro testo: ogni riga è una riga della tabella e le colonne sono separate da un carattere di tabulazione. Si apre con qualsiasi editor di testo, con Excel o con Fogli Google, e Anki sa importarlo direttamente.

[`anki/vocabolario-completo.tsv`](anki/vocabolario-completo.tsv) ([scarica](https://raw.githubusercontent.com/ellepannitto/corso-russo/main/anki/vocabolario-completo.tsv)) contiene tutto il vocabolario del corso, una nota per riga, in sei colonne: `ID`, `Russo`, `Italiano`, `FraseRusso`, `FraseItaliano`, tag. In cima ha cinque righe che iniziano con `#`: sono istruzioni per Anki (separatore, HTML attivo, tipo di nota e mazzo di destinazione, colonna dei tag) e non vanno cancellate.

Il file è generato dallo script a partire dalle liste in `lezioni/`: non si modifica a mano, perché alla prossima rigenerazione le modifiche andrebbero perse. Come importarlo in Anki è spiegato in [`GUIDA-TSV.md`](GUIDA-TSV.md) e in `anki/guida.html`.

## Rigenerare i file

```bash
pip install -r requirements.txt
python3 scripts/generate_anki_from_liste.py            # russo.apkg + vocabolario-completo.tsv
python3 scripts/generate_anki_from_liste.py --solo-tsv # solo vocabolario-completo.tsv
```

Se una riga è sbagliata (frase senza la parola da evidenziare, `card_id` vuoto, marcatori non bilanciati…) la generazione si ferma indicando file e riga, prima di modificare gli output.

## Tipo di nota e carte

Tutte le note usano un solo tipo di nota, **Russo**, con cinque campi in quest'ordine: `ID`, `Russo`, `Italiano`, `FraseRusso`, `FraseItaliano`. Ogni nota ha tag di tema e di lezione (es. `animali lez-3`).

Ogni parola genera due carte (**Russo → Italiano**, **Italiano → Russo**) e, se ha una frase d'esempio, una terza, **Frase → Traduzione**. Sul fronte compare la frase russa con la parola evidenziata; sul retro la traduzione della frase.

Se una parola compare in più liste, nell'output ha una sola nota: i significati vengono uniti (separati da ` / `) e si tiene una sola frase d'esempio, la prima in ordine di lista.

## Liste delle lezioni

Lo script legge tutti i file di `lezioni/` che si chiamano `lista*` o finiscono in `.tsv`. I file senza estensione e con un nome diverso (come `lezioni/extra`, usato per appunti) vengono ignorati.

Le colonne sono separate da tabulazione. Una riga di intestazione che inizia con `russo` viene saltata. I formati ammessi sono:

- `russo`, `italiano`, `categoria`
- `russo`, `italiano`, `categoria`, `id`
- `russo`, `italiano`, `categoria`, `id`, `frase-russo`, `frase-italiano`

L'`id` è l'identificativo stabile della parola in Anki: va scelto una volta sola e non va più cambiato, altrimenti Anki considera la riga una parola nuova e quella vecchia resta nel mazzo con i suoi progressi. Se una riga non ha `id`, ne viene calcolato uno dalla sola parola russa: correggere quella parola cambierebbe l'ID, quindi conviene sempre indicarlo.

### Evidenziare le parole nelle frasi

Nella colonna `frase-russo` la parola da evidenziare va tra `<b>` e `</b>`:

```text
знать	sapere	verbi	znat	Я <b>знаю</b> ответ.	So la risposta.
отвечать за	essere responsabile di	verbi	otvechat-za	Менеджер <b>отвечает за</b> работу команды.	Il manager è responsabile del lavoro della squadra.
```

- Si possono indicare più parti: `Я <b>хочу</b> читать, а брат <b>хочет</b> гулять.`
- Si accetta anche la forma `**parola**`.
- I marcatori non compaiono sulle carte: il generatore li converte in evidenziazione colorata. Il resto del testo viene trattato come testo, non come HTML.
- Senza marcatori viene evidenziata la forma esatta del lemma (ignorando maiuscole e punteggiatura finale come `?`). Le forme flesse non vengono indovinate: per quelle servono i marcatori.

## Migrare gli ID

`scripts/migrate_card_ids_from_tsv.py` serve a copiare in una sola volta gli ID di un vecchio TSV dentro le liste di `lezioni/`. Con `--source` si indica il file sorgente e con `--fill-missing` si assegna un ID anche ai termini che non esistono nel sorgente. È uno strumento della migrazione iniziale: i file di default che cerca (`anki/A1.tsv`, `anki/vocabolario.tsv`) non esistono più.

## Test

```bash
python3 -m unittest discover tests
```
