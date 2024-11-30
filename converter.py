import os
from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image
import logging
import subprocess

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FileConverter:
    def __init__(self, input_dir="input", output_dir="output"):
        """Initialize the converter with input and output directories."""
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        
        # Create directories if they don't exist
        self.input_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
        # Set up poppler path
        self.poppler_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'poppler', 'poppler-23.08.0', 'Library', 'bin')
        logger.info(f"Using Poppler path: {self.poppler_path}")
        
        # Verify poppler installation
        self._verify_poppler()

    def _verify_poppler(self):
        """Verify poppler installation and print debug information."""
        logger.info("Verifying Poppler installation...")
        
        # Check if directory exists
        if not os.path.exists(self.poppler_path):
            logger.error(f"Poppler directory not found at: {self.poppler_path}")
            raise RuntimeError("Poppler directory not found")
        
        # List contents of poppler directory
        logger.info("Poppler directory contents:")
        for root, dirs, files in os.walk(self.poppler_path):
            for name in files:
                logger.info(os.path.join(root, name))

    def pdf_to_png(self, pdf_path: str, output_prefix: str = None) -> list:
        """
        Convert PDF to PNG images.
        
        Args:
            pdf_path (str): Path to the PDF file
            output_prefix (str, optional): Prefix for output PNG files
            
        Returns:
            list: List of paths to generated PNG files
        """
        try:
            pdf_path = Path(pdf_path)
            if not pdf_path.exists():
                raise FileNotFoundError(f"PDF file not found: {pdf_path}")

            if output_prefix is None:
                output_prefix = pdf_path.stem

            logger.info(f"Converting PDF to PNG: {pdf_path}")
            logger.info(f"Using Poppler path: {self.poppler_path}")
            
            # Check if the PDF file is readable
            try:
                with open(pdf_path, 'rb') as f:
                    f.read(1024)  # Try to read first 1KB
                logger.info("PDF file is readable")
            except Exception as e:
                logger.error(f"Error reading PDF file: {e}")
                raise

            # Use the local poppler path
            images = convert_from_path(
                str(pdf_path),
                poppler_path=self.poppler_path,
                dpi=200,  # Explicitly set DPI
                fmt='png'  # Explicitly set format
            )
            
            logger.info(f"Successfully converted PDF to {len(images)} images")
            output_paths = []

            for i, image in enumerate(images):
                output_path = self.output_dir / f"{output_prefix}_page_{i+1}.png"
                image.save(str(output_path), "PNG")
                output_paths.append(str(output_path))
                logger.info(f"Saved PNG: {output_path}")

            return output_paths

        except Exception as e:
            logger.error(f"Error converting PDF to PNG: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            raise

    def png_to_pdf(self, png_paths: list, output_filename: str) -> str:
        """
        Convert PNG images to PDF.
        
        Args:
            png_paths (list): List of paths to PNG files
            output_filename (str): Name of the output PDF file
            
        Returns:
            str: Path to the generated PDF file
        """
        try:
            if not png_paths:
                raise ValueError("No PNG files provided")

            output_path = self.output_dir / output_filename
            if not output_path.suffix:
                output_path = output_path.with_suffix('.pdf')

            # If single PNG, convert directly
            if len(png_paths) == 1:
                image = Image.open(png_paths[0])
                image.save(str(output_path), "PDF", resolution=100.0)
            else:
                # If multiple PNGs, convert and combine
                images = []
                first_image = Image.open(png_paths[0])
                png_images = [Image.open(png) for png in png_paths[1:]]
                first_image.save(
                    str(output_path), "PDF",
                    resolution=100.0,
                    save_all=True,
                    append_images=png_images
                )

            logger.info(f"Created PDF: {output_path}")
            return str(output_path)

        except Exception as e:
            logger.error(f"Error converting PNG to PDF: {str(e)}")
            raise
