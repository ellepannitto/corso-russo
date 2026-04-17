# File per Anki

Questa cartella contiene file `TSV` pronti da importare in Anki.

## Formato consigliato

Ogni file usa campi separati da tabulazione:

1. `ID`
2. `Front`
3. `Back`
4. `Notes`
5. `Tags`

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
