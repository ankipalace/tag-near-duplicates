from setuptools import setup


setup(
    name="tag_dups",
    version="0.1",
    py_modules=["tag_dups"],
    install_requires=["Click",],
    entry_points="""
        [console_scripts]
        tag-dups=tag_dups.cli:cli
    """,
)
