from flask import Flask, request, jsonify
from flask_cors import CORS
from decouple import config  # For handling environment variables securely
import os
from openai import OpenAI  # Use openai library for xAI API

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# CoST Jalisco context from your description
cost_description = """
La iniciativa de Transparencia en Infraestructura [Construction Sector Transparency Initiative] o "CoST" por sus siglas en inglés, es la encargada de promover la transparencia y la rendición de cuentas dentro de las diferentes etapas de los proyectos de infraestructura y obra pública. Actualmente, tiene presencia en 19 países distribuidos en cuatro continentes, donde trabaja directamente con el Gobierno, la sociedad civil y la industria del ramo de la construcción para promover la divulgación, validación e interpretación de datos de proyectos de infraestructura y obra pública.
"""

# Initialize OpenAI client for xAI API
XAI_API_KEY = config('XAI_API_KEY')  # Get API key from .env
client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",  # xAI API base URL (confirm with xAI documentation)
)

# Route for chatbot API using grok-2-latest
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    model = data.get('model', 'grok-2-latest')  # Default to grok-2-latest

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        # Create chat completion using grok-2-latest
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": f"You are Grok, the CoST Jalisco assistant, part of the global Construction Sector Transparency Initiative (CoST). Your purpose is to provide accurate and transparent information about infrastructure projects in Jalisco, including budgets, costs, status, type, and transparency efforts. {cost_description}"
                },
                {
                    "role": "user",
                    "content": user_message
                },
            ],
        )

        bot_response = completion.choices[0].message.content
        return jsonify({'response': bot_response})

    except Exception as e:
        # Fallback to rule-based responses if API fails
        fallback_response = get_fallback_response(user_message)
        return jsonify({'response': fallback_response})

# Fallback rule-based responses (simulating grok-2-latest behavior)
def get_fallback_response(user_message):
    user_message = user_message.lower()
    
    if 'proyectos' in user_message or 'proyectos de infraestructura' in user_message:
        return f'El dashboard muestra el estado de los proyectos de infraestructura en Jalisco, incluyendo presupuestos, costos, estado, tipo, y otros detalles. {cost_description}'
    elif 'cost' in user_message or 'cost jalisco' in user_message:
        return f'CoST (Construction Sector Transparency Initiative) trabaja en 19 países para promover transparencia y rendición de cuentas en proyectos de infraestructura. En Jalisco, mostramos datos validados de obras públicas en el dashboard. {cost_description}'
    elif 'presupuesto' in user_message or 'costos' in user_message:
        return 'El dashboard proporciona información detallada sobre los presupuestos y costos de los proyectos de infraestructura en Jalisco. Puedes filtrar por estado, tipo y otros criterios para obtener datos precisos.'
    elif 'estado' in user_message:
        return 'El dashboard muestra el estado actual de los proyectos de infraestructura (en progreso, completados, retrasados, etc.) en Jalisco. Usa los filtros para ver detalles específicos.'
    elif 'tipo' in user_message:
        return 'Los tipos de proyectos en el dashboard incluyen carreteras, edificios públicos, sistemas de agua, y más. Puedes explorar esta información filtrando por tipo en el dashboard.'
    elif 'transparencia' in user_message:
        return f'La transparencia es nuestro pilar fundamental. CoST Jalisco, como parte de la iniciativa global CoST, divulga, valida e interpreta datos de proyectos de obra pública para garantizar rendición de cuentas a la sociedad civil, gobierno e industria. {cost_description}'
    else:
        return 'Hola, soy el asistente de CoST Jalisco, parte de la iniciativa global CoST. Puedo ayudarte con información sobre los proyectos de infraestructura, presupuestos, costos, estado, tipo, y transparencia. ¿En qué puedo ayudarte?'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)