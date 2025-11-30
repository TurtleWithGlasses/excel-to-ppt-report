# ReportForge - User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Creating Templates](#creating-templates)
5. [Generating Reports](#generating-reports)
6. [Managing Templates](#managing-templates)
7. [Advanced Features](#advanced-features)
8. [Troubleshooting](#troubleshooting)
9. [FAQ](#faq)

---

## Introduction

### What is ReportForge?
ReportForge is an automated PowerPoint report generator that transforms Excel data into professional presentations. Instead of manually copying data and creating charts, you define a template once and generate unlimited reports from different data files.

### Who Should Use This Guide?
This guide is for end users who want to:
- Create custom report templates
- Generate reports from Excel data
- Manage multiple report templates
- Customize report layouts and styling

---

## Installation

### System Requirements
- **Operating System**: Windows 10+, macOS 10.14+, or Linux
- **Python**: Version 3.8 or higher
- **Disk Space**: 100 MB minimum
- **RAM**: 2 GB minimum (4 GB recommended)

### Installation Steps

#### Step 1: Install Python
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **Important**: Check "Add Python to PATH" during installation
4. Verify installation:
   ```bash
   python --version
   ```

#### Step 2: Download ReportForge
1. Download the project from GitHub or your source
2. Extract to a folder (e.g., `C:\ReportForge`)

#### Step 3: Install Dependencies
1. Open Command Prompt (Windows) or Terminal (macOS/Linux)
2. Navigate to the project folder:
   ```bash
   cd "C:\ReportForge\PPT Report Generator"
   ```
3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

#### Step 4: Verify Installation
Run the application:
```bash
python scripts/gui.py
```

If the GUI window opens, installation is successful!

---

## Quick Start

### Your First Report in 5 Minutes

#### Step 1: Launch the Application
```bash
cd "PPT Report Generator"
python scripts/gui.py
```

#### Step 2: Select Direct Mode
1. In the template dropdown, select **"[No Template - Direct Mode]"**
2. Select brand: **BSH** (or your brand)

#### Step 3: Upload Excel File
1. Click **"📁 Choose Excel File"**
2. Select your Excel file
3. Ensure the file has these columns:
   - Firma (Company)
   - Erişim (Reach)
   - StxCm
   - Reklam Eşdeğeri (Ad Value)
   - Editör (Sentiment)

#### Step 4: Generate Report
1. (Optional) Enter a report name
2. Click **"🚀 Generate Report"**
3. Wait a few seconds
4. Report saved to `output/` folder!

---

## Creating Templates

### Why Use Templates?

Templates allow you to:
- **Reuse**: Define structure once, use many times
- **Consistency**: Same format across all reports
- **Flexibility**: Different templates for different reports
- **Efficiency**: Generate reports in seconds

### Template Creation Methods

#### Method 1: Template Builder GUI (Recommended)

##### Step 1: Open Template Builder
1. Launch main application:
   ```bash
   python scripts/gui.py
   ```
2. Click **"➕ Create Template"**

##### Step 2: Fill Template Information
In the **"Template Info"** tab:
- **Template Name**: Enter descriptive name (e.g., "Monthly Sales Report")
- **Client/Brand**: Enter client name (e.g., "Acme Corp")
- **Description**: Describe the template purpose
- **PPT Template**: Click "Browse" and select your PowerPoint template file

##### Step 3: Configure Data Mapping
In the **"Data Mapping"** tab:

1. **Set Sheet Name**: Enter the Excel sheet name (e.g., "Sheet1", "Data")

2. **Add Column Mappings**:
   - Click **"Add Mapping"**
   - Enter Excel column name (e.g., "Revenue")
   - Enter internal name (e.g., "revenue")
   - Select data type (text, number, currency, etc.)
   - Repeat for all columns

Example mappings:
```
Excel Column       → Internal Name → Data Type
"Company Name"     → company       → text
"Revenue"          → revenue       → currency
"Growth %"         → growth        → percentage
"Date"             → report_date   → date
```

##### Step 4: Configure Slides
In the **"Slides"** tab:

1. **Add Slide**:
   - Click **"Add Slide"**
   - Enter slide title
   - Select slide type (table, chart, mixed)

2. **Add Components**:
   - Click **"Add Table"** to add a table component
   - Click **"Add Chart"** to add a chart (coming soon)
   - Click **"Add Text"** to add text box (coming soon)

3. **Repeat** for multiple slides

##### Step 5: Set Processing Rules
In the **"Processing Rules"** tab:

- **Sort By Column**: Enter column name to sort by
- **Sort Order**: Select "ascending" or "descending"
- **Decimal Places**: Set number of decimal places (0-4)
- **Thousands Separator**: Check to use commas (1,000)
- **Currency Symbol**: Enter your currency symbol (₺, $, €, etc.)

##### Step 6: Save Template
1. Click **"Save Template"**
2. Template saved to `templates/configs/` folder
3. Template is now available in the main application!

#### Method 2: Programmatic Creation (Advanced)

For developers or advanced users:

```python
from template_manager import TemplateManager

# Initialize manager
manager = TemplateManager()

# Create new template
template = manager.create_template(
    name="Monthly Sales Report",
    client="Acme Corp",
    description="Monthly sales analysis with charts",
    ppt_template_path="templates/acme_template.pptx"
)

# Configure data mapping
template["data_mapping"] = {
    "sheet_name": "Sales",
    "columns": {
        "Company Name": "company",
        "Revenue": "revenue",
        "Growth %": "growth"
    }
}

# Add a slide with table
slide1 = {
    "slide_index": 0,
    "slide_type": "table",
    "title": "Sales Summary",
    "components": []
}

# Add table component to slide
manager.add_table_component(
    slide1,
    columns=["company", "revenue", "growth"],
    position={"left": 0.5, "top": 1.5, "width": 9, "height": 5},
    header_bold=True,
    alternating_rows=True
)

template["slides"].append(slide1)

# Save template
filepath = manager.save_template(template)
print(f"Template saved: {filepath}")
```

---

## Generating Reports

### Using Templates to Generate Reports

#### Via GUI (Recommended)

##### Step 1: Select Template
1. Open main application
2. Click the template dropdown
3. Select your template from the list
4. Template info appears below the dropdown

##### Step 2: Upload Data
1. Click **"📁 Choose Excel File"**
2. Select your Excel file
3. Ensure the Excel file:
   - Has the correct sheet name (as defined in template)
   - Has the correct column names (as defined in template)
   - Contains data in the expected format

##### Step 3: Customize (Optional)
1. Enter custom report name in **"Report Name"** field
2. If empty, default name will be used

##### Step 4: Generate
1. Click **"🚀 Generate Report"**
2. Progress indicator appears
3. When complete, success message shows
4. Report saved to `output/` folder

##### Step 5: Save or Share
1. Click **"💾 Save Report As..."** to save to custom location
2. Share the report with your team!

#### Via Command Line (Advanced)

```bash
python scripts/main.py
```

Or use in your own scripts:

```python
from main import generate_report_from_template

# Generate report
report_path = generate_report_from_template(
    template_id_or_path="abc123",  # Template ID or full path
    excel_path="data/november_2024.xlsx",
    output_path="output/november_report.pptx"  # Optional
)

print(f"Report generated: {report_path}")
```

---

## Managing Templates

### Viewing Templates

#### In GUI
1. Open main application
2. Template dropdown shows all available templates
3. Template info appears when selected

#### Programmatically
```python
from template_manager import TemplateManager

manager = TemplateManager()
templates = manager.list_templates()

for template in templates:
    print(f"{template['name']} - {template['client']}")
    print(f"  Created: {template['created_at']}")
    print(f"  File: {template['filepath']}")
```

### Editing Templates

#### Edit via GUI
1. Open main application
2. Select template from dropdown
3. Click **"✏️ Edit Template"**
4. Template builder opens with template loaded
5. Make changes
6. Click **"Save Template"**

#### Edit JSON Directly (Advanced)
1. Navigate to `templates/configs/`
2. Open template JSON file in text editor
3. Make changes (be careful with syntax!)
4. Save file
5. Refresh template list in GUI

### Deleting Templates

#### Via GUI
1. Select template from dropdown
2. Click **"🗑️ Delete Template"**
3. Confirm deletion
4. Template removed from list

#### Via Code
```python
manager.delete_template("template_id")
```

### Import/Export Templates

#### Export Template
```python
manager.export_template("template_id", "backup/my_template.json")
```

#### Import Template
1. Via GUI: Click "Import Template" (if available)
2. Via code:
```python
manager.import_template("backup/my_template.json")
```

### Backing Up Templates

**Recommended Practice**:
1. Regularly backup `templates/configs/` folder
2. Use version control (Git) for templates
3. Export important templates to separate folder

---

## Advanced Features

### Data Processing Rules

#### Sorting Data
Configure in template:
```json
"processing_rules": {
  "sort_by": "revenue",
  "sort_order": "descending"
}
```

#### Filtering Data (Coming Soon)
```json
"processing_rules": {
  "filters": [
    {
      "column": "revenue",
      "operator": ">",
      "value": 10000
    }
  ]
}
```

#### Aggregations (Coming Soon)
```json
"processing_rules": {
  "aggregations": [
    {
      "type": "sum",
      "columns": ["revenue", "costs"],
      "group_by": "company"
    }
  ]
}
```

### Custom Formatting

#### Number Formatting
```json
"formatting": {
  "number_format": {
    "decimal_places": 2,
    "use_thousands_separator": true
  }
}
```

Result: `1000` → `1,000.00`

#### Currency Formatting
```json
"formatting": {
  "currency_symbol": "$"
}
```

#### Date Formatting
```json
"formatting": {
  "date_format": "%Y-%m-%d"
}
```

### Multiple Components per Slide (Coming Soon)

```json
"slides": [
  {
    "slide_index": 0,
    "components": [
      {
        "type": "table",
        "position": {"left": 0.5, "top": 1.5, "width": 5, "height": 4}
      },
      {
        "type": "chart",
        "position": {"left": 6, "top": 1.5, "width": 4, "height": 4}
      }
    ]
  }
]
```

---

## Troubleshooting

### Common Issues

#### Issue 1: "Template not loading"

**Symptoms**: Error message when selecting template

**Solutions**:
1. Check if template file exists in `templates/configs/`
2. Verify JSON syntax using online JSON validator
3. Check file permissions
4. Try refreshing template list (click ↻ Refresh button)

#### Issue 2: "Data not appearing in report"

**Symptoms**: Empty tables or missing data in generated report

**Solutions**:
1. Verify Excel sheet name matches template configuration
2. Check column names match exactly (case-sensitive)
3. Ensure Excel file has data in the specified sheet
4. Check for special characters or extra spaces in column names

#### Issue 3: "PowerPoint template not found"

**Symptoms**: Error about missing PPT template

**Solutions**:
1. Verify PowerPoint template path in template configuration
2. Use absolute path instead of relative path
3. Ensure PowerPoint file exists at specified location
4. Check file permissions

#### Issue 4: "Excel file error"

**Symptoms**: Error when loading Excel file

**Solutions**:
1. Ensure file is valid Excel format (.xlsx or .xls)
2. Check if file is open in Excel (close it)
3. Verify file is not corrupted
4. Try opening file in Excel to verify it works

#### Issue 5: "GUI freezes during generation"

**Symptoms**: Application becomes unresponsive

**Solutions**:
1. Wait - large files may take time
2. Check system resources (RAM, CPU)
3. Try with smaller Excel file
4. Restart application

### Error Messages

#### "Missing column in Excel data"
**Meaning**: Excel file doesn't have expected columns
**Fix**: Add missing columns or update template mapping

#### "Template validation failed"
**Meaning**: Template configuration is invalid
**Fix**: Check template JSON structure, ensure all required fields exist

#### "Failed to save presentation"
**Meaning**: Cannot save PowerPoint file
**Fix**: Check disk space, file permissions, close PowerPoint if open

---

## FAQ

### General Questions

**Q: Is ReportForge free?**
A: Yes, ReportForge is open source and free to use.

**Q: Do I need to know programming?**
A: No, the GUI allows you to create templates and generate reports without coding.

**Q: Can I use my own PowerPoint templates?**
A: Yes, you can use any PowerPoint file as a template.

**Q: How many templates can I create?**
A: Unlimited templates.

### Technical Questions

**Q: What Excel formats are supported?**
A: .xlsx (Excel 2007+) and .xls (Excel 97-2003)

**Q: What PowerPoint formats are supported?**
A: .pptx (PowerPoint 2007+)

**Q: Can I generate multiple reports at once?**
A: Batch generation is coming in a future update.

**Q: Does it work offline?**
A: Yes, ReportForge works completely offline.

### Template Questions

**Q: Can I share templates with my team?**
A: Yes, export templates and share the JSON files.

**Q: Can templates work with different Excel files?**
A: Yes, as long as Excel files have the same column structure.

**Q: Can I have different templates for different clients?**
A: Yes, create separate templates for each client.

**Q: Can I modify templates after creation?**
A: Yes, edit templates using the Template Builder.

### Data Questions

**Q: What happens if Excel has extra columns?**
A: Extra columns are ignored, only mapped columns are used.

**Q: Can I use formulas in Excel?**
A: Yes, ReportForge reads calculated values from Excel.

**Q: What if my data has missing values?**
A: Missing values appear as empty cells in the report.

**Q: Can I filter or transform data?**
A: Basic sorting is supported. Advanced processing coming soon.

---

## Next Steps

### For Beginners
1. Complete the Quick Start tutorial
2. Create your first template
3. Generate a few reports
4. Explore advanced features

### For Advanced Users
1. Learn programmatic template creation
2. Customize data processing
3. Create complex multi-slide templates
4. Integrate with your workflows

### Get Help
- Read [TEMPLATE_GUIDE.md](../TEMPLATE_GUIDE.md)
- Check [API_REFERENCE.md](API_REFERENCE.md)
- Review example templates in `templates/configs/`
- Open issues on GitHub

---

**Happy Report Building! 🚀**
