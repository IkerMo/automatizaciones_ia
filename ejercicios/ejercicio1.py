from groq import Groq
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal
import json
from dotenv import load_dotenv

load_dotenv()
client = Groq()

class ClasificacionCuentas(BaseModel):
    model_config = ConfigDict(extra="forbid")
    grupo: Literal[1,2,3,4,5,6,7,8,9]
    subgrupo: str = Field(description="string corto descriptor del subgrupo")
    naturaleza: Literal["Activo", "Pasivo", "Patrimonio", "Ingreso", "Gasto"]
    descripcion: str = Field(description="string de maximo 20 palabras")

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    temperature= 0,
    messages=[
        {
            "role" : "system",
            "content" : "Eres un experto en clasificar partidas de contabilidad. Quiero que clasifiques partidas contables en categorias estructuradas. Te pasare el numero y el nombre de la cuenta",
        },
        {"role": "user",
         "content" : "57000 - Caja, euros",
        },
    ],
    response_format={
        "type": "json_schema",
        "json_schema":{
            "name": "clasificador_partidas_contables",
            "strict": True,
            "schema": ClasificacionCuentas.model_json_schema()
        }
    }
)

clasificacion_cuentas = ClasificacionCuentas.model_validate(json.loads(response.choices[0].message.content))
print(json.dumps(clasificacion_cuentas.model_dump(), indent=2, ensure_ascii=False))