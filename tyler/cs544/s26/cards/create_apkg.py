#!/usr/bin/env python3
"""Create .apkg Anki deck files from JSON deck files."""

import json
import random
from pathlib import Path
import genanki

# Create a model (note type) for basic cards
# Using a fixed ID so decks can be updated later
MODEL_ID = 1607392319
BASIC_MODEL = genanki.Model(
    MODEL_ID,
    'CS544 Basic',
    fields=[
        {'name': 'Front'},
        {'name': 'Back'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Front}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Back}}',
        },
    ],
    css='''
    .card {
        font-family: arial;
        font-size: 20px;
        text-align: center;
        color: black;
        background-color: white;
    }
    '''
)

# Deck IDs - using fixed IDs so decks can be updated
DECK_IDS = {
    'foundations': 2059400110,
    'networking': 2059400111,
    'memory': 2059400112,
    'compute': 2059400113,
    'storage': 2059400114,
    'sql': 2059400115,
    'hdfs': 2059400116,
    'spark': 2059400117,
    'cassandra': 2059400118,
    'kafka': 2059400119,
    'cloud': 2059400120,
}


def create_deck_from_json(json_path, output_dir):
    """Create an .apkg file from a JSON deck file."""
    with open(json_path) as f:
        data = json.load(f)

    deck_num = data['deck_number']
    topic = data['topic']
    cards = data['cards']

    # Create deck with consistent ID
    deck_id = DECK_IDS.get(topic, random.randrange(1 << 30, 1 << 31))
    deck_name = f"CS544::{deck_num}-{topic}"
    deck = genanki.Deck(deck_id, deck_name)

    # Add notes
    tag = f"cs544-{topic}"
    for card in cards:
        note = genanki.Note(
            model=BASIC_MODEL,
            fields=[card['front'], card['back']],
            tags=[tag],
        )
        deck.add_note(note)

    # Write .apkg file
    output_filename = f"deck-{deck_num}-{topic}.apkg"
    output_path = output_dir / output_filename
    genanki.Package(deck).write_to_file(output_path)

    return output_filename, len(cards)


def main():
    decks_dir = Path('/Users/tharter/scratch/cards/decks')
    output_dir = Path('/Users/tharter/scratch/cards/apkg')
    output_dir.mkdir(exist_ok=True)

    print("=== CREATING APKG FILES ===\n")

    json_files = sorted(decks_dir.glob('deck-*.json'))
    total = 0

    for json_path in json_files:
        filename, count = create_deck_from_json(json_path, output_dir)
        print(f"Created {filename} ({count} cards)")
        total += count

    print(f"\nTotal: {total} cards in {len(json_files)} decks")
    print(f"\nOutput directory: {output_dir}")


if __name__ == '__main__':
    main()
