from pathlib import Path

from .util import read_notes, pre_process
import tag_dups.tag_duplicates as tag_duplicates

import click


@click.group()
def cli():
    """Identify duplicates in an plain text file exported from Anki. Save the results to a new plain text file which can be imported back into Anki.  Importing this file will add a tag to duplicate notes."""
    pass


@cli.command()
@click.argument("df", type=click.Path(exists=True))
@click.option(
    "--o-duplicates",
    type=click.Path(exists=False),
    help="Path to the output file that will contain notes tagged as duplicates. Import this file into Anki to tag duplicate notes.",
)
@click.option(
    "--threshold",
    type=int,
    default=90,
    help="The strictness threshold. Higher integers will result in a stricter threshold for determining duplicates.",
)
@click.option(
    "--append/--no-append", default=True, help="Append results to existing output file."
)
def fuzzy_dups(df, o_duplicates, threshold, append):
    """Save duplicates identified in DF - a plain text file exported from Anki using a fuzzy matching algorithm, and save to output file."""
    if not o_duplicates:
        o_duplicates = f"{Path(df).stem}_threshold_{threshold}.csv"
    df = read_notes(df)
    df = pre_process(df)
    df = tag_duplicates.simple_dups(df)
    df = tag_duplicates.fuzzy_dups(df, o_duplicates, threshold=threshold, append=append)


@cli.command()
@click.argument("df", type=click.Path(exists=True))
@click.option(
    "--o-duplicates",
    default="dups.txt",
    type=click.Path(exists=False),
    help="Import this file into Anki to tag duplicate notes.",
)
def simple_dups(df, o_duplicates):
    """Identify exact duplicates identified in DF - a plain text file exported from Anki, and save to output file."""
    df = read_notes(df)
    df = pre_process(df)
    df = tag_duplicates.simple_dups(df)
    df[df.duplicate.notnull()].to_csv(o_duplicates)
