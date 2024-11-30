import argparse
import sys
from pathlib import Path
from converter import FileConverter

def main():
    parser = argparse.ArgumentParser(description='File Converter CLI - Convert between PDF and PNG formats')
    parser.add_argument('--mode', choices=['pdf2png', 'png2pdf'], required=True,
                      help='Conversion mode: pdf2png or png2pdf')
    parser.add_argument('--input', required=True, nargs='+',
                      help='Input file path(s). For png2pdf, you can specify multiple files')
    parser.add_argument('--output', required=True,
                      help='Output filename or prefix')
    
    args = parser.parse_args()
    converter = FileConverter()

    try:
        if args.mode == 'pdf2png':
            output_files = converter.pdf_to_png(args.input[0], args.output)
            print(f"Successfully converted PDF to PNG. Output files: {output_files}")
        
        else:  # png2pdf
            output_file = converter.png_to_pdf(args.input, args.output)
            print(f"Successfully converted PNG to PDF. Output file: {output_file}")

    except Exception as e:
        print(f"Error during conversion: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
