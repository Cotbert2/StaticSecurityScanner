"""Genera gráficos del dataset desde la terminal."""

import sys

from static_security_scanner.cli import main

if __name__ == "__main__":
    main(["explore-pilot", *sys.argv[1:]])
