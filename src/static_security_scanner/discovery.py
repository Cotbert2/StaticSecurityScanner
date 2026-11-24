"""Descubrimiento preliminar por manifiestos; no detecta vulnerabilidades."""
import os
from pathlib import Path

MANIFESTS = {"package.json", "pom.xml", "requirements.txt", "pyproject.toml"}
LANGUAGES = {".py": "Python", ".js": "JavaScript", ".jsx": "JavaScript",
             ".ts": "TypeScript", ".tsx": "TypeScript"}
EXCLUDED = {".git", "node_modules", ".venv", "venv", "__pycache__",
            "dist", "build", "coverage", ".next", ".venv-jupyter"}


def discover_project(project: Path) -> dict:
    """Inventaría rutas sin ejecutar ni importar código del proyecto objetivo.

    Los directorios con manifiesto son candidatos, no microservicios confirmados.
    No se siguen enlaces simbólicos. Los errores de lectura no se silencian.
    """
    root = Path(project).expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"El proyecto no es un directorio existente: {root}")
    candidates = set()
    sources = []

    def raise_walk_error(error):
        raise error

    for current, directories, filenames in os.walk(
        root, followlinks=False, onerror=raise_walk_error
    ):
        current_path = Path(current)
        directories[:] = sorted(
            name for name in directories
            if name not in EXCLUDED and not (current_path / name).is_symlink()
        )
        regular_files = [
            current_path / name for name in sorted(filenames)
            if not (current_path / name).is_symlink()
            and (current_path / name).is_file()
        ]
        if any(path.name in MANIFESTS for path in regular_files):
            candidates.add(current_path)
        sources.extend(path for path in regular_files if path.suffix in LANGUAGES)

    records = []
    for path in sorted(sources):
        owner = next((parent for parent in path.parents if parent in candidates), None)
        records.append({
            "path": path.relative_to(root).as_posix(),
            "language": LANGUAGES[path.suffix],
            "candidate_service": owner.relative_to(root).as_posix() if owner else None,
        })
    return {
        "status": "inventory_only_not_security_analysis",
        "project_root": str(root),
        "candidate_services": sorted(path.relative_to(root).as_posix() for path in candidates),
        "source_files": records,
    }
