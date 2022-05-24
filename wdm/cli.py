"""Console script for wdm."""
import argparse
import sys
from typing import List, Optional

from wdm import __version__

def main():
    """Command line application to manage webOS Emulators"""
    parser = argparse.ArgumentParser(description=main.__doc__)
    args = _parse_args(parser)

    parser.print_help()

    return 0

def _parse_args(parser: argparse.ArgumentParser, args: Optional[List] = None) -> argparse.Namespace:
    parser.add_argument(
        "--version", action="version", version="%(prog)s " + __version__,
    )

    return parser.parse_args(args)

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
