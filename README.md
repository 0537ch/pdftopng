# PDF to PNG Converter

A Python-based service for converting between PDF and PNG file formats with both web interface and command-line support.

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## Features

- Convert PDF files to PNG images (supports multi-page PDFs)
- Convert PNG images to PDF (single or multiple images)
- Web interface with drag-and-drop support
- Command-line interface for batch processing
- Clean and modern UI using Tailwind CSS

## Prerequisites

- Python 3.7+
- Poppler (required for pdf2image)
  - Windows: Download from https://github.com/oschwartz10612/poppler-windows/releases/
  - Linux: `sudo apt-get install poppler-utils`

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/pdf-to-png.git
   cd pdf-to-png
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Poppler as mentioned in prerequisites

## Usage

### Web Interface

1. Start the web server:
   ```bash
   python app.py
   ```

2. Open your browser and go to `http://localhost:5000`
3. Drag and drop your files or use the file picker
4. Click "Convert" and your converted file will download automatically

### Command Line

Convert PDF to PNG:
```bash
python cli.py --mode pdf2png --input input/document.pdf --output converted
```

Convert PNG to PDF:
```bash
python cli.py --mode png2pdf --input input/image1.png input/image2.png --output combined.pdf
```

### Python API

```python
from converter import FileConverter

converter = FileConverter()

# PDF to PNG
png_files = converter.pdf_to_png("input/document.pdf", "output_prefix")

# PNG to PDF
pdf_file = converter.png_to_pdf(["input/image.png"], "output.pdf")
```

## Project Structure

```
pdf-to-png/
├── app.py           # Flask web application
├── cli.py           # Command-line interface
├── converter.py     # Main converter class
├── requirements.txt # Project dependencies
├── templates/       # HTML templates
│   └── index.html  # Web interface
├── input/          # Input files directory
└── output/         # Output files directory
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
