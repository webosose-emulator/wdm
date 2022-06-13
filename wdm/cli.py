"""Console script for wdm."""
import argparse
import sys
from typing import List, Optional

from wdm import __version__
from wdm import WebosDevice

def main():
    """Command line application to manage webOS Emulators"""
    parser = argparse.ArgumentParser(description=main.__doc__)
    args = _parse_args(parser)
    
    if args.create:
        vm = WebosDevice("webos-imagex")
        vm.create()
    else:
        parser.print_help()

    return 0

def _parse_args(parser: argparse.ArgumentParser, args: Optional[List] = None) -> argparse.Namespace:
    parser.add_argument(
        "--version", action="version", version="%(prog)s " + __version__,
    )
    parser.add_argument(
        "-c",
        "--create",
        action="store_true",
        dest="create",
        help="Create a default webOS device",
    )
    
    return parser.parse_args(args)

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
