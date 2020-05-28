from .util import read_notes, pre_process
import tag_dups.tag_duplicates as tag_duplicates

import click


@click.group()
def cli():
    pass


@cli.command()
@click.argument("df", type=click.Path(exists=True))
@click.option("--o-duplicates", default="dups.txt", type=click.Path(exists=False))
@click.option("--threshold", default=90)
@click.option("--append/--no-append", default=True)
def fuzzy_dups(df, o_duplicates, threshold, append):
    df = read_notes(df)
    df = pre_process(df)
    df = tag_duplicates.simple_dups(df)
    df = tag_duplicates.fuzzy_dups(df, o_duplicates, threshold=threshold, append=append)


@cli.command()
@click.argument("df1", type=click.Path(exists=True))
@click.argument("df2", type=click.Path(exists=True))
@click.option("--o-duplicates", default="dups.txt", type=click.Path(exists=False))
def simple_dups(df1, df2, o_duplicates):
    df = read_notes(df)
    df = pre_process(df)
    df = tag_duplicates.simple_dups(df)
    df[df.duplicate.notnull()].to_csv(o_duplicates)
