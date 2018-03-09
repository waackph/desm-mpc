# desm-mpc

## Minimale Anforderung
1. word2vec-Model nutzen / word-embeddings extrahieren
2. "word perturbation analysis“-Experimenten-Setting in Python nachbilden zur Validierung der korrekten Implementierung. (Versuchsdaten sind im Paper, word2vec-Embbedings sind auf verfügbar. Weitere Experimente im Paper sind leider nicht reproduzierbar, da eine zufällige Auswahl von Daten aus "Bing’s large scale query logs“ verwendet wurde)
3. word-embeddings & DESM nach C portieren (zur weiteren Benutzung in Obliv-C)

## Optionale Ziele
1. Obliv-C Umsetzung des DESM-Rankers
2. Lineare Regression beispielhaft implementieren [5] (zur Einarbeitung)
3. DESM-Berechnung aufteilen in lokale und MPC-basierte Berechnungen
4. 2-Party-Case mit Obliv-C implementieren
5. Erneute Ausführung des word perturbation analysis“-Experiments mit Obliv-C Implementierung - Vergleich mit einfacher C DESM-Implementation.
6. Kombination von TF-IDF-Text-Repräsentation BM25 und dem DESM, da DESM alleine schlecht abschneidet auf großen Dokumentenmengen [3]
