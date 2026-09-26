from groq import Groq
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal
from pathlib import Path
import json
from dotenv import load_dotenv

load_dotenv()
client = Groq()

class AccionesPendientes(BaseModel):
    model_config = ConfigDict(extra="forbid")
    accion: str
    responsable: str | None = Field(description="Persona o equipo que se compromete explícitamente. null si no está claro.")
    fecha: str | None = Field(description="Plazo tal como se menciona en la transcripción (p. ej. 'hoy', 'la semana que viene'). null si no se menciona. No conviertas a fecha")

class ResumenTranscripcion(BaseModel):
    model_config = ConfigDict(extra="forbid")
    resumen_una_linea: str = Field(description= "Resumen de la reunion en una linea aproximadamente")
    temas_tratados: list[str]
    decisiones_tomadas: list[str]
    acciones_pendientes: list[AccionesPendientes]
    siguiente_reunion: str | None = Field(description="Fecha en la que se va a celebrar la proxima reunion o null si no se menciona")

reglas = Path("inputs/reglas.txt").read_text(encoding="utf-8")


transcripcion = """Contexto: Primera revisión detallada del flujo de caja proyectado a 13 semanas tras detectarse una desviación negativa en el fondo de maniobra.

                        Transcripción:

                        Consultor: Gracias por el tiempo, Carlos. Vamos directo al grano. Hemos analizado el borrador de la plantilla de 13-Week Cash Flow que nos envió tu equipo el martes. La viabilidad del negocio a medio plazo sigue ahí, pero la tensión de liquidez entre la semana 4 y la semana 7 es severa. En la semana 6 tenemos un pico de salidas que deja la caja en número rojo por casi 420.000 euros si no intervenimos ya.

                        CFO: Lo sé, Javier. El problema principal es que dos de nuestros clientes clave en la división industrial han aplazado sus pagos de 60 a 90 días unilateralmente. Al mismo tiempo, los proveedores de materia prima nos están exigiendo pagos a 30 días o contra entrega porque vieron el informe trimestral y están nerviosos. Estamos atrapados en el medio.

                        Consultor: Entiendo la presión, pero la prioridad absoluta hoy es tapar esa brecha de la semana 6. No podemos contar con líneas de crédito adicionales de los bancos en este momento; el pool bancario ya nos dejó claro la semana pasada que no incrementará el drawdown hasta que presentemos un plan de viabilidad formal. ¿Qué margen tenemos para negociar un standstill temporal o refinanciar el pago de la maquinaria que vence la próxima semana?

                        CFO: Hablé ayer con la entidad financiera del leasing. Podríamos solicitar un aplazamiento del principal de las cuotas de los próximos tres meses, pagando solo intereses. Eso nos liberaría unos 80.000 euros al mes. Respecto a la plantilla y salarios, la nómina de fin de mes está garantizada, pero la paga extraordinaria de dentro de dos meses va a ser un problema grave si no cobramos la factura de Construcciones Martínez.

                        Consultor: De acuerdo. Vamos a estructurar tres acciones inmediatas para esta semana. Primero, clasificaremos a los proveedores en tres categorías: críticos para la operación, diferibles y negociables. A los críticos les mantendremos el flujo con compromisos de pago semanales pequeños pero constantes. Segundo, hablo esta misma tarde con el socio de reestructuración para redactar la carta de aplazamiento para el leasing. Y tercero, necesito que tu equipo comercial aplique un descuento por pronto pago del 3% a Martínez para adelantar el cobro de esos 300.000 euros. Es preferible perder un margen marginal que romper la caja en la semana 6.

                        CFO: Me parece razonable. Hablaré con el director comercial hoy para el descuento de Martínez. Mi principal inquietud es cómo presentar esto al Consejo la semana que viene sin generar pánico.

                        Consultor: Presentaremos un discurso transparente pero bajo control: la compañía es operativa y técnicamente solvente, pero atraviesa un descalce temporal de capital de trabajo. Con el plan de choque de caja que acordemos hoy, demostraremos que la brecha se cubre sin necesidad de medidas concursales ni quitas agresivas."""

    

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    temperature=0,

    messages=[
        {
            "role" : "system",
            "content" : reglas,
        },
        {"role": "user",
         "content" : transcripcion,
        },
    ],
    response_format={
        "type": "json_schema",
        "json_schema":{
            "name": "Resumen_reunion",
            "strict": True,
            "schema": ResumenTranscripcion.model_json_schema()
        }
    }
)

resumen = ResumenTranscripcion.model_validate(json.loads(response.choices[0].message.content))
print(json.dumps(resumen.model_dump(), indent=2, ensure_ascii=False))


