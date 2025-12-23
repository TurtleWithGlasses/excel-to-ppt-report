# PDF Export Feature - User Guide

## Overview

The report generator now supports exporting reports in two formats:
- **PowerPoint (.pptx)** - Editable presentation format
- **PDF (.pdf)** - Non-editable, portable document format

## How to Use

### 1. Select Output Format

When generating a report, you'll see a **Format** dropdown next to the report name field:

```
Report name: [Report_20251223]    Format: [PowerPoint (.pptx) ▼]
```

Click the dropdown to choose between:
- **PowerPoint (.pptx)** - Default option
- **PDF (.pdf)** - For read-only distribution

### 2. Generate Report

1. Complete Steps 1 & 2 (Import Data and Select Template)
2. Choose your desired format from the dropdown
3. Click **Step 3: Prepare Report**
4. Wait for generation to complete

**What happens during PDF generation:**
- The system first creates a PowerPoint file (.pptx)
- If PDF is selected, it automatically converts the PPTX to PDF
- Both files are saved in the `output/` folder
- Progress bar shows: "Converting to PDF..." during conversion

### 3. Download Report

Click **Step 4: Download Report** to save the file to your desired location.

The file dialog will automatically:
- Show the correct file extension (.pptx or .pdf)
- Filter for the appropriate file type
- Suggest the correct filename

## System Requirements

### For PowerPoint Export
- No additional requirements
- Works on all platforms

### For PDF Export
- **Operating System:** Windows (required)
- **Software:** Microsoft PowerPoint installed
- **Python Package:** pywin32

### Installing Requirements

If PDF export is not available, you'll see an error message. To enable it:

```bash
pip install pywin32
```

After installation, ensure Microsoft PowerPoint is installed on your system.

## Technical Details

### How PDF Conversion Works

The PDF conversion uses Microsoft PowerPoint's COM automation:

1. Report is generated as PowerPoint (.pptx)
2. PowerPoint application is launched invisibly
3. PPTX file is opened
4. PowerPoint's native "Save as PDF" is used
5. PowerPoint is closed
6. Original PPTX is preserved (not deleted)

### File Locations

Generated files are saved in the `output/` folder:

```
output/
├── Report_20251223.pptx    # PowerPoint version (always created)
└── Report_20251223.pdf     # PDF version (if PDF format selected)
```

### Error Handling

If PDF conversion fails:
- You'll see a warning message
- The PowerPoint version (.pptx) will still be available
- Error details will be shown in the message

Common error reasons:
1. PowerPoint not installed
2. PowerPoint is already running and locked
3. Insufficient permissions
4. pywin32 not installed

## Advantages of Each Format

### PowerPoint (.pptx)
✅ **Advantages:**
- Editable - recipient can modify content
- Supports animations and transitions
- Smaller file size
- Can extract charts and images easily

❌ **Disadvantages:**
- Requires PowerPoint to view properly
- Layout may change on different systems
- Not ideal for final distribution

### PDF (.pdf)
✅ **Advantages:**
- Universal compatibility - opens anywhere
- Layout is preserved exactly
- Cannot be easily modified (security)
- Professional for final distribution
- Smaller file size after conversion

❌ **Disadvantages:**
- Not editable without special tools
- Loses PowerPoint features (animations)
- Requires conversion time (~5-10 seconds)
- Windows-only generation

## Use Cases

### When to Use PowerPoint
- Internal reports that may need editing
- Presentations that will be projected
- When recipients need to customize content
- Collaborative workflows

### When to Use PDF
- Final reports for clients
- Archival purposes
- Email distribution
- Public sharing
- When you want to prevent modifications

## Programmatic Usage

You can also use PDF conversion in your Python scripts:

```python
from utils.pdf_converter import convert_pptx_to_pdf, is_pdf_conversion_available

# Check if PDF conversion is available
if is_pdf_conversion_available():
    # Convert PPTX to PDF
    pdf_path = convert_pptx_to_pdf('report.pptx')
    print(f"PDF created: {pdf_path}")
else:
    print("PDF conversion not available on this system")
```

### Advanced Options

```python
# Specify custom PDF output path
convert_pptx_to_pdf('input.pptx', 'custom_output.pdf')

# Delete original PPTX after conversion
convert_pptx_to_pdf('input.pptx', delete_pptx=True)
```

### Command Line Usage

Convert PPTX to PDF from command line:

```bash
# Basic conversion
python -m utils.pdf_converter input.pptx

# Specify output path
python -m utils.pdf_converter input.pptx -o output.pdf

# Delete original PPTX after conversion
python -m utils.pdf_converter input.pptx -d
```

## Troubleshooting

### "PDF conversion not available" error

**Solution:** Install Microsoft PowerPoint and pywin32:
```bash
pip install pywin32
```

### "PowerPoint is already running" error

**Solution:**
1. Close all PowerPoint windows
2. Open Task Manager
3. End any `POWERPNT.EXE` processes
4. Try again

### Conversion is very slow

**Cause:** Normal for large presentations (many slides or complex charts)

**Expected time:**
- Small reports (5-10 slides): 5-10 seconds
- Medium reports (10-20 slides): 10-20 seconds
- Large reports (20+ slides): 20-30 seconds

### PDF looks different from PowerPoint

**Cause:** Font rendering differences

**Solution:**
- Ensure fonts used in template are standard (Arial, Calibri, etc.)
- Avoid custom fonts that may not render in PDF

## Future Enhancements

Planned improvements:
- [ ] Support for PDF conversion on macOS and Linux (using LibreOffice)
- [ ] Batch conversion of multiple reports
- [ ] PDF compression options
- [ ] Watermark support for PDFs
- [ ] Password protection for PDFs

## Support

If you encounter issues:
1. Check the console output for detailed error messages
2. Verify Microsoft PowerPoint is installed and working
3. Ensure pywin32 is installed: `pip show pywin32`
4. Try generating a simple report first to test

For bug reports, include:
- Error message from console
- Windows version
- PowerPoint version
- Report template being used
