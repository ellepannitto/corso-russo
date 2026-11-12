# TODO

## Lista `gatti_ermitage.tsv`

- [x] Rileggere le 134 carte, soprattutto frasi e traduzioni scritte da Claude
- [x] Controllare `кормушка` (la slide era tagliata)
- [x] Decidere se tenere `турецкая кошка` (slide e foto non coincidono: la slide dice «короткошёрстная», la foto mostra un gatto a pelo lungo)
- [x] Decidere il nome/numero della lista (ora è descrittivo, come `seminario_morte.tsv`)
- [ ] Decidere su `schitat-ritenere`: tenerla separata o unirla alla carta di lista8 («contare»)
- [ ] Aggiungere, se servono, le parole saltate: Леонардо, Казань, благополучие

## Integrazione in Anki

- [ ] Aggiungere `gatti_ermitage.tsv` alla generazione del mazzo (verificare come `scripts/generate_anki_from_liste.py` legge i `.tsv`)
- [ ] Far passare `tests/test_example_highlighting.py`
- [ ] Importare il mazzo in Anki e controllare qualche carta nuova

## Pulizia delle liste esistenti

- [ ] Convertire `lista40.tsv` e `vocaboli_vari.tsv` da CRLF a LF
- [ ] Togliere i duplicati nella stessa lista: `столовая`, `уютный` (lista21), `обычно` (lista8), `блюдо` (lista11), `семья` (lista3)
- [ ] Separare con `/` o `,` le traduzioni accostate (`storia racconto`, `è vietato non si può`, `si deve bisogna`, `naturalmente certamente`, `troppo eccessivamente`, `tranquillo silenzioso`, `particolare insolito`, `rumorosamente a voce-alta`)
- [ ] Distinguere i due significati di `столовая` («mensa» / «sala da pranzo») con id diversi
- [ ] Sostituire spazi e underscore negli id con trattini e correggere `Bog` (lista15, lista16, lista17, lista19, lista20, lista21, `vocaboli_vari.tsv`)
- [ ] Scegliere un'unica regola di translitterazione (`-ый`/`-ий`/`-ой`, `х`, `ц`, `я`, `ь`) e allineare gli id (vedi `scripts/transliterate_card_ids.py`)
- [ ] Decidere se migrare o rifare le carte già importate in Anki (cambiare l'id cambia il `guid`)
- [ ] Unificare le 56 categorie in circa 20–25 (`cibo`→`cibo-e-bevande`, `viaggi`/`trasporti`→`viaggi-e-trasporti`, `natura`→`natura-e-luoghi`, `persone`→`persone-e-famiglia`, `tempo`/`tempo-e-stagioni`→`tempo-e-date`, …)
- [ ] Decidere cosa fare con le circa 170 parole ripetute tra liste
- [ ] Uniformare o distinguere con id diversi le traduzioni incoerenti: `шуба`, `курица`, `учить`, `сидеть`, `печь`, `парень`/`девушка`, `дети`
- [ ] Decidere cosa fare di `extra` (125 parole, 3 colonne): lista vera o appunti

## Controllo finale

- [ ] Rileggere frasi e traduzioni delle liste esistenti per errori di grammatica
