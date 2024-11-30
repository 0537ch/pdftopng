from converter import FileConverter

def main():
    # Initialize the converter
    converter = FileConverter()

    # Example: Convert PDF to PNG
    try:
        # Place your PDF file in the input directory and update the path
        pdf_paths = converter.pdf_to_png("input/sample.pdf", "output_prefix")
        print(f"Generated PNG files: {pdf_paths}")
    except Exception as e:
        print(f"Error converting PDF to PNG: {e}")

    # Example: Convert PNG to PDF
    try:
        # Provide list of PNG files to convert
        png_files = ["input/image1.png", "input/image2.png"]
        pdf_path = converter.png_to_pdf(png_files, "combined_output.pdf")
        print(f"Generated PDF file: {pdf_path}")
    except Exception as e:
        print(f"Error converting PNG to PDF: {e}")

if __name__ == "__main__":
    main()
