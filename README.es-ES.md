# DataPulse

> Una pequeña automatización en Python que convierte una API pública de noticias en archivos útiles.

DataPulse consulta la API pública de búsqueda de Hacker News, limpia las historias recibidas y exporta dos archivos: un CSV que se puede abrir en Excel y un resumen JSON con métricas básicas.

Este es el segundo proyecto de portfolio después de VoteFlow. Es intencionadamente pequeño: el objetivo es practicar Python, peticiones HTTP, estructuras de datos, gestión de errores y automatización sin esconder la lógica detrás de un framework grande.

## Funcionalidades

- Buscar historias por tema.
- Elegir la cantidad de resultados desde la línea de comandos.
- Exportar datos CSV en UTF-8.
- Generar un resumen JSON con puntos, comentarios y autores frecuentes.
- Mostrar mensajes claros cuando hay errores de red o de entrada.

## Requisitos

- Python 3.10 o posterior.
- Conexión a Internet durante la recopilación.

El proyecto utiliza únicamente la biblioteca estándar de Python, por lo que no hay que ejecutar `pip install`.

## Ejecutarlo

```bash
python datapulse.py --query python --limit 20
```

También puedes probar otro tema:

```bash
python datapulse.py --query javascript --limit 50
```

Los archivos generados aparecen en `output/`:

- `stories.csv`: filas limpias para Excel o Google Sheets.
- `summary.json`: totales y los cinco autores más frecuentes.

## Qué ocurre internamente

1. `argparse` lee la búsqueda y el límite desde el terminal.
2. `urllib` envía una petición HTTP a la API pública.
3. La respuesta JSON se transforma en una lista de diccionarios coherente.
4. `csv.DictWriter` convierte esa lista en un archivo compatible con hojas de cálculo.
5. `Counter` y `json.dumps` generan el informe de resumen.

## Estructura del proyecto

```text
datapulse/
├── datapulse.py       # CLI, petición a la API, limpieza y exportaciones
├── output/            # Archivos generados al ejecutar el script
└── README.md
```

## Uso responsable

DataPulse utiliza la API pública de búsqueda de Hacker News en lugar de raspar páginas web. Envía un identificador de cliente, define un tiempo máximo de espera y limita el número de registros. Antes de adaptar el script a otra fuente, revisa siempre sus condiciones de uso y sus límites de peticiones.

## Qué se practica

Funciones de Python, listas y diccionarios, argumentos de línea de comandos, peticiones HTTP, JSON, CSV, rutas de archivos, contadores, fechas UTC, validación y gestión de errores.

---

La documentación en inglés está disponible en [README.md](README.md).
