# 🌱 Carbon Receipt Scanner

Carbon Receipt Scanner is a web application that allows users to instantly calculate the estimated carbon footprint of their grocery purchases. By simply snapping a photo or uploading a receipt, the app utilizes multimodal AI to analyze the food items and provide a comprehensive environmental impact breakdown.

## Features

- **📷 Live Camera & Upload Integration**: Use your device's camera to snap receipts on the go, or upload existing images directly.
- **🧠 AI-Powered Analysis**: Powered by Google's Gemini Vision API to extract items and estimate their real-world carbon footprint.
- **📊 Impact Simulator**: Translates raw CO2 data into relatable metrics (miles driven, trees to plant) and simulates a carbon offset micro-transaction.
- **🏆 Gamification**: Grades your shopping trip from A to F based on the overall environmental impact.
- **📈 History Dashboard**: Tracks all previous scans using local storage, complete with inline previews and detailed breakdowns.

## Tech Stack

- **Frontend**: HTML5, CSS3, React (via CDN)
- **Backend**: Python, Flask
- **AI Integration**: Google Generative AI (Gemini Flash)

## Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ParjadM/Carbon-receipt-scanner.git
   cd Carbon-receipt-scanner
   ```

2. **Set up the virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install flask python-dotenv google-generativeai pillow
   ```

4. **Environment Variables**
   Create a `.env` file in the root directory and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

5. **Run the App**
   ```bash
   python app.py
   ```
   The application will be available at `http://localhost:5000`.

## How It Works
The backend uses a finely-tuned prompt passed to the Gemini Vision model to ignore non-food items, extract grocery products, and calculate the CO2 equivalent. The frontend handles the live video stream, responsive UI, and persistent history state.

## License
MIT

## Created by
1) Parjad Minooei
2) Aatman Shah
3) Akhil Sam
