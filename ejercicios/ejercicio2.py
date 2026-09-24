from groq import Groq
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal
import json
from dotenv import load_dotenv

load_dotenv()
client = Groq()

class ResumenNoticias(BaseModel):
    model_config = ConfigDict(extra="forbid")
    empresa: str
    sector: str
    tipo_procedimiento: Literal["concurso voluntario", "concurso necesario", "preconcurso", "plan de reestructuración", "otro"]
    fecha_evento: str | None = Field(description="Fecha con el formato YYYY-MM-DD o null si la noticia no da una fecha exacta") 
    deuda_mencionada_eur: float | None
    principales_acreedores: list[str]
    resumen_una_linea: str = Field(description= "descripcion de maximo 25 palabras")

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    temperature=0,
    messages=[
        {
            "role" : "system",
            "content" : "Eres un experto en resumir noticias de empresas en concurso. Quiero que resumas el fragmento de texto de la noticia que te voy a mandar ",
        },
        {"role": "user",
         "content" : "Tras meses de reestructuración y un expediente de regulación de empleo (ERE) para la totalidad de la plantilla en España, Enerside pide el concurso de acreedores. La energética catalana comunicó este lunes que se ha acogido al concurso voluntario acuciada por una deuda de más de 40 millones de euros que le vencen este mes de septiembre.",
        },
    ],
    response_format={
        "type": "json_schema",
        "json_schema":{
            "name": "Resumen_noticias_concurso",
            "strict": True,
            "schema": ResumenNoticias.model_json_schema()
        }
    }
)

resumen = ResumenNoticias.model_validate(json.loads(response.choices[0].message.content))
print(json.dumps(resumen.model_dump(), indent=2, ensure_ascii=False))


