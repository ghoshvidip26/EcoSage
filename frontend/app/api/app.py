from langchain_ollama import ChatOllama
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.messages import HumanMessage, AIMessage
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

# Suppress TensorFlow logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

app = Flask(__name__)
# Configure CORS to allow all origins for development
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

model = ChatOllama(model="llama3:latest")
class EcoAdvice(BaseModel):
    N: str = Field(..., description="Nitrogen")
    P: str = Field(..., description="Phosphorus")
    K: str = Field(..., description="Potassium")
    temp: str = Field(..., description="Temperature")
    rainfall: str = Field(..., description="Rainfall")

def build_filter(query: str) -> Optional[Dict[str, Any]]:
    """Build a filter for the vector store based on the query"""
    if not isinstance(query, str):
        return None
        
    filters = {}
    
    # Look for N, P, K values
    for param in ['N', 'P', 'K']:
        if f"{param}=" in query:
            try:
                value = float(query.split(f"{param}=")[1].split()[0].rstrip(','))
                filters[param] = value
            except (ValueError, IndexError):
                continue
    
    # Look for temperature and rainfall
    if 'temperature=' in query:
        try:
            temp = float(query.split('temperature=')[1].split()[0].rstrip('°C').rstrip(','))
            filters['temperature'] = temp
        except (ValueError, IndexError):
            pass
            
    if 'rainfall=' in query:
        try:
            rainfall = float(query.split('rainfall=')[1].split()[0].rstrip('mm').rstrip(','))
            filters['rainfall'] = rainfall
        except (ValueError, IndexError):
            pass
    
    return filters if filters else None

@app.route('/recommend-crop', methods=['POST'])
def recommend_crop():
    try:
        data = request.get_json()
        if not data or 'user_input' not in data:
            return jsonify({"error": "Please provide 'user_input' in the request body"}), 400
            
        user_input = data['user_input']
        print("\n🤖 Processing your request...")
        print(f"User Input: {user_input}")
        
        # Create the prompt template
        system_prompt = """You are an agricultural expert AI assistant. Your goal is to help farmers with crop recommendations 
        based on soil conditions (N, P, K levels) and weather conditions (temperature, rainfall). Be concise and practical 
        in your recommendations."""
        
        # Create a simple prompt
        prompt = f"""{system_prompt}
        
        Based on the following conditions, provide a crop recommendation:
        {user_input}
        
        Please provide:
        1. Recommended crop(s)
        2. Brief explanation
        3. Any additional agricultural advice
        """
        
        # Get response from the model
        response = model.invoke(prompt)
        
        # Format the response
        result = {
            "recommendation": response.content,
            "input_parameters": user_input
        }
        
        print("\n" + "="*50)
        print("🌱 CROP RECOMMENDATION")
        print("="*50)
        print(response.content)
        print("="*50)
        
        return jsonify(result)
        
    except Exception as e:
        error_msg = f"Error processing request: {str(e)}"
        print(f"\n⚠️ {error_msg}")
        return jsonify({"error": error_msg}), 500

if __name__ == '__main__':
    # Run on port 5000 to avoid conflict with Next.js frontend
    app.run(debug=True, port=5000, host='0.0.0.0')