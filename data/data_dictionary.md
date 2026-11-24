# Diccionario de datos

Cada fila de `pilot.csv` representa un fragmento de código o configuración con una etiqueta revisada. Ambos CSV contienen únicamente sus encabezados.

| Campo | Descripción |
| --- | --- |
| `id` | Identificador único del registro. |
| `source_project` | Proyecto de origen. Permite agrupar registros al dividir el dataset. |
| `source_ref` | URL y revisión o versión de origen. |
| `source_path` | Ruta del archivo y, cuando se conoce, rango de líneas. |
| `language` | Lenguaje del código o formato de la configuración. |
| `artifact_type` | Tipo de fragmento, como `source`, `api` o `config`. |
| `content` | Contenido del fragmento. |
| `is_vulnerable` | `1` para un caso vulnerable y `0` para un caso sin la debilidad evaluada. |
| `cwe_ids` | Identificadores CWE aplicables. |
| `owasp_web_ids` | Identificadores de OWASP Top 10:2025 aplicables. |
| `owasp_api_ids` | Identificadores de OWASP API Security Top 10:2023 aplicables. |

Los campos de identificadores admiten varios valores separados por `|`. Un campo vacío indica que no se asignó ninguna etiqueta de ese catálogo. El CSV de correspondencias registra una relación por fila, con su fuente y las condiciones de aplicación.
