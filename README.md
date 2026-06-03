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

## Autor

Iker Moreno— [GitHub: IkerMo](https://github.com/IkerMo)