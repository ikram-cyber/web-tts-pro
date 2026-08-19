from flask import Flask, request, send_file, render_template, jsonify
import subprocess
import sys
import os
import uuid

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_tts():
    data = request.json
    text = data.get('text', '').strip()
    voice = data.get('voice', 'id-ID-ArdiNeural')

    if not text:
        return jsonify({"error": "Teks kosong!"}), 400

    filename = f"suara_{uuid.uuid4().hex}.mp3"
    filepath = os.path.join('/tmp', filename) 

    try:
        # Panggil edge-tts melalui core system executable langsung
        command = [sys.executable, '-m', 'edge_tts', '--voice', voice, '--text', text, '--write-media', filepath]
        
        # Jalankan dan tangkap log jika gagal
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        
        return send_file(filepath, as_attachment=True, download_name=f"voice-{voice}.mp3")
    except subprocess.CalledProcessError as e:
        # Ini akan melemparkan log asli dari mesin jika gagal
        return jsonify({"error": f"Sistem Error: {e.stderr}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
