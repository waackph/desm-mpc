# desm-mpc

Studienarbeit: Sichere dezentrale Berechnung eines Dokument-Ranking-Ansatzes

Ziel: Relevanz-basierte Suche auf Basis des Dual Embedding Space Models (DESM) als sichere Multi-Party-Computation Umsetzung.

## Minimale Anforderung
1. word2vec-Model nutzen / word-embeddings extrahieren
2. "word perturbation analysis“-Experiment-Setting in Python nachbilden zur Validierung der korrekten Implementierung. (Versuchsdaten sind im Paper, word2vec-Embbedings sind auf verfügbar. Weitere Experimente im Paper sind leider nicht reproduzierbar, da eine zufällige Auswahl von Daten aus "Bing’s large scale query logs“ verwendet wurde)
3. word-embeddings & DESM nach C portieren (zur weiteren Benutzung in Obliv-C)

## Optionale Ziele
1. Lineare Regression beispielhaft implementieren (zur Einarbeitung)
2. DESM-Berechnung aufteilen in lokale und MPC-basierte Berechnungen
3. 2-Party-Case mit Obliv-C implementieren
4. Erneute Ausführung des word perturbation analysis“-Experiments mit Obliv-C Implementierung - Vergleich mit einfacher C DESM-Implementation.
5. Kombination von TF-IDF-Text-Repräsentation BM25 und dem DESM, da DESM alleine schlecht abschneidet auf großen Dokumentenmengen
