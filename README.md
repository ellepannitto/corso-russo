# File per Anki

Questa cartella contiene file `TSV` pronti da importare in Anki.

## Formato consigliato

Ogni file usa campi separati da tabulazione:

1. `ID`
2. `Front`
3. `Back`
4. `Notes`
5. `ExampleRu`
6. `ExampleIt`
7. `Tags`

I vecchi TSV in `old_anki/` hanno solo i primi quattro campi e `Tags`.

Durante l'import in Anki:

- scegli `Tipo di nota`: un tipo di nota che includa anche il campo `ID`
- seleziona `Campi separati da tab`
- mappa i campi nell'ordine sopra
- se vuoi, crea un mazzo diverso per ogni file
- usa `ID` come campo stabile per aggiornare le note senza creare duplicati

## Note utili

- Puoi usare HTML semplice dentro i campi, ad esempio `<br>` per andare a capo.
- Per audio o immagini, Anki accetta riferimenti come `[sound:file.mp3]` o `<img src="immagine.png">` se i file sono nella collection.
- Non cambiare gli `ID` dopo il primo import, altrimenti Anki considererà le righe come nuove note.

## Liste lezioni

Lo script `scripts/generate_anki_from_liste.py` legge i file in `lezioni/lista*`.

- Formato base: `russo<TAB>italiano<TAB>tema`
- Formato con ID stabile: `russo<TAB>italiano<TAB>tema<TAB>card_id`
- Formato con frase d'esempio: `russo<TAB>italiano<TAB>tema<TAB>card_id<TAB>frase_russa<TAB>traduzione_frase`

Le frasi d'esempio generano una terza carta, **Frase → Traduzione**. Sul fronte compaiono la parola e la frase russa, con la parola evidenziata; sul retro la traduzione della parola e quella della frase tra parentesi. Le righe senza frase mantengono soltanto le due carte esistenti.

### Evidenziare le forme flesse

Nella colonna `frase_russa`, racchiudi tra `**` la parola o l'espressione da evidenziare:

```text
знать	sapere	verbi	znat	Я **знаю** ответ.	So la risposta.
отвечать за	essere responsabile di	verbi	otvechat-za	Менеджер **отвечает за** работу команды.	Il manager è responsabile del lavoro della squadra.
```

Puoi indicare più parti: `Я **хочу** читать, а брат **хочет** гулять.`
I marcatori non compaiono nelle carte: il generatore li converte in evidenziazione colorata.
Il resto del testo resta invariato e viene trattato come testo, non come HTML.

Senza marcatori, viene evidenziata la forma esatta del lemma (ignorando maiuscole e punteggiatura finale come `?`). Non vengono indovinate automaticamente le forme flesse. Se il lemma non compare o i marcatori sono malformati, la generazione si ferma indicando file e riga, prima di modificare gli output.

Rigenera entrambi i file con `python3 scripts/generate_anki_from_liste.py`.
L'evidenziazione riguarda solo `ExampleRu`: ID, campi e template delle due carte di vocabolario rimangono invariati.

Se aggiungi `card_id` a una riga, quello verra' usato come `ID` Anki della carta cumulativa anche se in futuro cambi `russo`, `italiano` o `tema`.

Per migrare automaticamente gli ID esistenti dentro le `lezioni/lista*`, usa:

```bash
python3 scripts/migrate_card_ids_from_tsv.py
```

Per default lo script legge prima `anki/A1.tsv` e poi `anki/vocabolario.tsv`. Puoi anche indicare esplicitamente la sorgente:

```bash
python3 scripts/migrate_card_ids_from_tsv.py --source anki/A1.tsv
```

Se vuoi assegnare automaticamente un `card_id` anche ai termini che non esistono ancora nel TSV sorgente:

```bash
python3 scripts/migrate_card_ids_from_tsv.py --fill-missing
```
