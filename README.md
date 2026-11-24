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

## Demostración del piloto

Desde la raíz del repositorio, con el entorno activado:

```bash
static-security-scanner demo
```

El comando valida los 24 ejemplos controlados de Java y Python, guarda tres
gráficos en `reports/pilot/` y muestra una vista previa de TF-IDF. La vista
previa reserva proyectos completos y ajusta el vectorizador con el resto.
En JupyterLab puedes abrir los PNG desde el panel de archivos.

Las etapas también se pueden ejecutar por separado:

```bash
python scripts/validate_pilot.py
python scripts/explore_pilot.py
python scripts/preview_features.py
```

El diccionario y la procedencia del piloto están en `data/`. Los notebooks
incluyen celdas ejecutables para Sample, Explore y Modify. El entrenamiento, la
evaluación y el escaneo de repositorios quedan pendientes.

## Inventario preliminar de un proyecto

```bash
static-security-scanner discover .
```

El comando imprime un inventario JSON de directorios candidatos según sus
manifiestos y de archivos fuente Python, JavaScript y TypeScript. Un
`pom.xml` identifica un directorio candidato. Los archivos `.java` quedan
fuera del inventario actual. El comando solo examina rutas.
