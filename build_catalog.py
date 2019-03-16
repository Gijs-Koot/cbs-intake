#! /usr/bin/env python
import logging
import click
from cbs_intake.cat import write_to_file


@click.command()
@click.argument('filename', type=click.Path(exists=False))
def build_catalog(filename):
    """Program that download data from CBS and builds a catalog.
    """

    write_to_file(filename)


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    build_catalog()
