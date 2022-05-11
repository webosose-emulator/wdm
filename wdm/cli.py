"""Console script for wdm."""
import argparse
import sys


def main():
    """webOS device manager : Command line application to manage webOS Emulators"""
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('_', nargs='*')
    args = parser.parse_args()

    print("Arguments: " + str(args._))
    print("Replace this message by putting your code into "
          "wdm.cli.main")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
