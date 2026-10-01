import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq()

SYSTEM_PROMPT = "Eres un tutor sobre el TRLC (Ley Concursal española post-2022). Respondes dudas conceptuales con ejemplos claros."

conversation_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

print("Tutor TRLC. Escribe 'salir' para terminar o 'historial' para ver la memoria.")

while True:
    pregunta = input("\nTú: ").strip()

    # Si el usuario pulsa Enter sin escribir nada, volvemos a preguntar
    if not pregunta:
        continue

    # Comando para salir del bucle
    if pregunta.lower() == "salir":
        print("Hasta luego.")
        break

    # Comando de depuración: enseña qué hay en la memoria
    if pregunta.lower() == "historial":
        for i, mensaje in enumerate(conversation_history):
            print(f"[{i}] {mensaje['role']}: {mensaje['content'][:80]}")
        continue

    conversation_history.append({"role": "user", "content": pregunta})

    try:
        respuesta = client.chat.completions.create(
            model="openai/gpt-oss-120b",           
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                }

            ],         
            temperature=0.3,        # TODO: piensa qué valor tiene sentido aquí
        )
    except Exception as e:
        print(f"\n[Error llamando a la API: {e}]")
        conversation_history.pop()   # quitamos la pregunta huérfana para no duplicarla
        continue


    texto = respuesta.choices[0].message.content
    print(f"\nTutor: {texto}")

    # TODO: el paso que casi todo el mundo olvida
    conversation_history.append({"role": "assistant", "content": texto})