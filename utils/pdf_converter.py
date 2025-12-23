"""
PDF Converter - Converts PowerPoint files to PDF using COM automation

This module provides functionality to convert PPTX files to PDF format
using Microsoft PowerPoint's COM interface (Windows only).
"""

import os
import sys
from pathlib import Path


def convert_pptx_to_pdf(pptx_path: str, pdf_path: str = None, delete_pptx: bool = False) -> str:
    """
    Convert PowerPoint file to PDF using COM automation.

    This function requires Microsoft PowerPoint to be installed on Windows.
    It automates PowerPoint to open the PPTX file and export it as PDF.

    Args:
        pptx_path: Path to the input PowerPoint file (.pptx)
        pdf_path: Path for the output PDF file. If None, uses same name with .pdf extension
        delete_pptx: If True, deletes the original PPTX file after conversion

    Returns:
        str: Path to the generated PDF file

    Raises:
        ImportError: If win32com is not installed
        FileNotFoundError: If the input PPTX file doesn't exist
        Exception: If PowerPoint automation fails

    Example:
        >>> pdf_path = convert_pptx_to_pdf('report.pptx')
        >>> print(f"PDF saved to: {pdf_path}")
    """
    # Validate input file
    pptx_path = os.path.abspath(pptx_path)
    if not os.path.exists(pptx_path):
        raise FileNotFoundError(f"PowerPoint file not found: {pptx_path}")

    # Determine output PDF path
    if pdf_path is None:
        pdf_path = os.path.splitext(pptx_path)[0] + '.pdf'
    else:
        pdf_path = os.path.abspath(pdf_path)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

    # Try to import win32com
    try:
        import win32com.client
    except ImportError:
        raise ImportError(
            "win32com is required for PDF conversion. "
            "Install it with: pip install pywin32"
        )

    # PowerPoint constants
    PP_SAVE_AS_PDF = 32  # PowerPoint constant for PDF export format
    PP_FIXED_FORMAT_TYPE_PDF = 2  # Alternative constant

    powerpoint = None
    presentation = None

    try:
        # Create PowerPoint application instance
        print(f"[PDF Converter] Opening PowerPoint...")
        powerpoint = win32com.client.Dispatch("PowerPoint.Application")
        powerpoint.Visible = 1  # Make visible for debugging (set to 0 for production)

        # Open presentation
        print(f"[PDF Converter] Loading PPTX: {pptx_path}")
        presentation = powerpoint.Presentations.Open(pptx_path, WithWindow=False)

        # Export as PDF
        print(f"[PDF Converter] Exporting to PDF: {pdf_path}")
        presentation.SaveAs(pdf_path, PP_SAVE_AS_PDF)

        print(f"[PDF Converter] ✓ PDF created successfully")

        # Close presentation
        presentation.Close()

        # Optionally delete the original PPTX
        if delete_pptx:
            print(f"[PDF Converter] Deleting original PPTX: {pptx_path}")
            os.remove(pptx_path)

        return pdf_path

    except Exception as e:
        error_msg = f"Failed to convert PPTX to PDF: {str(e)}"
        print(f"[PDF Converter] ERROR: {error_msg}")
        raise Exception(error_msg) from e

    finally:
        # Clean up COM objects
        if presentation:
            try:
                presentation.Close()
            except:
                pass

        if powerpoint:
            try:
                powerpoint.Quit()
            except:
                pass


def is_pdf_conversion_available() -> bool:
    """
    Check if PDF conversion is available on this system.

    Returns:
        bool: True if PowerPoint COM automation is available, False otherwise

    Example:
        >>> if is_pdf_conversion_available():
        ...     print("PDF export is available")
        ... else:
        ...     print("PDF export requires Windows and Microsoft PowerPoint")
    """
    # Check if on Windows
    if sys.platform != 'win32':
        return False

    # Check if win32com is installed
    try:
        import win32com.client
    except ImportError:
        return False

    # Try to access PowerPoint
    try:
        powerpoint = win32com.client.Dispatch("PowerPoint.Application")
        powerpoint.Quit()
        return True
    except:
        return False


# Example usage
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Convert PowerPoint to PDF')
    parser.add_argument('input', help='Input PowerPoint file (.pptx)')
    parser.add_argument('-o', '--output', help='Output PDF file path')
    parser.add_argument('-d', '--delete', action='store_true',
                        help='Delete original PPTX after conversion')

    args = parser.parse_args()

    try:
        if not is_pdf_conversion_available():
            print("ERROR: PDF conversion is not available on this system")
            print("Requirements:")
            print("  - Windows operating system")
            print("  - Microsoft PowerPoint installed")
            print("  - pywin32 package (pip install pywin32)")
            sys.exit(1)

        pdf_path = convert_pptx_to_pdf(
            args.input,
            args.output,
            delete_pptx=args.delete
        )
        print(f"\n✓ Success! PDF saved to: {pdf_path}")

    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        sys.exit(1)
