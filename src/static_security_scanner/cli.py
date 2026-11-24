"""Punto de entrada de la herramienta."""

import argparse
import json
from pathlib import Path

from . import pilot
from .discovery import discover_project


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="static-security-scanner",
        description="Escáner de seguridad para proyectos de microservicios.",
    )
    commands = parser.add_subparsers(dest="command")
    for name, description in (
        ("demo", "Ejecuta las tres etapas del piloto SEMMA"),
        ("validate-pilot", "Valida el CSV piloto"),
        ("explore-pilot", "Genera los gráficos del piloto"),
        ("preview-features", "Muestra la transformación TF-IDF"),
    ):
        command = commands.add_parser(name, help=description, description=description)
        command.add_argument("--input", type=Path, default=Path("data/pilot.csv"), help="CSV del piloto")
        if name in {"demo", "explore-pilot"}:
            command.add_argument("--output", type=Path, default=Path("reports/pilot"), help="Carpeta de gráficos")

    discover = commands.add_parser(
        "discover", help="Inventaría servicios candidatos y archivos fuente"
    )
    discover.add_argument("project", type=Path, nargs="?", default=Path("."))

    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return

    try:
        if args.command == "discover":
            print(json.dumps(discover_project(args.project), ensure_ascii=False, indent=2))
            return

        rows = pilot.validate(args.input)
        print(f"Validación: {len(rows)} registros válidos en {args.input}")
        if args.command in {"demo", "explore-pilot"}:
            pilot.explore(rows, args.output)
            print(f"Gráficos guardados en {args.output}")
        if args.command in {"demo", "preview-features"}:
            pilot.preview_features(rows)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")
    except ModuleNotFoundError as error:
        parser.exit(1, f"Falta {error.name}. Instala las dependencias con pip install -e '.[semma]'.\n")
