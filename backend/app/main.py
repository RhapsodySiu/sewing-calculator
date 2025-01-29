import os
from flask import Flask, send_file, request
from dotenv import load_dotenv
from .pdf import generate_pdf

load_dotenv(os.path.join(os.getcwd(), '../config/.env'))

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/pdf', methods=['POST'])
def test():
    data = request.json
    width = data.get('width')
    height = data.get('height')
    thickness = data.get('thickness')
    roundness = data.get('roundness')
    name = data.get('name')
    
    pdf_output = generate_pdf(name, width, height, thickness, roundness)
    return send_file(pdf_output, download_name="test.pdf", mimetype="application/pdf", as_attachment=True)

if __name__ == '__main__':
    api_host = os.getenv('API_HOST', '127.0.0.1')
    api_port = int(os.getenv('API_PORT', 5000))
    app.run(debug=True, host=api_host, port=api_port)
