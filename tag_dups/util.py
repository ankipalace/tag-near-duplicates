import random
import re
import string
import uuid

import pandas as pd

from bs4 import BeautifulSoup

# TODO: Remove dependency
from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words("english"))
RD = random.Random()
RD.seed(0)


def read_notes(notes_file):
    """
    `notes_file` is expected to have been exported from Anki in plain text format, including HTML
    and media references.
    :param notes_file:
    :return: pd.DataFrame
    """
    df = pd.read_csv(notes_file, names=["id", "html"], usecols=[0, 1], sep="\t")
    return df


def pre_process(df: pd.DataFrame):
    df.drop_duplicates(inplace=True)

    # Create a column without HTML
    df["text"] = df["html"].apply(lambda x: BeautifulSoup(x, "html.parser").get_text())

    # Remove cloze deletion syntax and sound references
    pat = re.compile("{{c[0-9]*::")
    df["clean"] = df["text"].str.replace(pat, " ").str.replace("}}", " ")
    df["clean"] = df["clean"].str.replace(f"sound|mp3", " ")

    # Remove punctuation and lower
    df["clean"] = df["clean"].str.replace(f"[{string.punctuation}]", " ")
    df["clean"] = df["clean"].str.replace("\s+", " ").str.strip()
    df["clean"] = df["clean"].str.lower()

    df["set"] = df["clean"].apply(get_set)

    # TODO: Tag duplicates as per the `set` column at this point
    df.sort_values(by=["set"], inplace=True)
    df.set_index("id", inplace=True)

    bad_ix = []
    for ix in df.index.tolist():
        if not isinstance(ix, int):
            try:
                int(ix.strip('-'))
            except ValueError:
                bad_ix.append(ix)
    df.drop(bad_ix, inplace=True)

    return df


def get_set(x):
    """Remove stopwords and populate new column `set` with the sorted set of elements in
    `clean`
    """
    x = set(x.split()) - STOPWORDS
    x = " ".join(sorted(x))

    def repl(m):
        return ""

    p = re.compile("^[0-9]+[a-z]* *")
    while matches := re.match(p, x):
        x = re.sub(p, repl, x)
        x = f"{x} {' '.join(matches.group(0))}"
    return x


def generate_tag(prefix="duplicate", category="", score=""):
    id_ = uuid.UUID(int=RD.getrandbits(128))
    prefix = f"{prefix}::{category}::" if category else f"{prefix}::"
    prefix = f"{prefix}::{score}::" if score else prefix
    tag = f"{prefix}{id_}"
    return tag
