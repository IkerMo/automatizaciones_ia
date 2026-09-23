# Automatizaciones IA aplicadas a Restructuring

Repositorio personal de aprendizaje y desarrollo de herramientas de IA aplicadas a tareas de corporate finance y restructuring. Verano 2026.

## Objetivo

Construir tres herramientas funcionales que asisten a un consultor de restructuring en tareas habituales:

1. Extractor de sumas y saldos → modelo IBR base
2. Generador de sección sectorial de informes
3. Tercera herramienta (a decidir en función del feedback)

El objetivo no es vender este verano, sino dominar la materia y construir un portfolio público enseñable.

## Stack

- **Lenguaje:** Python 3.12
- **LLM:** Groq (Llama 3.3) en Fase 1, posible migración a Claude en Fase 2
- **Librerías principales:** `groq`, `python-dotenv`, `pydantic`, `python-docx`, `openpyxl`, `pdfplumber`, `python-pptx`

## Estructura del repositorio

```
automatizaciones_ia/
├── ejercicios/         # Ejercicios de aprendizaje por fase
├── herramienta_1/      # (pendiente) Extractor SyS → IBR
├── herramienta_2/      # (pendiente) Generador sectorial
├── herramienta_3/      # (pendiente)
└── test_conexion.py    # Script de prueba de API
```

## Bitácora

### Semana 1 — Fundamentos

**Día 1 (3 de Junio de 2026):** setup del entorno completado. Python 3.12.6, venv funcionando, repo en GitHub, conexión a API verificada.

Problemas encontrados y resueltos:
- El comando `python` estaba secuestrado por el alias de la Microsoft Store en Windows 11. Solución: usar `py` fuera del venv y desactivar el alias.
- Google AI Studio generaba claves con prefijo `AQ.` en lugar de `AIza`, incompatibles con el SDK oficial. Tras confirmar que era un problema conocido del lado de Google y no de configuración local, decidí cambiar a Groq como proveedor para la Fase 1. La sintaxis es OpenAI-compatible (más extendida en la industria) y los conceptos transfieren igual a otros proveedores.´

**Día 3 (23 de Septiembre de 2026):** primer ejercicio completado — clasificador de partidas contables. Script que recibe una cuenta del PGC (código y nombre) y devuelve un JSON estructurado con grupo, subgrupo, naturaleza y descripción. Implementado con structured output de Groq (`gpt-oss-120b`), modo `strict=True`, enums mediante `Literal` para grupo y naturaleza, `temperature=0` para extracción determinista y validación con Pydantic.

Problemas encontrados y resueltos:
- En el diccionario `response_format` escribí `type="json_schema"`, usando `=` (sintaxis de argumento) en lugar de `:` (clave de diccionario) → error de sintaxis.
- Tras corregirlo, dejé `type:` sin comillas: la clave pasaba a ser la función `type` de Python en vez del texto `"type"` → `TypeError: keys must be str... not type` al serializar a JSON. El traceback apuntaba dentro de las librerías, lejos del fallo real, que estaba en mi fichero. Lección: que un código compile no significa que esté bien.

Aprendizaje clave: `strict` garantiza la *forma* de la respuesta (JSON válido, valores dentro del enum), no su *acierto*. Probando 5 inputs, el modelo acertó la naturaleza en los 5 casos (tarea semántica) pero falló el grupo en 4 de 5 (tarea mecánica = primer dígito del código). Conclusión para la Fase 2: el grupo debe calcularse en código puro (`int(cuenta[0])`) y reservar el LLM para lo genuinamente ambiguo.


## Autor

Iker Moreno— [GitHub: IkerMo](https://github.com/IkerMo)