import os

import pandas as pd

import click

from fuzzywuzzy import fuzz, process

from util import read_notes, generate_tag


def simple_dups(df: pd.DataFrame) -> pd.DataFrame:
    prefix = "dup"
    for ix, row in df.iterrows():
        text = df.loc[ix]['set']
        dups = df[df['set'] == text]
        if len(dups) > 1:
            tag = generate_tag(prefix=prefix, category="simple")
            df.loc[dups.index, prefix] = tag
    return df


def fuzzy_dups(df: pd.DataFrame, threshold=90):

    # Get all clean card text from the DataFrame and put it in a set
    # We need this copy as a set so that we can quickly remove cards as they are found
    # and only check for duplicates against the ever shrinking set
    total_cards = len(df)
    cards = set(row["clean"] for ix, row in df.iterrows())
    x, match_counter = 0, 0
    for ix, row in df.iterrows():
        card_text = str(row["clean"])
        x += 1
        try:
            # Remove card_text from cards first, otherwise it will always look like a duplicate.
            # If this fails, then `card_text` has already been seen
            cards.remove(card_text)
            matches = [
                name for name, score
                # TODO: Test if setting limit=1 gets any speedup
                in process.extract(card_text, cards, scorer=fuzz.ratio)
                if score > threshold
            ]
        except KeyError:
            continue

        if matches:
            match_counter += 1
            pfx = generate_tag()
            # Get the indices of all matches in the DataFrame
            match_locations = df["clean"].isin(matches + [card_text])
            # Assign the same tag with a UUID to matches
            df.loc[match_locations, "duplicate"] = f"duplicate::{pfx}"
            matches_df = df[df['duplicate'].notnull()]
            matches_df.to_csv(out_file, mode="a")

            print(f"Found {match_counter} potential duplicates so far")
            print(f"Identified the following potential duplicates:")
            print(card_text)
            for match in matches:
                try:
                    print(match)
                    cards.remove(match)
                except KeyError:
                    continue
            print(f"checked {x} cards out of {total_cards}")
            print(f"Checking against {len(cards)} cards now")


def tag_dups(df: pd.DataFrame):
    return df
