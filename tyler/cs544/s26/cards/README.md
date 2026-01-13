# CS544 Anki Flashcards

Topic-based Anki decks for CS544.

## Decks

| Deck | Cards | Topics |
|------|-------|--------|
| deck-01-foundations | 95 | systems intro, shell, docker |
| deck-02-networking | 39 | networking, gRPC |
| deck-03-memory | 17 | CPU caching, Arrow |
| deck-04-compute | 26 | threads, locks |
| deck-05-storage | 21 | file systems, file formats |
| deck-06-sql | 9 | SQL basics |
| deck-07-hdfs | 16 | HDFS |
| deck-08-spark | 49 | Spark |
| deck-09-cassandra | 36 | Cassandra |
| deck-10-kafka | 38 | Kafka |
| deck-11-cloud | 41 | cloud, BigQuery |

## Regenerating .apkg files

```bash
python3 -m venv venv
source venv/bin/activate
pip install genanki
python create_apkg.py
```

Output goes to `apkg/`.

## Editing cards

Edit the JSON files in `decks/`. Each card has:
- `front`: question (HTML)
- `back`: answer (HTML)
- `source_lecture`: original lecture (for reference)

Then regenerate the .apkg files.
