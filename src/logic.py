from argparse import ArgumentParser
from datetime import datetime, timedelta
from os import path
from os.path import basename, getsize, splitext


def determine_timestamp(year, file_date):
    """Gets a 'best guess' for the timestamp when the citation occurred.

    Args:
        year (str): Citation year recorded in the Crossref entry.
        file_date (str): Date stamp in file name - based on the date queried in
            crossref when retrieving the citation (YYYY-MM-DD).

    Returns:
        str: Timestamp for citation in the form YYYY-MM-DD.
    """
    timestamp = datetime.strptime(file_date, '%Y-%m-%d')

    if timestamp.year != int(year):
        timestamp = datetime.strptime(year, '%Y')

    return timestamp.strftime('%Y-%m-%d 00:00:00')


def get_options(args):
    """Parse options entered when running a script.

    Args:
        args (List): dicts of arguments to pass to the argument parser.

    Returns:
        Namespace: Each option mapped to its value.
    """
    parser = ArgumentParser()
    for arg in args:
        parser.add_argument(arg.pop('val'), **arg)

    options = parser.parse_args()

    return options


def get_filename(out_dir, file_date, extension):
    """Determine file names for output and cached files."""
    return path.join(out_dir, f'CrossrefCitations_{file_date}.{extension}')


def get_date_from_filename(file_path):
    """Assumes file is named e.g. '{path}/{driver}_{file_date}.csv'. """
    file_name = basename(file_path)
    name, _ = splitext(file_name)
    _, date = name.split('_')

    return date


def generate_dates(start_date, cutoff_date):
    """Yield dates, one day at a time from start_date until cutoff_date."""
    epoch = datetime.strptime(start_date, '%Y-%m-%d')
    cutoff = datetime.strptime(cutoff_date, '%Y-%m-%d')

    while epoch <= cutoff:
        yield epoch
        epoch += timedelta(days=1)


def exists_and_not_empty(filename):
    try:
        return getsize(filename) > 0
    except (AssertionError, OSError):
        return False


def uri_schema_doi(doi):
    return f'info:doi:{doi}'
