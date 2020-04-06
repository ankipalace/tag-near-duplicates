import re
import string

import pandas as pd

from bs4 import BeautifulSoup


from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words("english"))


def read_notes(notes_file):
    """
    `notes_file` is expected to have been exported from Anki in plain text format, including HTML and media references.
    :param notes_file:
    :return: pd.DataFrame
    """
    df = pd.read_csv(notes_file, names=["id", "html"], usecols=[0, 1], sep="\t")
    return df


def pre_process(df):
    df.drop_duplicates(inplace=True)

    # Create a column without HTML
    df["text"] = df["html"].apply(lambda x: BeautifulSoup(x, "html.parser").get_text())

    # Remove cloze deletion syntax and sound references
    pat = re.compile("{{c[0-9]*::")
    df["clean"] = df["text"].str.replace(pat, " ").str.replace("}}", " ")
    df["clean"] = df["clean"].str.replace(f"sound|mp3", " ")

    # Remove punctuation and lower
    df["clean"] = df["clean"].str.replace(f"[{string.punctuation}]", " ")
    df["clean"] = df["clean"].str.lower()

    df["set"] = df["clean"].apply(get_set)

    # TODO: Tag duplicates as per the `set` column at this point
    df.sort_values(by=["set"], inplace=True)
    df.set_index("id", inplace=True)

    return df


def get_set(x):
    """Remove stopwords and populate new column `set` with the sorted set of elements in
    `clean`
    """
    x = set(x.split()) - STOPWORDS
    x = " ".join(sorted(x))
    p = re.compile("^[0-9]+[a-z]* *")

    def repl(m):
        return ""

    while matches := re.match(p, x):
        x = re.sub(p, repl, x)
        x = f"{x} {' '.join(matches.group(0))}"
    return x
