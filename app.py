import os
import uuid
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from carbon_calculator import estimate_footprint

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/scan', methods=['POST'])
def scan_receipt():
    if 'receipt' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
        
    file = request.files['receipt']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    image_bytes = file.read()
    mime_type = file.mimetype
    
    # Do not save to disk (Vercel has a read-only filesystem and ephemeral instances)
    # Instead, return the image directly as a base64 data URI for the frontend preview
    import base64
    base64_encoded = base64.b64encode(image_bytes).decode('utf-8')
    image_url = f"data:{mime_type};base64,{base64_encoded}"
    
    # Calculate footprint (Directly using Multimodal Gemini)
    result = estimate_footprint(image_bytes, mime_type)
    
    if "error" in result:
        return jsonify(result), 400
        
    result["image_url"] = image_url
    return jsonify(result)

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True, port=5000)
