"""Validación, exploración y preprocesamiento del piloto SEMMA."""

import csv
from collections import Counter
from pathlib import Path

REQUIRED = (
    "id", "source_project", "source_ref", "source_path", "language",
    "artifact_type", "content", "is_vulnerable",
)
LABELS = ("cwe_ids", "owasp_web_ids", "owasp_api_ids")


def validate(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        missing = set(REQUIRED + LABELS) - set(reader.fieldnames or [])
        if missing:
            raise ValueError("Columnas faltantes: " + ", ".join(sorted(missing)))
        rows = list(reader)

    if not rows:
        raise ValueError("El CSV no contiene registros.")

    ids = Counter(row["id"] for row in rows)
    fragments = Counter((row["language"], row["content"]) for row in rows)
    errors = []
    for line, row in enumerate(rows, start=2):
        missing_fields = [field for field in REQUIRED if not (row[field] or "").strip()]
        if missing_fields:
            errors.append(f"Fila {line}: campos vacíos: {', '.join(missing_fields)}")
        if None in row or any(row[field] is None for field in LABELS):
            errors.append(f"Fila {line}: cantidad incorrecta de columnas")
        if row["is_vulnerable"] not in {"0", "1"}:
            errors.append(f"Fila {line}: is_vulnerable debe ser 0 o 1")
        if row["is_vulnerable"] == "1" and not any(row[field] for field in LABELS):
            errors.append(f"Fila {line}: caso vulnerable sin etiquetas")
        if ids[row["id"]] > 1:
            errors.append(f"Fila {line}: identificador duplicado")
        if fragments[row["language"], row["content"]] > 1:
            errors.append(f"Fila {line}: fragmento duplicado")

    if errors:
        raise ValueError(f"{len(rows)} registros revisados.\n" + "\n".join(errors))
    return rows


def explore(rows: list[dict[str, str]], output: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    labels = Counter(
        label.strip()
        for row in rows
        for field in ("owasp_web_ids", "owasp_api_ids")
        for label in row[field].split("|")
        if label.strip()
    )
    charts = {
        "vulnerabilidad": (
            "Condición evaluada",
            Counter("Vulnerable" if row["is_vulnerable"] == "1" else "No vulnerable" for row in rows),
        ),
        "lenguajes": ("Lenguaje", Counter(row["language"] for row in rows)),
        "owasp": ("Etiquetas OWASP", labels),
    }
    output.mkdir(parents=True, exist_ok=True)
    for filename, (title, counts) in charts.items():
        figure, axis = plt.subplots(figsize=(8, 4), layout="constrained")
        if counts:
            bars = axis.barh(list(counts), list(counts.values()))
            axis.bar_label(bars, padding=3)
            axis.margins(x=0.15)
        else:
            axis.text(0.5, 0.5, "Sin etiquetas", ha="center", transform=axis.transAxes)
        axis.set(title=title, xlabel="Registros")
        figure.savefig(output / f"{filename}.png", dpi=130)
        plt.close(figure)
        print(f"{title}: " + (", ".join(f"{key}={value}" for key, value in counts.items()) or "sin datos"))


def preview_features(rows: list[dict[str, str]]) -> None:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.model_selection import GroupShuffleSplit

    groups = [row["source_project"] for row in rows]
    if len(set(groups)) < 2:
        raise ValueError("La vista previa requiere al menos dos proyectos de origen.")

    train, reserved = next(
        GroupShuffleSplit(n_splits=1, test_size=0.33, random_state=42).split(rows, groups=groups)
    )
    vectorizer = TfidfVectorizer(
        analyzer="char", ngram_range=(3, 5), lowercase=False, max_features=300
    )
    matrix = vectorizer.fit_transform([rows[index]["content"] for index in train])
    names = vectorizer.get_feature_names_out()
    example = rows[train[0]]["id"]
    terms = sorted(zip(matrix[0].indices, matrix[0].data), key=lambda item: -item[1])[:5]
    print(f"TF-IDF: {matrix.shape[0]} fragmentos × {matrix.shape[1]} características")
    print("Proyectos de ajuste: " + ", ".join(sorted({groups[index] for index in train})))
    print("Proyectos reservados: " + ", ".join(sorted({groups[index] for index in reserved})))
    print(f"Términos de {example}: " + ", ".join(f"{names[index]!r} ({weight:.2f})" for index, weight in terms))
