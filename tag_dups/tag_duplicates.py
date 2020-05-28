import pandas as pd

from fuzzywuzzy import fuzz, process

from .util import generate_tag


def simple_dups(df) -> pd.DataFrame:
    cards = set(row["set"] for ix, row in df.iterrows())

    for ix, row in df.iterrows():
        text = row["set"]
        if text in cards:
            dups = df[df.set == text].index
            if len(dups) > 1:
                tag = generate_tag(category="simple")
                df.loc[dups, "duplicate"] = tag
            try:
                cards.remove(text)
            except KeyError:
                pass
    return df


def fuzzy_dups(df: pd.DataFrame, out_file="dups.txt", append=True, threshold=90):
    """
    :param df:
    :param out_file:
    :param append:
    :param threshold:
    :return: df
    """

    # TODO: Don't mutate df

    # Get all clean card text from the DataFrame and put it in a set
    # We need this copy as a set so that we can quickly remove cards as they are found
    # and only check for duplicates against the ever shrinking set

    total_cards = len(df)
    try:
        remaining = df[df.duplicate.isnull()]
    except AttributeError:
        # There weren't any duplicates found in previous step
        remaining = df

    cards = set(row["clean"] for ix, row in df.iterrows())
    x, match_counter = 0, 0
    for ix, row in remaining.iterrows():
        text = str(row["clean"])
        x += 1
        # Remove card_text from set, otherwise it will always look like a duplicate.
        try:
            cards.remove(text)
        except KeyError:
            pass

        if not cards:
            break

        matches = []
        for name, score in process.extract(text, cards, scorer=fuzz.ratio):
            if score > threshold:
                matches.append(name)

        if matches:
            match_counter += 1
            tag = generate_tag(category="fuzzy", score=str(threshold))
            # Get the indices of all matches in the DataFrame
            match_locations = remaining["clean"].isin(matches + [text])
            # Assign the same tag to matches
            remaining.loc[match_locations, "duplicate"] = tag
            if append:
                these_matches = remaining[remaining.duplicate == tag]
                these_matches.to_csv(out_file, mode="a")

            print(f"Found {match_counter} potential duplicates so far")
            print(f"Identified the following potential duplicates:")
            print(text)

            for match in matches:
                try:
                    print(match)
                    cards.remove(match)
                except KeyError:
                    continue

            print(f"checked {x} cards out of {total_cards}")
            print(f"Checking against {len(cards)} cards now")

    all_matches = pd.concat([remaining, df])

    try:
        all_matches = all_matches[all_matches.duplicate.notnull()]
        all_matches.to_csv(out_file)
    except AttributeError:
        print("No duplicates")
    return all_matches
