import os
import requests

def perform_ocr(image_bytes):
    api_key = os.getenv('OCR_API_KEY', 'helloworld')
    url = 'https://api.ocr.space/parse/image'
    
    payload = {
        'apikey': api_key,
        'language': 'eng',
        'isOverlayRequired': False,
        'detectOrientation': True,
        'scale': True,
        'OCREngine': 2
    }
    
    files = {
        'file': ('receipt.jpg', image_bytes, 'image/jpeg')
    }
    
    try:
        response = requests.post(url, files=files, data=payload)
        response.raise_for_status()
        data = response.json()
        
        if data.get('IsErroredOnProcessing'):
            print(f"OCR Error: {data.get('ErrorMessage')}")
            return None
            
        parsed_results = data.get('ParsedResults', [])
        if not parsed_results:
            return None
            
        return parsed_results[0].get('ParsedText', '')
    except Exception as e:
        print(f"Request Error: {e}")
        return None
