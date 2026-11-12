import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import generate_anki_from_liste as generator


class ExampleHighlightingTests(unittest.TestCase):
    def test_rendering(self):
        cases = [
            ("Кот, кот!", "кот", '<span class="target-word">Кот</span>, <span class="target-word">кот</span>!'),
            ("Котёнок и кот.", "кот", 'Котёнок и <span class="target-word">кот</span>.'),
            ("Сколько стоит книга?", "сколько стоит?", '<span class="target-word">Сколько стоит</span> книга?'),
            ("Я **хочу** читать, а брат **хочет** гулять.", "хотеть", 'Я <span class="target-word">хочу</span> читать, а брат <span class="target-word">хочет</span> гулять.'),
            ("Он **отвечает за** работу.", "отвечать за", 'Он <span class="target-word">отвечает за</span> работу.'),
            ("В этой **печи** пекут хлеб.", "печь", 'В этой <span class="target-word">печи</span> пекут хлеб.'),
            ("Кот видит **кота**.", "кот", 'Кот видит <span class="target-word">кота</span>.'),
            ('<b>**кот**</b> & "кот"', "кот", '&lt;b&gt;<span class="target-word">кот</span>&lt;/b&gt; &amp; &quot;кот&quot;'),
            ("**<кот>**", "кот", '<span class="target-word">&lt;кот&gt;</span>'),
            ("<кот> &", "кот", '&lt;<span class="target-word">кот</span>&gt; &amp;'),
            ("", "кот", ""),
        ]
        for sentence, word, expected in cases:
            with self.subTest(sentence=sentence):
                self.assertEqual(generator.highlight_word(sentence, word), expected)

    def test_malformed_markers(self):
        for sentence in ("Я **знаю ответ.", "****", "** **", "** кот**", "**кот **", "***кот***"):
            with self.subTest(sentence=sentence), self.assertRaises(ValueError):
                generator.highlight_word(sentence, "кот")

    def test_html_bold_targets(self):
        cases = [
            ("У меня есть <b>кот</b>.", "кот", 'У меня есть <span class="target-word">кот</span>.'),
            ("Я <b>хочу</b> читать.", "хотеть", 'Я <span class="target-word">хочу</span> читать.'),
            ("<b>Это</b> <кот> &", "это", '<span class="target-word">Это</span> &lt;кот&gt; &amp;'),
        ]
        for sentence, word, expected in cases:
            with self.subTest(sentence=sentence):
                self.assertEqual(generator.highlight_word(sentence, word), expected)

    def test_malformed_html_bold_targets(self):
        for sentence in ("Я <b>кот.", "Я кот</b>.", "<b></b> кот", "<b> кот</b>", "<b>кот </b>"):
            with self.subTest(sentence=sentence), self.assertRaises(ValueError):
                generator.highlight_word(sentence, "кот")

    def test_lesson_labels_and_order(self):
        names = ["lista10", "lista2", "lista21bis.tsv", "lista21", "vocaboli_vari.tsv", "lista30.tsv", "gatti_ermitage.tsv"]
        paths = [Path(name) for name in names]
        self.assertEqual(
            [generator.lesson_label(p) for p in sorted(paths, key=generator.lesson_sort_key)],
            ["2", "10", "21", "21bis", "30", "gatti_ermitage", "vocaboli_vari"],
        )

    def test_headers_other_files_and_multiple_themes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            lessons = root / "lezioni"
            lessons.mkdir()
            header = "russo\titaliano\tcategoria\tid\tfrase-russo\tfrase-italiano\n"
            (lessons / "lista1").write_text(
                header + "готовить\tcucinare\tverbi,cibo-e-bevande\tgotovit\tОна <b>готовит</b> суп.\tLei cucina la zuppa.\n",
                encoding="utf-8",
            )
            (lessons / "lista21bis.tsv").write_text(
                header + "кот\tgatto\tanimali\tkot\tУ меня есть <b>кот</b>.\tHo un gatto.\n",
                encoding="utf-8",
            )
            (lessons / "extra").write_text("сандалии\tsandali\tabbigliamento\n", encoding="utf-8")
            output, package = root / "vocabolario-completo.tsv", root / "russo.apkg"
            with patch.multiple(generator, LESSONS_DIR=lessons, APKG_OUTPUT=package):
                generator.main()
                generator.write_import_tsv(generator.collect_notes(), output)
            rows = output.read_text(encoding="utf-8").splitlines()[len(generator.IMPORT_HEADER):]
            tags = {row.split("\t")[1]: row.split("\t")[-1] for row in rows}
            self.assertEqual(len(rows), 2)  # `extra` e le intestazioni sono ignorati
            self.assertEqual(tags["готовить"], "cibo-e-bevande verbi lez-1")
            self.assertEqual(tags["кот"], "animali lez-21bis")

    def test_import_tsv_merges_notes_and_allows_word_only_rows(self):
        import csv

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            lessons = root / "lezioni"
            lessons.mkdir()
            (lessons / "lista1").write_text(
                "кот\tgatto\tanimali\tkot\tУ меня есть <b>кот</b>.\tHo un gatto.\n"
                "дом\tcasa\tcasa-e-oggetti\tdom\n",
                encoding="utf-8",
            )
            (lessons / "lista2").write_text(
                "кот\tmicio\tanimali\tkot\tЭто <b>кот</b>.\tÈ un gatto.\n",
                encoding="utf-8",
            )
            output = root / "vocabolario-completo.tsv"
            with patch.multiple(generator, LESSONS_DIR=lessons):
                generator.write_import_tsv(generator.collect_notes(), output)
            lines = output.read_text(encoding="utf-8").splitlines()
            self.assertEqual(lines[:5], generator.IMPORT_HEADER)
            rows = list(csv.reader(lines[5:], delimiter="\t"))
            by_id = {row[0]: row for row in rows}
            self.assertEqual({len(row) for row in rows}, {6})
            self.assertEqual(by_id["dom"][3:5], ["", ""])  # parola singola: nessuna frase
            self.assertEqual(by_id["dom"][5], "casa-e-oggetti lez-1")
            self.assertEqual(by_id["kot"][2], "gatto / micio")  # significati uniti
            self.assertNotIn("<br>", by_id["kot"][3])  # una sola frase: la prima
            self.assertIn("У меня есть", by_id["kot"][3])
            self.assertEqual(by_id["kot"][4], "Ho un gatto.")
            self.assertEqual(by_id["kot"][5], "animali lez-1 lez-2")

    def test_apkg_and_tsv_share_the_same_note_type(self):
        model = generator.RUSSO_MODEL
        header = generator.IMPORT_HEADER
        self.assertEqual(model.name, header[2].removeprefix("#notetype:"))
        self.assertEqual([f["name"] for f in model.fields], generator.FIELDS)
        self.assertEqual(
            [t["name"] for t in model.templates],
            ["Russo → Italiano", "Italiano → Russo", "Frase → Traduzione"],
        )
        # le carte con frase sono condizionate al campo FraseRusso
        self.assertIn("{{#FraseRusso}}", model.templates[2]["qfmt"])
        self.assertIn(".target-word", model.css)

    def test_missing_target_requires_annotation(self):
        with self.assertRaisesRegex(ValueError, "nessuna occorrenza"):
            generator.highlight_word("Я знаю ответ.", "знать")

    def test_invalid_example_does_not_overwrite_outputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            lessons = root / "lezioni"
            lessons.mkdir()
            (lessons / "lista1").write_text(
                "кот\tgatto\tanimali\tkot\tУ меня есть кот.\tHo un gatto.\n"
                "знать\tsapere\tverbi\tznat\tЯ знаю ответ.\tSo la risposta.\n",
                encoding="utf-8",
            )
            package = root / "russo.apkg"
            package.write_bytes(b"previous package")
            with patch.multiple(generator, LESSONS_DIR=lessons, APKG_OUTPUT=package):
                with self.assertRaisesRegex(ValueError, "lista1:2:"):
                    generator.main()
            self.assertEqual(package.read_bytes(), b"previous package")


if __name__ == "__main__":
    unittest.main()
