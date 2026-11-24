"""Punto de entrada de la herramienta."""

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="static-security-scanner",
        description="Escáner de seguridad para proyectos de microservicios.",
    )
    parser.parse_args()
    parser.print_help()
