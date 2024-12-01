from flask import Flask, request, send_file, jsonify
import os
from pathlib import Path
from converter import FileConverter
from werkzeug.utils import secure_filename
import traceback

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'input'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

converter = FileConverter()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'png'}

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    try:
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)

        if filename.lower().endswith('.pdf'):
            # Convert PDF to PNG
            try:
                output_files = converter.pdf_to_png(input_path, Path(filename).stem)
                if len(output_files) == 1:
                    return send_file(output_files[0])
                # For multiple pages, send the first one
                return send_file(output_files[0])
            except Exception as e:
                error_msg = f"PDF conversion error: {str(e)}\n{traceback.format_exc()}"
                print(error_msg)  # Print to console for debugging
                return jsonify({'error': error_msg}), 500
        else:
            # Convert PNG to PDF
            output_file = converter.png_to_pdf([input_path], f"{Path(filename).stem}.pdf")
            return send_file(output_file)

    except Exception as e:
        error_msg = f"General error: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)  # Print to console for debugging
        return jsonify({'error': error_msg}), 500

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=5001, debug=True)
