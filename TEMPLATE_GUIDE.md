# ReportForge - Template Management Guide

## Overview
ReportForge now supports **template-based report generation**, allowing you to create reusable report configurations that can be applied to different data sets.

## Features

### ✨ Key Capabilities
- **Create Custom Templates**: Define report structure once, reuse many times
- **Visual Template Builder**: User-friendly GUI for template creation
- **Data Mapping**: Map Excel columns to report components dynamically
- **Multi-Client Support**: Create separate templates for different clients/brands
- **Template Library**: Save, load, and manage multiple templates
- **Flexible Layouts**: Configure tables, charts, and text components

---

## Getting Started

### 1. Creating a Template

#### Method A: Using the Template Builder GUI

1. Launch the main application:
   ```bash
   python scripts/gui.py
   ```

2. Click **"➕ Create Template"** button

3. Fill in template information:
   - **Template Name**: e.g., "BSH Monthly Media Report"
   - **Client/Brand**: e.g., "BSH"
   - **Description**: Purpose of the template
   - **PPT Template**: Select your PowerPoint template file

4. Configure Data Mapping:
   - Set **Sheet Name** (which Excel sheet to read)
   - Add **Column Mappings** (Excel column → internal name)
   
5. Configure Slides:
   - Add slides
   - Set slide titles
   - Add components (tables, charts, text)

6. Set Processing Rules:
   - Sort order
   - Number formatting
   - Currency settings

7. Click **"Save Template"**

#### Method B: Programmatically

```python
from template_manager import TemplateManager

manager = TemplateManager()

# Create template
template = manager.create_template(
    name="Monthly Report",
    client="BSH",
    description="Monthly media analysis",
    ppt_template_path="templates/template.pptx"
)

# Configure data mapping
template["data_mapping"] = {
    "sheet_name": "BSH",
    "columns": {
        "Firma": "company",
        "Erişim": "reach",
        "Editör": "sentiment"
    }
}

# Add a slide with table
slide1 = {
    "slide_index": 0,
    "slide_type": "table",
    "title": "Summary",
    "components": []
}

manager.add_table_component(
    slide1,
    columns=["company", "reach", "sentiment"],
    position={"left": 0.5, "top": 1.5, "width": 9, "height": 5}
)

template["slides"].append(slide1)

# Save template
manager.save_template(template)
```

---

### 2. Using Templates to Generate Reports

#### Via GUI:

1. Launch the application:
   ```bash
   python scripts/gui.py
   ```

2. **Select Template** from dropdown
3. **Choose Excel File** with your data
4. (Optional) Enter report name
5. Click **"🚀 Generate Report"**
6. Report will be generated in `output/` directory

#### Via Code:

```python
from main import generate_report_from_template

# Generate report using template
generate_report_from_template(
    template_id_or_path="templates/configs/your_template.json",
    excel_path="data/your_data.xlsx",
    output_path="output/report.pptx"
)
```

---

## Template Structure

### Template JSON Format

```json
{
  "template_id": "abc123",
  "name": "BSH Monthly Report",
  "client": "BSH",
  "description": "Monthly media analysis report",
  "ppt_template_path": "templates/bsh_template.pptx",
  "created_at": "2024-11-29T10:00:00",
  "updated_at": "2024-11-29T10:00:00",
  "version": "1.0",
  
  "data_mapping": {
    "sheet_name": "BSH",
    "columns": {
      "Firma": "company",
      "Erişim": "reach",
      "StxCm": "stxcm",
      "Reklam Eşdeğeri": "ad_value",
      "Editör": "sentiment"
    },
    "filters": []
  },
  
  "slides": [
    {
      "slide_index": 0,
      "slide_type": "table",
      "title": "Monthly Summary",
      "components": [
        {
          "type": "table",
          "columns": ["company", "reach", "sentiment"],
          "position": {
            "left": 0.5,
            "top": 1.5,
            "width": 9,
            "height": 5
          },
          "styling": {
            "header_bold": true,
            "header_font_size": 12,
            "data_font_size": 11,
            "alternating_rows": true
          }
        }
      ]
    }
  ],
  
  "processing_rules": {
    "sort_by": "Toplam",
    "sort_order": "descending",
    "filters": [],
    "aggregations": [
      {
        "type": "sum",
        "columns": ["reach", "ad_value"],
        "group_by": "company"
      }
    ]
  },
  
  "formatting": {
    "number_format": {
      "decimal_places": 2,
      "use_thousands_separator": true
    },
    "date_format": "%Y-%m-%d",
    "currency_symbol": "₺"
  }
}
```

---

## Template Management

### List All Templates

```python
from template_manager import TemplateManager

manager = TemplateManager()
templates = manager.list_templates()

for tmpl in templates:
    print(f"{tmpl['name']} - {tmpl['client']}")
```

### Load a Template

```python
# By template ID
template = manager.load_template("abc123")

# By file path
template = manager.load_template("templates/configs/template.json")
```

### Delete a Template

```python
manager.delete_template("abc123")
```

### Export/Import Templates

```python
# Export
manager.export_template("abc123", "backup/template.json")

# Import
manager.import_template("backup/template.json")
```

### Validate Template

```python
is_valid, errors = manager.validate_template(template)

if is_valid:
    print("Template is valid!")
else:
    print("Errors:", errors)
```

---

## Component Types

### 1. Table Component

Displays data in tabular format.

```python
{
  "type": "table",
  "columns": ["col1", "col2", "col3"],
  "position": {
    "left": 0.5,    # inches from left
    "top": 1.5,     # inches from top
    "width": 9,     # width in inches
    "height": 5     # height in inches
  },
  "styling": {
    "header_bold": true,
    "header_font_size": 12,
    "data_font_size": 11,
    "alternating_rows": true
  }
}
```

### 2. Chart Component (Coming Soon)

Visualize data with charts.

```python
{
  "type": "chart",
  "chart_type": "bar",  # bar, line, pie, column
  "data_columns": {
    "x_axis": "company",
    "y_axis": "reach"
  },
  "position": {...},
  "styling": {
    "title": "Reach by Company",
    "legend": true,
    "data_labels": false,
    "colors": ["#FF6B6B", "#4ECDC4"]
  }
}
```

### 3. Text Component (Coming Soon)

Add static or dynamic text.

```python
{
  "type": "text",
  "text_type": "static",  # static, dynamic, ai_generated
  "content": "Monthly Summary",
  "position": {...},
  "styling": {
    "font_size": 14,
    "bold": true,
    "color": "black",
    "alignment": "left"
  }
}
```

---

## Best Practices

### 1. **Naming Conventions**
- Use descriptive template names
- Include client name and report type
- Example: "BSH_Monthly_Media_Analysis"

### 2. **Data Mapping**
- Map all columns you'll need in the report
- Use consistent internal names
- Document unusual mappings in description

### 3. **Template Organization**
- Keep templates in `templates/configs/`
- Create separate templates for each client
- Version your templates (update version field)

### 4. **Testing**
- Always test templates with sample data
- Validate templates before sharing
- Check formatting on different screen sizes

### 5. **Maintenance**
- Backup templates regularly
- Document template changes
- Update templates when Excel structure changes

---

## Troubleshooting

### Template Not Loading
- Check file path is correct
- Verify JSON is valid (use JSON validator)
- Check file permissions

### Data Not Appearing
- Verify sheet name matches Excel file
- Check column mappings are correct
- Ensure Excel file has data in specified columns

### Formatting Issues
- Check position values (must be positive)
- Verify font sizes are reasonable (8-24)
- Test with different PowerPoint templates

### Generation Errors
- Validate template first
- Check Excel file is not corrupted
- Ensure PowerPoint template exists

---

## Migration Guide

### From Direct Mode to Templates

If you have existing direct-mode code:

**Before:**
```python
generate_report_direct(
    excel_path="data.xlsx",
    ppt_template_path="template.pptx",
    sheet_name="Sheet1",
    output_path="output.pptx"
)
```

**After:**
1. Create a template configuration
2. Use template-based generation:

```python
generate_report_from_template(
    template_id_or_path="my_template.json",
    excel_path="data.xlsx",
    output_path="output.pptx"
)
```

---

## Future Enhancements

- [ ] Chart generation (bar, line, pie)
- [ ] AI-generated insights
- [ ] Conditional formatting
- [ ] Multi-sheet support
- [ ] Template marketplace
- [ ] Real-time preview
- [ ] Drag-and-drop template builder
- [ ] Template versioning UI
- [ ] Batch report generation

---

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review example templates in `templates/configs/`
3. See `scripts/template_manager.py` for API reference

---

## Example Templates

Example templates are automatically created when you run:

```bash
python scripts/template_manager.py
```

This creates:
- `BSH Monthly Media Report` template
- Configured for Turkish media analysis
- Ready to use with your data

---

**Happy Report Building! 🚀**






