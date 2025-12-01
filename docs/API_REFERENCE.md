# ReportForge - API Reference

Complete API documentation for ReportForge modules and functions.

---

## Table of Contents
1. [template_manager](#templatemanager)
2. [main](#main-module)
3. [data_processing](#dataprocessing)
4. [ppt_generator](#pptgenerator)
5. [Data Structures](#data-structures)

---

## TemplateManager

**Module**: `template_manager.py`

**Purpose**: Manages report templates - creation, storage, loading, and validation.

### Class: TemplateManager

```python
class TemplateManager:
    """Manages report templates - creation, saving, loading, and validation"""
```

#### Constructor

```python
def __init__(self, templates_dir: str = "templates/configs") -> None
```

**Parameters**:
- `templates_dir` (str, optional): Directory to store template configuration files. Default: `"templates/configs"`

**Example**:
```python
manager = TemplateManager()
# Or with custom directory
manager = TemplateManager("custom/templates")
```

---

### Methods

#### create_template()

Create a new template configuration.

```python
def create_template(
    self,
    name: str,
    client: str,
    description: str = "",
    ppt_template_path: str = "",
) -> Dict[str, Any]
```

**Parameters**:
- `name` (str): Template name
- `client` (str): Client/brand name
- `description` (str, optional): Template description. Default: `""`
- `ppt_template_path` (str, optional): Path to PowerPoint template file. Default: `""`

**Returns**:
- `Dict[str, Any]`: Template configuration dictionary

**Example**:
```python
template = manager.create_template(
    name="Monthly Report",
    client="Acme Corp",
    description="Monthly sales and revenue report",
    ppt_template_path="templates/acme_template.pptx"
)
```

**Template Structure**:
```python
{
    "template_id": "abc123",
    "name": "Monthly Report",
    "client": "Acme Corp",
    "description": "Monthly sales and revenue report",
    "ppt_template_path": "templates/acme_template.pptx",
    "created_at": "2024-11-29T10:00:00",
    "updated_at": "2024-11-29T10:00:00",
    "version": "1.0",
    "data_mapping": {...},
    "slides": [],
    "processing_rules": {...},
    "formatting": {...}
}
```

---

#### save_template()

Save template to JSON file.

```python
def save_template(self, template: Dict[str, Any]) -> str
```

**Parameters**:
- `template` (Dict[str, Any]): Template configuration dictionary

**Returns**:
- `str`: Path to saved template file

**Example**:
```python
filepath = manager.save_template(template)
print(f"Template saved to: {filepath}")
# Output: Template saved to: templates/configs/abc123_Acme_Corp_Monthly_Report.json
```

**File Naming Convention**:
```
{template_id}_{client}_{name}.json
```

---

#### load_template()

Load template from file.

```python
def load_template(self, template_id_or_path: str) -> Optional[Dict[str, Any]]
```

**Parameters**:
- `template_id_or_path` (str): Template ID or full path to template file

**Returns**:
- `Optional[Dict[str, Any]]`: Template configuration dictionary or `None` if not found

**Example**:
```python
# Load by ID
template = manager.load_template("abc123")

# Load by full path
template = manager.load_template("templates/configs/abc123_Acme_Corp_Monthly_Report.json")

if template:
    print(f"Loaded template: {template['name']}")
else:
    print("Template not found")
```

---

#### list_templates()

List all available templates.

```python
def list_templates(self) -> List[Dict[str, Any]]
```

**Returns**:
- `List[Dict[str, Any]]`: List of template summary dictionaries

**Example**:
```python
templates = manager.list_templates()

for tmpl in templates:
    print(f"ID: {tmpl['template_id']}")
    print(f"Name: {tmpl['name']}")
    print(f"Client: {tmpl['client']}")
    print(f"Created: {tmpl['created_at']}")
    print(f"File: {tmpl['filepath']}")
    print("---")
```

**Template Summary Structure**:
```python
{
    "template_id": "abc123",
    "name": "Monthly Report",
    "client": "Acme Corp",
    "description": "Monthly sales report",
    "created_at": "2024-11-29T10:00:00",
    "filepath": "templates/configs/abc123_Acme_Corp_Monthly_Report.json"
}
```

---

#### delete_template()

Delete a template.

```python
def delete_template(self, template_id: str) -> bool
```

**Parameters**:
- `template_id` (str): Template ID to delete

**Returns**:
- `bool`: `True` if deleted successfully, `False` otherwise

**Example**:
```python
success = manager.delete_template("abc123")
if success:
    print("Template deleted")
else:
    print("Template not found")
```

---

#### validate_template()

Validate template configuration.

```python
def validate_template(self, template: Dict[str, Any]) -> tuple[bool, List[str]]
```

**Parameters**:
- `template` (Dict[str, Any]): Template dictionary to validate

**Returns**:
- `tuple[bool, List[str]]`: Tuple of (is_valid, list_of_errors)

**Example**:
```python
is_valid, errors = manager.validate_template(template)

if is_valid:
    print("Template is valid!")
else:
    print("Validation errors:")
    for error in errors:
        print(f"  - {error}")
```

**Validation Rules**:
- Required fields: `template_id`, `name`, `client`, `data_mapping`, `slides`
- `data_mapping` must specify `sheet_name`
- Must have at least one slide configuration

---

#### export_template()

Export template to a different location.

```python
def export_template(self, template_id: str, export_path: str) -> bool
```

**Parameters**:
- `template_id` (str): Template ID to export
- `export_path` (str): Destination file path

**Returns**:
- `bool`: `True` if exported successfully, `False` otherwise

**Example**:
```python
success = manager.export_template("abc123", "backup/template.json")
if success:
    print("Template exported")
```

---

#### import_template()

Import template from a file.

```python
def import_template(self, import_path: str) -> Optional[str]
```

**Parameters**:
- `import_path` (str): Path to template file to import

**Returns**:
- `Optional[str]`: Path to imported template file or `None` if failed

**Example**:
```python
filepath = manager.import_template("backup/template.json")
if filepath:
    print(f"Template imported to: {filepath}")
else:
    print("Import failed")
```

---

#### add_slide_config()

Add a slide configuration to template.

```python
def add_slide_config(
    self,
    template: Dict[str, Any],
    slide_index: int,
    slide_type: str,
    title: str = "",
    **kwargs
) -> Dict[str, Any]
```

**Parameters**:
- `template` (Dict[str, Any]): Template dictionary
- `slide_index` (int): Position of slide in presentation
- `slide_type` (str): Type of slide (`"table"`, `"chart"`, `"text"`, `"mixed"`)
- `title` (str, optional): Slide title. Default: `""`
- `**kwargs`: Additional slide configuration

**Returns**:
- `Dict[str, Any]`: Updated template dictionary

**Example**:
```python
template = manager.add_slide_config(
    template,
    slide_index=0,
    slide_type="table",
    title="Sales Summary",
    components=[]
)
```

---

#### add_table_component()

Add a table component to a slide.

```python
def add_table_component(
    self,
    slide_config: Dict[str, Any],
    columns: List[str],
    position: Dict[str, float],
    **kwargs
) -> Dict[str, Any]
```

**Parameters**:
- `slide_config` (Dict[str, Any]): Slide configuration dictionary
- `columns` (List[str]): List of column names to include
- `position` (Dict[str, float]): Position dict with `left`, `top`, `width`, `height` (in inches)
- `**kwargs`: Additional table configuration

**Kwargs Options**:
- `header_bold` (bool): Make header text bold. Default: `True`
- `header_font_size` (int): Header font size. Default: `12`
- `data_font_size` (int): Data font size. Default: `11`
- `alternating_rows` (bool): Use alternating row colors. Default: `True`

**Returns**:
- `Dict[str, Any]`: Updated slide configuration

**Example**:
```python
slide_config = {"slide_index": 0, "components": []}

manager.add_table_component(
    slide_config,
    columns=["company", "revenue", "growth"],
    position={"left": 0.5, "top": 1.5, "width": 9, "height": 5},
    header_bold=True,
    header_font_size=14,
    alternating_rows=True
)
```

---

#### add_chart_component()

Add a chart component to a slide.

```python
def add_chart_component(
    self,
    slide_config: Dict[str, Any],
    chart_type: str,
    data_columns: Dict[str, str],
    position: Dict[str, float],
    **kwargs
) -> Dict[str, Any]
```

**Parameters**:
- `slide_config` (Dict[str, Any]): Slide configuration dictionary
- `chart_type` (str): Type of chart (`"bar"`, `"line"`, `"pie"`, `"column"`)
- `data_columns` (Dict[str, str]): Dict mapping `x_axis` and `y_axis` to column names
- `position` (Dict[str, float]): Position dict
- `**kwargs`: Additional chart configuration

**Kwargs Options**:
- `title` (str): Chart title
- `legend` (bool): Show legend. Default: `True`
- `data_labels` (bool): Show data labels. Default: `False`
- `colors` (List[str]): List of color hex codes

**Returns**:
- `Dict[str, Any]`: Updated slide configuration

**Example**:
```python
manager.add_chart_component(
    slide_config,
    chart_type="bar",
    data_columns={"x_axis": "company", "y_axis": "revenue"},
    position={"left": 1, "top": 2, "width": 8, "height": 5},
    title="Revenue by Company",
    legend=True,
    colors=["#FF6B6B", "#4ECDC4", "#45B7D1"]
)
```

---

#### add_text_component()

Add a text component to a slide.

```python
def add_text_component(
    self,
    slide_config: Dict[str, Any],
    text_type: str,
    position: Dict[str, float],
    **kwargs
) -> Dict[str, Any]
```

**Parameters**:
- `slide_config` (Dict[str, Any]): Slide configuration dictionary
- `text_type` (str): Type of text (`"static"`, `"dynamic"`, `"ai_generated"`)
- `position` (Dict[str, float]): Position dict
- `**kwargs`: Additional text configuration

**Kwargs Options**:
- `content` (str): Static text content
- `data_source` (str): Data source for dynamic text
- `font_size` (int): Font size. Default: `14`
- `bold` (bool): Bold text. Default: `False`
- `color` (str): Text color. Default: `"black"`
- `alignment` (str): Text alignment (`"left"`, `"center"`, `"right"`). Default: `"left"`

**Returns**:
- `Dict[str, Any]`: Updated slide configuration

**Example**:
```python
manager.add_text_component(
    slide_config,
    text_type="static",
    position={"left": 1, "top": 0.5, "width": 8, "height": 1},
    content="Monthly Sales Report",
    font_size=24,
    bold=True,
    alignment="center"
)
```

---

## Main Module

**Module**: `main.py`

**Purpose**: Main report generation engine that orchestrates the report creation process.

### Functions

#### generate_report_from_template()

Generate a report using a template configuration.

```python
def generate_report_from_template(
    template_id_or_path: str,
    excel_path: str,
    output_path: str = None
) -> Optional[str]
```

**Parameters**:
- `template_id_or_path` (str): Template ID or path to template JSON file
- `excel_path` (str): Path to Excel data file
- `output_path` (str, optional): Optional output path for generated PPT. Default: `None` (auto-generated)

**Returns**:
- `Optional[str]`: Path to generated report or `None` if failed

**Example**:
```python
from main import generate_report_from_template

# Using template ID
report_path = generate_report_from_template(
    template_id_or_path="abc123",
    excel_path="data/november_2024.xlsx"
)

# Using template file path
report_path = generate_report_from_template(
    template_id_or_path="templates/configs/my_template.json",
    excel_path="data/november_2024.xlsx",
    output_path="output/custom_report.pptx"
)

if report_path:
    print(f"Report generated: {report_path}")
else:
    print("Generation failed")
```

**Process Flow**:
1. Load template configuration
2. Validate template
3. Load PowerPoint template
4. Load and process Excel data
5. Generate slides according to template
6. Add components (tables, charts)
7. Save presentation
8. Return output path

---

#### generate_report_direct()

Generate report directly without using a template configuration (legacy method).

```python
def generate_report_direct(
    excel_path: str,
    ppt_template_path: str,
    sheet_name: str,
    output_path: str
) -> Optional[str]
```

**Parameters**:
- `excel_path` (str): Path to Excel file
- `ppt_template_path` (str): Path to PowerPoint template
- `sheet_name` (str): Name of Excel sheet to process
- `output_path` (str): Output path for generated report

**Returns**:
- `Optional[str]`: Path to generated report or `None` if failed

**Example**:
```python
from main import generate_report_direct

report_path = generate_report_direct(
    excel_path="data/sales.xlsx",
    ppt_template_path="templates/template.pptx",
    sheet_name="Sheet1",
    output_path="output/report.pptx"
)
```

---

## DataProcessing

**Module**: `data_processing.py`

**Purpose**: Load and process Excel data with transformations and formatting.

### Functions

#### load_and_process_data()

Load and process Excel data.

```python
def load_and_process_data(
    file_path: str,
    sheet_name: str
) -> Optional[pd.DataFrame]
```

**Parameters**:
- `file_path` (str): Path to Excel file
- `sheet_name` (str): Name of sheet to read

**Returns**:
- `Optional[pd.DataFrame]`: Processed DataFrame or `None` if failed

**Example**:
```python
from data_processing import load_and_process_data

data = load_and_process_data(
    file_path="data/sales.xlsx",
    sheet_name="Sales"
)

if data is not None:
    print(data.head())
else:
    print("Failed to load data")
```

**Processing Steps**:
1. Load Excel file with pandas
2. Validate required columns exist
3. Normalize text data (strip, uppercase)
4. Group and aggregate data
5. Calculate derived columns
6. Sort data
7. Format numbers and currencies
8. Return processed DataFrame

**Current Implementation Note**:
- Currently hardcoded for specific Turkish media analysis columns
- Future versions will be configurable via template

---

## PPTGenerator

**Module**: `ppt_generator.py`

**Purpose**: Generate PowerPoint elements (tables, charts, text).

### Functions

#### create_table_slide()

Add a table to the slide with processed data.

```python
def create_table_slide(
    slide: Slide,
    data: pd.DataFrame
) -> None
```

**Parameters**:
- `slide` (Slide): PowerPoint slide object from python-pptx
- `data` (pd.DataFrame): Data to display in table

**Returns**:
- `None`

**Example**:
```python
from pptx import Presentation
from ppt_generator import create_table_slide
import pandas as pd

# Create presentation and slide
prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[5])

# Create data
data = pd.DataFrame({
    'Company': ['A', 'B', 'C'],
    'Revenue': [1000, 2000, 3000]
})

# Add table to slide
create_table_slide(slide, data)

# Save presentation
prs.save("output/report.pptx")
```

**Table Properties**:
- Position: 0.5 inches from left, 1.5 inches from top
- Size: 9 inches wide, 5 inches tall
- Header: Bold, 12pt font
- Data: 11pt font

**Future Functions** (Coming Soon):

#### create_chart_slide()
```python
def create_chart_slide(
    slide: Slide,
    data: pd.DataFrame,
    chart_type: str,
    config: Dict[str, Any]
) -> None
```

#### create_text_component()
```python
def create_text_component(
    slide: Slide,
    text: str,
    position: Dict[str, float],
    styling: Dict[str, Any]
) -> None
```

---

## Data Structures

### Template Configuration

Complete template configuration structure:

```python
{
    # Metadata
    "template_id": str,              # Unique identifier
    "name": str,                     # Template name
    "client": str,                   # Client/brand name
    "description": str,              # Description
    "version": str,                  # Version number (e.g., "1.0")
    "created_at": str,               # ISO-8601 datetime
    "updated_at": str,               # ISO-8601 datetime

    # PowerPoint template
    "ppt_template_path": str,        # Path to .pptx file

    # Data configuration
    "data_mapping": {
        "sheet_name": str,           # Excel sheet name
        "columns": {                 # Column mappings
            "Excel Column": "internal_name"
        },
        "filters": []                # Data filters (future)
    },

    # Slide configurations
    "slides": [
        {
            "slide_index": int,      # Slide position (0-based)
            "slide_type": str,       # "table", "chart", "text", "mixed"
            "title": str,            # Slide title
            "layout": str,           # Layout name (default: "default")
            "components": [          # List of components
                {
                    "type": str,     # "table", "chart", "text"
                    # Component-specific config
                }
            ]
        }
    ],

    # Processing rules
    "processing_rules": {
        "sort_by": str,              # Column to sort by
        "sort_order": str,           # "ascending" or "descending"
        "filters": [],               # Filter rules (future)
        "aggregations": []           # Aggregation rules (future)
    },

    # Formatting
    "formatting": {
        "number_format": {
            "decimal_places": int,   # Number of decimal places
            "use_thousands_separator": bool  # Use comma separator
        },
        "date_format": str,          # Python date format string
        "currency_symbol": str       # Currency symbol
    }
}
```

### Position Dictionary

Used for component positioning:

```python
{
    "left": float,    # Distance from left edge (inches)
    "top": float,     # Distance from top edge (inches)
    "width": float,   # Component width (inches)
    "height": float   # Component height (inches)
}
```

**Example**:
```python
position = {
    "left": 0.5,      # 0.5 inches from left
    "top": 1.5,       # 1.5 inches from top
    "width": 9.0,     # 9 inches wide
    "height": 5.0     # 5 inches tall
}
```

---

## Error Handling

All functions return `None` or `False` on failure and print error messages to console.

**Future Implementation** will use custom exceptions:

```python
class ReportForgeError(Exception):
    """Base exception"""

class TemplateError(ReportForgeError):
    """Template errors"""

class DataProcessingError(ReportForgeError):
    """Data processing errors"""

class GenerationError(ReportForgeError):
    """Report generation errors"""
```

---

## Examples

### Complete Workflow Example

```python
from template_manager import TemplateManager
from main import generate_report_from_template

# 1. Create template manager
manager = TemplateManager()

# 2. Create new template
template = manager.create_template(
    name="Sales Report",
    client="Acme Corp",
    description="Monthly sales analysis",
    ppt_template_path="templates/acme_template.pptx"
)

# 3. Configure data mapping
template["data_mapping"] = {
    "sheet_name": "Sales",
    "columns": {
        "Company Name": "company",
        "Revenue": "revenue",
        "Growth %": "growth"
    }
}

# 4. Add slide with table
slide_config = {
    "slide_index": 0,
    "slide_type": "table",
    "title": "Sales Summary",
    "components": []
}

manager.add_table_component(
    slide_config,
    columns=["company", "revenue", "growth"],
    position={"left": 0.5, "top": 1.5, "width": 9, "height": 5}
)

template["slides"].append(slide_config)

# 5. Save template
filepath = manager.save_template(template)
print(f"Template saved: {filepath}")

# 6. Generate report using template
report_path = generate_report_from_template(
    template_id_or_path=template["template_id"],
    excel_path="data/november_sales.xlsx",
    output_path="output/november_report.pptx"
)

print(f"Report generated: {report_path}")
```

---

This API reference covers the current stable functionality. For upcoming features, see the [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) roadmap.
