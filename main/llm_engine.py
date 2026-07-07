# llm_engine.py
import os
import json
from openai import OpenAI

# Initialize the AI client (Default to DeepSeek for low cost / high logic)
# Set your API key in Termux: export DEEPSEEK_API_KEY="your-key-here"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "your-fallback-key-if-testing")

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"  # Or "https://api.openai.com/v1" if using GPT-4
)

async def parse_architectural_prompt(prompt_text, fallback_domain, fallback_type):
    """
    Converts a user's natural language prompt into structured JSON configuration.
    """
    if not prompt_text or len(prompt_text.strip()) < 5:
        # Fallback to defaults if the user didn't type anything specific
        return {"domain": fallback_domain, "type": fallback_type}

    system_instruction = """
    You are an expert Architectural AI. 
    Parse the user's architectural description into a JSON structure.
    Use these exact keys: domain, type, plot_size, floors, bathrooms.
    
    Valid domains: "Residential", "Commercial", "Industrial".
    If not specified, infer from context (e.g., 'beach house' = Residential).
    If plot_size, floors, or bathrooms are not mentioned, use realistic defaults for the type.
    Return ONLY valid JSON. Do not include markdown formatting or extra text.
    
    Example input: "A 3-story modern glass office in Kampala"
    Example output: {"domain": "Commercial", "type": "Corporate Hub Block", "plot_size": 1200, "floors": 3, "bathrooms": 4}
    """

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",  # Or "gpt-4o" if you prefer OpenAI
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt_text}
            ],
            temperature=0.1, # Keep it strictly factual
            response_format={ "type": "json_object" }
        )
        
        # Parse the AI's JSON response
        parsed = json.loads(response.choices[0].message.content)
        
        # Ensure the response matches our schema
        return {
            "domain": parsed.get("domain", fallback_domain),
            "type": parsed.get("type", fallback_type),
            "plot_size": parsed.get("plot_size", 800),
            "floors": parsed.get("floors", 3),
            "bathrooms": parsed.get("bathrooms", 2)
        }
    except Exception as e:
        print(f"AI Parsing error: {e}. Falling back to sidebar config.")
        return {"domain": fallback_domain, "type": fallback_type}