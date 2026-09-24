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
- Google AI Studio generaba claves con prefijo `AQ.` en lugar de `AIza`, incompatibles con el SDK oficial. Tras confirmar que era un problema conocido del lado de Google y no de configuración local, decidí cambiar a Groq como proveedor para la Fase 1. La sintaxis es OpenAI-compatible (más extendida en la industria) y los conceptos transfieren igual a otros proveedores.

**Día 3 (23 de Septiembre de 2026):** primer ejercicio completado — clasificador de partidas contables. Script que recibe una cuenta del PGC (código y nombre) y devuelve un JSON estructurado con grupo, subgrupo, naturaleza y descripción. Implementado con structured output de Groq (`gpt-oss-120b`), modo `strict=True`, enums mediante `Literal` para grupo y naturaleza, `temperature=0` para extracción determinista y validación con Pydantic.

Problemas encontrados y resueltos:
- En el diccionario `response_format` escribí `type="json_schema"`, usando `=` (sintaxis de argumento) en lugar de `:` (clave de diccionario) → error de sintaxis.
- Tras corregirlo, dejé `type:` sin comillas: la clave pasaba a ser la función `type` de Python en vez del texto `"type"` → `TypeError: keys must be str... not type` al serializar a JSON. El traceback apuntaba dentro de las librerías, lejos del fallo real, que estaba en mi fichero. Lección: que un código compile no significa que esté bien.

Aprendizaje clave: `strict` garantiza la *forma* de la respuesta (JSON válido, valores dentro del enum), no su *acierto*. Probando 5 inputs, el modelo acertó la naturaleza en los 5 casos (tarea semántica) pero falló el grupo en 4 de 5 (tarea mecánica = primer dígito del código). Conclusión para la Fase 2: el grupo debe calcularse en código puro (`int(cuenta[0])`) y reservar el LLM para lo genuinamente ambiguo.

**Día 4 (24 de Septiembre de 2026):** segundo ejercicio en curso — resumidor de noticias de empresas en concurso. Script que recibe el texto de una noticia y devuelve un JSON estructurado con empresa, sector, tipo de procedimiento, fecha del evento, deuda mencionada (EUR), principales acreedores y resumen de una línea. Implementado con structured output de Groq (`gpt-oss-120b`), modo `strict=True`, `Literal` para el tipo de procedimiento, `extra="forbid"`, `temperature=0` y validación con Pydantic. Probado por ahora con una sola noticia (Enerside); quedan dos por probar, entre ellas una con fecha completa y acreedores nombrados.

Problemas encontrados y resueltos (detectados al revisar el código antes de ejecutar):
- Escribí `NULL` en lugar de `None` → `NameError` al definir la clase.
- Puse el `| None` sobre `Field(...)` en vez de en la anotación de tipo → `TypeError`. La unión con `None` va en el tipo, a la izquierda del `=`; `Field(...)` es el valor, a la derecha.

Aprendizaje clave: en modo estricto todos los campos deben ser obligatorios, así que un dato que puede faltar se declara como `X | None` **sin** valor por defecto. Con `= None`, Pydantic lo saca de `required` y el esquema deja de cumplir lo que exige Groq (lo comprobé generando el esquema). Además, JSON no tiene tipo fecha: la fecha siempre viaja como texto y hay que decidir en qué capa se valida. Resultado con Enerside: fecha `null` (la noticia solo dice "este lunes"), deuda 40.000.000 y acreedores `[]` (no se nombra ninguno), que coincide con lo que había anotado esperar. Que el modelo prefiera `null` a inventar depende de las instrucciones del system prompt, no del esquema.

Limitaciones conocidas:
- `fecha_evento` es `str`: Pydantic no valida que sea una fecha real.
- "Más de 40 millones" se guarda como 40.000.000, sin distinguir que es un mínimo.
- Solo probado con una noticia, que no tiene fecha ni acreedores: falta un caso con datos completos para comprobar que el modelo no devuelve `null` por sistema.

## Autor

Iker Moreno — [GitHub: IkerMo](https://github.com/IkerMo)