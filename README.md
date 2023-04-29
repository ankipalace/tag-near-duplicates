# Getting started
- Create a virtual environment
- Install requirements: `python -m pip install requirements/requirements.txt`
- Install the package: `python -m pip install .` (run in the root of this repo)
- Install required data:  `python -c "import nltk;nltk.download('stopwords')"`

# Usage
Use the CLI to view usage details:

```
➜ tag-dups --help
Usage: tag-dups [OPTIONS] COMMAND [ARGS]...

  Identify duplicates in an plain text file exported from Anki. Save the
  results to a new plain text file which can be imported back into Anki.
  Importing this file will add a tag to duplicate notes.

Options:
  --help  Show this message and exit.

Commands:
  fuzzy-dups   Save duplicates identified in DF - a plain text file...
  simple-dups  Identify exact duplicates identified in DF - a plain text...

➜ tag-dups fuzzy-dups --help
Usage: tag-dups fuzzy-dups [OPTIONS] DF

  Save duplicates identified in DF - a plain text file exported from Anki
  using a fuzzy matching algorithm, and save to output file.

Options:
  --o-duplicates PATH     Path to the output file that will contain notes
                          tagged as duplicates. Import this file into Anki to
                          tag duplicate notes.
  --threshold INTEGER     The strictness threshold. Higher integers will
                          result in a stricter threshold for determining
                          duplicates.
  --append / --no-append  Append results to existing output file.
  --help                  Show this message and exit.


```
