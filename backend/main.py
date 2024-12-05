import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from classes.Reader import Reader
from classes.Analyzer import Analyzer
from classes.ConfigurationManager import ConfigurationManager

import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-c', '--configuration',
        metavar='FILE',
        default='configuration.yml',
        type=str,
        help=' location to of the configuration file (default: configuration.yml)')

    args = parser.parse_args()

    abs_path = Path(__file__).resolve().parent

    cm = ConfigurationManager(args.configuration, abs_path)
    reader = Reader(cm, abs_path)
    analyzer = Analyzer(reader, cm)
    data = analyzer._Analyzer__analyze()
    return data
    # print(data)

if __name__ == '__main__':
    try:

        main()
        sys.exit()
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')
