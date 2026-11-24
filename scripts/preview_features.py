"""Muestra la transformación TF-IDF desde la terminal."""

import sys

from static_security_scanner.cli import main

if __name__ == "__main__":
    main(["preview-features", *sys.argv[1:]])
