import pandas as pd

from fuzzywuzzy import fuzz, process

from .util import generate_tag


def simple_dups(df: pd.DataFrame) -> pd.DataFrame:
    prefix = "duplicate"
    for ix, row in df.iterrows():
        text = row["set"]
        # TODO: check only for matches in step2?
        dups = df[df["set"] == text]
        if len(dups) > 1:
            tag = generate_tag(prefix=prefix, category="simple")
            df.loc[dups.index, prefix] = tag
    return df


def fuzzy_dups(
    df1: pd.DataFrame, df2: pd.DataFrame, out_file="dups.txt", append=True, threshold=50
):
    """
    :param df1:
    :param df2:
    :param out_file:
    :param append:
    :param threshold:
    :return: df
    """

    # TODO: Don't mutate df

    # Get all clean card text from the DataFrame and put it in a set
    # We need this copy as a set so that we can quickly remove cards as they are found
    # and only check for duplicates against the ever shrinking set

    merged = pd.concat([df1, df2])
    total_cards = len(merged)

    try:
        merged[merged.duplicate.notnull()].to_csv(out_file)
        remaining = merged[merged.duplicate.isnull()]
    except AttributeError:
        # There weren't any duplicates found in previous step
        remaining = merged
        pass

    cards = set(row["clean"] for ix, row in df2.iterrows())
    x, match_counter = 0, 0
    for ix, row in remaining.iterrows():
        card_text = str(row["clean"])
        x += 1
        # Remove card_text from set, otherwise it will always look like a duplicate.
        try:
            cards.remove(card_text)
        except KeyError:
            pass
        matches = []
        for name, score in process.extract(card_text, cards, scorer=fuzz.ratio):
            if score > threshold:
                matches.append(name)

        if matches:
            match_counter += 1
            tag = generate_tag(category="fuzzy")
            # Get the indices of all matches in the DataFrame
            match_locations = remaining["clean"].isin(matches + [card_text])
            # Assign the same tag to matches
            remaining.loc[match_locations, "duplicate"] = tag
            if append:
                these_matches = remaining[remaining["duplicate" == tag]]
                these_matches.to_csv(out_file, mode="a")

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

        try:
            matches_df = remaining[remaining["duplicate"].notnull()]
        except KeyError:
            matches_df = remaining

        matches_df.to_csv(out_file)
        return matches_df
