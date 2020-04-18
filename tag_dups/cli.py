import pandas as pd

from .util import read_notes, pre_process
import tag_dups.tag_duplicates as tag_duplicates

import click


@click.group()
def cli():
    pass


@cli.command()
@click.argument("df1", type=click.Path(exists=True))
@click.argument("df2", type=click.Path(exists=True))
@click.option("--o-duplicates", default="dups.txt", type=click.Path(exists=False))
@click.option("--threshold", default=90)
@click.option("--append/--no-append", default=True)
def fuzzy_dups(df1, df2, o_duplicates, threshold, append):
    df1 = read_notes(df1)
    df1 = pre_process(df1)
    df1 = tag_duplicates.simple_dups(df1)

    df2 = read_notes(df2)
    df2 = pre_process(df2)
    df2 = tag_duplicates.simple_dups(df2)

    df = tag_duplicates.fuzzy_dups(df1, df2, o_duplicates, threshold=threshold, append=append)


@cli.command()
@click.argument("df1", type=click.Path(exists=True))
@click.argument("df2", type=click.Path(exists=True))
@click.option("--o-duplicates", default="dups.txt", type=click.Path(exists=False))
def simple_dups(df1, df2, o_duplicates):

    df1 = read_notes(df1)
    df1 = pre_process(df1)

    df2 = read_notes(df2)
    df2 = pre_process(df2)

    merged = pd.concat([df1, df2])
    merged = tag_duplicates.simple_dups(merged)
    merged[merged.duplicate.notnull()].to_csv(o_duplicates)
