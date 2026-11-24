# StaticSecurityScanner

Proyecto de Desarrollo de Software Seguro para analizar código y configuraciones de microservicios y clasificar posibles hallazgos según OWASP Top 10:2025 y OWASP API Security Top 10:2023. El alcance inicial contempla Java y Python.

## Instalación

Se requiere Python 3.10 o posterior.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[semma]'
static-security-scanner --help
jupyter lab
```

## Estado del avance

- `src/static_security_scanner/` contiene el punto de entrada de la CLI. El comando muestra la ayuda.
- `data/` contiene el esquema del dataset piloto, el diccionario de datos y la plantilla de correspondencias CWE–OWASP.
- `notebooks/` contiene guías de trabajo para Sample, Explore y Modify.

El primer hito contempla poblar el piloto, documentar sus fuentes, explorar su distribución y preparar una muestra de la transformación TF-IDF. El entrenamiento, la evaluación, el análisis de proyectos y la exportación de reportes quedan pendientes.
