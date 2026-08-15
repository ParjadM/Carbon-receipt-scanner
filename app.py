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
    
    # Save image for history preview
    ext = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
    filename = f"receipt_{uuid.uuid4().hex}.{ext}"
    uploads_dir = os.path.join(app.root_path, 'static', 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    
    with open(os.path.join(uploads_dir, filename), 'wb') as f:
        f.write(image_bytes)
        
    image_url = f"/static/uploads/{filename}"
    
    # Calculate footprint (Directly using Multimodal Gemini)
    result = estimate_footprint(image_bytes, mime_type)
    
    if "error" in result:
        return jsonify(result), 400
        
    result["image_url"] = image_url
    return jsonify(result)

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True, port=5000)
