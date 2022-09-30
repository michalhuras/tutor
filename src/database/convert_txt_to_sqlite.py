"""Get data from quiz text file and put it into SQLite database file. Database version used in this script: 0.0.1. """
from argparse import ArgumentParser, Namespace

from database.database_manager import add_quiz
from run import get_quiz_model

DATABASE_PATH = 'data/quiz.db'


def create_arg_parser() -> ArgumentParser:
    """Create argument parser. """
    pars = ArgumentParser(description=__doc__)
    pars.add_argument('input_path', type=str, help='path to input text file to be processed')
    pars.add_argument('database_path', type=str, help='path to SQLite database file to be processed')
    return pars


def run(arguments: Namespace):
    """Main function of this script. """
    model = get_quiz_model(arguments.input_path)
    add_quiz(arguments.database_path, model)


if __name__ == '__main__':
    parser = create_arg_parser()
    run(parser.parse_args())
