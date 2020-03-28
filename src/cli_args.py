import argparse
from enum import Enum


class OutputFormat(Enum):
    html = 'html'
    json = 'json'

    def __str__(self):
        return self.value


class CLIArgs:

    CONFIRMED_COMMAND = "confirmed"
    RECOVERED_COMMAND = "recovered"
    DEATHS_COMMAND = "death"

    @classmethod
    def read_args(cls, argv):
        # Common args
        common_args = argparse.ArgumentParser(add_help=False)
        common_args.add_argument('--verbose', dest='verbose', action='count', help="Add verbosity")
        common_args.add_argument('--format', '-f', dest='format', nargs='?', type=OutputFormat, choices=list(OutputFormat))
        common_args.add_argument('--output', '-o', dest='output', nargs='?', help="File path")

        # retrieve_routers args
        confirmed_case_parser = argparse.ArgumentParser(add_help=False)
        confirmed_case_parser.add_argument('--all', dest='show all charts', action='store_true',
                                           help="show all charts")

        # creating sub argparser to reuse arguments and differentiate commands
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(title="commands", dest="command")

        # retrieve_routers
        parser_confirmed = subparsers.add_parser(cls.CONFIRMED_COMMAND, parents=[common_args, confirmed_case_parser],
                                                 help='Show data for confirmed cases.')

        # retrieve_routers
        parser_recovered = subparsers.add_parser(cls.RECOVERED_COMMAND, parents=[common_args, confirmed_case_parser],
                                                 help='Show data for recovered cases.')

        # retrieve_routers
        parser_recovered = subparsers.add_parser(cls.DEATHS_COMMAND, parents=[common_args, confirmed_case_parser],
                                                 help='Show data for deaths cases.')

        return parser.parse_args(argv)
