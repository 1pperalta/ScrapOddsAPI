from dotenv import load_dotenv
import os
import google.generativeai as genai
from server_py.services.match_tools import get_last_results

# Cargar la API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Modelo de Gemini
model = genai.GenerativeModel("gemini-2.5-flash")

def analyze_team(team: str):
    """Consulta los últimos resultados del equipo y genera un análisis con Gemini."""
    results = get_last_results(team)
    if not results:
        return f"No hay datos disponibles para el equipo {team}."

    # Construir el contexto para Gemini
    context = "Últimos resultados recientes:\n"
    for r in results:
        context += f"{r[0]} | {r[1]} {r[3]}-{r[4]} {r[2]} | Resultado: {r[5]} | Diferencia: {r[6]}\n"

    prompt = (
        f"Con base en los siguientes resultados del equipo {team}, "
        f"describe brevemente su desempeño reciente en tono analítico:\n\n{context}"
    )

    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    print(analyze_team("Arsenal"))
