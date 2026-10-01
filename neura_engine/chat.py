import google.generativeai as genai
from neura_engine.config import GEMINI_API_KEY, MODEL_NAME

genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel(MODEL_NAME)

def ask_gemini(question):
    try:
        response = gemini_model.generate_content(question)
        return response.text if hasattr(response, "text") else "Sorry, I couldn't understand that."
    except Exception as e:
        print("Gemini error:", e)
        return "Neura is facing a connection issue with Gemini."