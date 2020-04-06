import uuid
import os
import random
import string

import click

from fuzzywuzzy import fuzz, process

from util import read_notes

RD = random.Random()
RD.seed(0)


def punctuation(notes_file):
    """
    Tag cards that are identical when punctuation is removed.
    :param notes_file:
    :return:
    """
    df = read_notes(notes_file)
    for text, row in df.iterrows():
        clean = df.loc[text]['clean']
        dups = df[df['clean'] == clean]
        if len(dups) > 1:
            tag_prefix = generate_tag_prefix()
            df.loc[dups.index, 'near-dup'] = f"near-dup::punctuation::{tag_prefix}"
            x_dups = int(len(df[df['near-dup'].notnull()]) / 2)
            print(f"found {x_dups:0} duplicates")
    out_file = f"{notes_file.strip('text')}_punctuation.txt"
    all_dups = df[df['near-dup'].notnull()].sort_values("clean")
    all_dups.drop(columns="clean", inplace=True)
    all_dups.to_csv(out_file)


@cli.command()
@click.argument("notes_file", type=click.Path(exists=True))
def fuzzy(notes_file):

    out_file = f"{notes_file.strip('.txt')}_fuzzy_dups.txt"
    try:
        os.remove(out_file)
    except FileNotFoundError:
        pass

    df = read_notes(notes_file)
    cards = set(row["text"] for ix, row in df.iterrows())
    x = 0
    match_counter = 0
    for ix, row in df.iterrows():
        card_text = str(row["text"])
        x += 1
        try:
            # If this fails, then `card_text` has already been seen
            cards.remove(card_text)
            matches = [
                name for name, score
                # TODO: Test if setting limit=1 gets any speedup
                in process.extract(card_text, cards, scorer=fuzz.ratio)
                if score > 90  # TODO: Make configurable
            ]
        except KeyError:
            continue
        if matches:
            match_counter += 1
            print(f"Found {match_counter} potential duplicates so far")
            tag_prefix = generate_tag_prefix()
            df.loc[df["text"].isin(matches + [card_text]), "near_dup"] = f"near_dup::{tag_prefix}"
            df[df['near_dup'].notnull()].to_csv(out_file)
            print(card_text)
            for match in matches:
                print(match)
                try:
                    cards.remove(match)
                except KeyError:
                    continue
            print(f"checked {x} cards out of {len(df)}")
            print(f"checking against {len(cards)} cards now")


def generate_tag_prefix():
    tag = uuid.UUID(int=RD.getrandbits(128))  # TODO Prefix tag with score for ordering
    return tag
