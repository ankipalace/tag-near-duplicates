from tag_dups.cli import fuzzy_dups


from click.testing import CliRunner


def test_tag_dups():
    runner = CliRunner()
    result = runner.invoke(fuzzy_dups, ["data/step1-slice.txt", "--no-append"])
    assert result.exit_code == 0
