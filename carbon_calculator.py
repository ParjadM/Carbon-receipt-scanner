import os
import json
import google.generativeai as genai

def estimate_footprint(image_bytes, mime_type="image/jpeg"):
    if not image_bytes:
        return {"items": [], "total_g_co2": 0}
        
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("Missing GEMINI_API_KEY")
        return {"error": "Missing Gemini API Key"}
        
    genai.configure(api_key=api_key)
    
    prompt = """
    Analyze this grocery receipt image. Identify the food items and their quantities.
    Calculate the estimated carbon footprint for each item in grams of CO2 equivalent (g CO2e).
    Return the result in JSON format with two keys:
    1. 'items': a list of objects, each containing 'name' (string) and 'co2' (number in grams).
    2. 'total_g_co2': the sum of all item footprints (number).
    
    CRITICAL: If the image is blurry, illegible, or the text cannot be confidently read (which happens often with webcam captures), you MUST NOT guess or hallucinate items. Instead, return an empty array for 'items' and 0 for 'total_g_co2'.
    
    Return ONLY the raw JSON object, without any markdown formatting, backticks, or extra text.
    """
    
    image_part = {
        "mime_type": mime_type,
        "data": image_bytes
    }
    
    models_to_try = ['gemini-1.5-flash-latest', 'gemini-1.5-flash', 'gemini-1.5-pro-latest']
    last_error = None
    
    for model_name in models_to_try:
        try:
            print(f"Trying model: {model_name}...")
            model = genai.GenerativeModel(model_name)
            
            response = model.generate_content(
                [prompt, image_part],
                generation_config={"temperature": 0.0}
            )
            
            result_text = response.text.strip()
            print(f"--- DEBUG GEMINI RESPONSE ({model_name}) ---")
            print(result_text)
            print("---------------------------")
            
            # Remove markdown code blocks if the model accidentally includes them
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
                
            result_text = result_text.strip()
            
            data = json.loads(result_text)
            
            return data
            
        except Exception as e:
            print(f"Failed with {model_name}: {e}")
            last_error = e

    # If all API calls fail
    print("All models failed.")
    return {"error": f"Failed to analyze receipt. Last error: {str(last_error)}"}
