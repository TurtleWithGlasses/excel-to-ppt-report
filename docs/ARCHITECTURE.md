# ReportForge - Architecture Documentation

## Overview

ReportForge follows a modular, layered architecture that separates concerns and enables extensibility. This document describes the technical architecture, design patterns, and implementation details.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface Layer                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Main GUI    │  │  Template    │  │   CLI        │      │
│  │  (gui.py)    │  │  Builder     │  │  Interface   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────┼────────────────────────────────┐
│                    Business Logic Layer                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Template    │  │  Report      │  │  Data        │      │
│  │  Manager     │  │  Generator   │  │  Processor   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────┼────────────────────────────────┐
│                     Data Access Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  File I/O    │  │  Excel       │  │  PowerPoint  │      │
│  │  Operations  │  │  Reader      │  │  Generator   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## Module Structure

### 1. User Interface Layer

#### gui.py - Main Application GUI
**Purpose**: Primary user interface for report generation

**Responsibilities**:
- Display template selection
- Handle file selection
- Trigger report generation
- Show generation progress
- Display results

**Key Components**:
```python
class PPTReportGeneratorApp:
    - __init__(root)              # Initialize GUI
    - create_template_selector()  # Template dropdown
    - create_file_selector()      # File picker
    - on_generate_report()        # Generate button handler
    - update_preview()            # Update preview pane
```

**Dependencies**:
- tkinter (GUI framework)
- template_manager (business logic)
- main (report generation)

#### template_builder_gui.py - Template Builder
**Purpose**: Visual interface for creating/editing templates

**Responsibilities**:
- Create new templates
- Edit existing templates
- Configure data mappings
- Design slide layouts
- Preview template JSON

**Key Components**:
```python
class TemplateBuilderGUI:
    - setup_ui()                  # Create UI layout
    - create_info_tab()           # Template info tab
    - create_mapping_tab()        # Data mapping tab
    - create_slides_tab()         # Slide configuration
    - create_rules_tab()          # Processing rules
    - save_template()             # Save to JSON
```

### 2. Business Logic Layer

#### template_manager.py - Template Operations
**Purpose**: CRUD operations for templates

**Responsibilities**:
- Create templates
- Load/save templates
- Validate templates
- Import/export templates
- List available templates

**Key Components**:
```python
class TemplateManager:
    - create_template()           # Create new template
    - load_template()             # Load from JSON
    - save_template()             # Save to JSON
    - validate_template()         # Validate structure
    - list_templates()            # Get all templates
    - delete_template()           # Remove template
    - import_template()           # Import from file
    - export_template()           # Export to file
```

**Data Structure**:
```python
template = {
    "template_id": str,
    "name": str,
    "client": str,
    "description": str,
    "ppt_template_path": str,
    "data_mapping": {...},
    "slides": [...],
    "processing_rules": {...},
    "formatting": {...}
}
```

#### main.py - Report Generation Engine
**Purpose**: Orchestrate report generation process

**Responsibilities**:
- Load templates
- Process Excel data
- Generate PowerPoint
- Handle errors
- Save output

**Key Functions**:
```python
def generate_report_from_template(
    template_id_or_path: str,
    excel_path: str,
    output_path: str = None
) -> str:
    """Generate report using template"""

def generate_report_direct(
    excel_path: str,
    ppt_template_path: str,
    sheet_name: str,
    output_path: str
) -> str:
    """Generate report without template (legacy)"""
```

**Workflow**:
```
1. Load template configuration
2. Load PowerPoint template
3. Load and process Excel data
4. Apply data transformations
5. Generate slides
6. Add components (tables, charts)
7. Save presentation
```

#### data_processing.py - Data Transformation
**Purpose**: Load and transform Excel data

**Responsibilities**:
- Load Excel files
- Validate data structure
- Transform data (sort, filter, aggregate)
- Format numbers, dates, currencies
- Handle missing values

**Key Functions**:
```python
def load_and_process_data(
    file_path: str,
    sheet_name: str
) -> pd.DataFrame:
    """Load and process Excel data"""
```

**Processing Pipeline**:
```
Excel File
    ↓
Load with pandas
    ↓
Validate columns
    ↓
Transform data (group, aggregate)
    ↓
Sort and filter
    ↓
Format values
    ↓
Return DataFrame
```

### 3. Data Access Layer

#### ppt_generator.py - PowerPoint Generation
**Purpose**: Create PowerPoint elements

**Responsibilities**:
- Create tables
- Generate charts (coming soon)
- Add text boxes (coming soon)
- Apply styling
- Position elements

**Key Functions**:
```python
def create_table_slide(
    slide: Slide,
    data: pd.DataFrame
) -> None:
    """Add table to slide"""
```

**Future Expansion**:
```python
def create_chart_slide(
    slide: Slide,
    data: pd.DataFrame,
    chart_type: str
) -> None:
    """Add chart to slide"""

def create_text_component(
    slide: Slide,
    text: str,
    position: dict
) -> None:
    """Add text box to slide"""
```

## Design Patterns

### 1. Template Method Pattern
**Used in**: Report generation

```python
def generate_report_from_template(...):
    # Algorithm skeleton
    template = load_template()        # Step 1
    data = load_data()                # Step 2
    presentation = load_ppt()         # Step 3
    process_slides(template, data)    # Step 4 (customizable)
    save_presentation()               # Step 5
```

### 2. Strategy Pattern
**Used in**: Data processing

```python
# Different strategies for different data types
class NumberFormatter:
    def format(self, value): pass

class CurrencyFormatter:
    def format(self, value): return f"${value:,.2f}"

class PercentageFormatter:
    def format(self, value): return f"{value:.1f}%"
```

### 3. Factory Pattern
**Planned for**: Component creation

```python
class ComponentFactory:
    def create_component(self, component_type, config):
        if component_type == "table":
            return TableComponent(config)
        elif component_type == "chart":
            return ChartComponent(config)
        elif component_type == "text":
            return TextComponent(config)
```

### 4. Builder Pattern
**Used in**: Template creation

```python
manager = TemplateManager()
template = (manager
    .create_template(name="Report", client="Client")
    .add_slide_config(...)
    .add_table_component(...)
    .add_chart_component(...))
```

## Data Flow

### Report Generation Flow

```
User Action (GUI)
    ↓
Select Template
    ↓
TemplateManager.load_template()
    ↓
Read JSON file
    ↓
Parse template configuration
    ↓
Select Excel File
    ↓
data_processing.load_and_process_data()
    ↓
pandas.read_excel()
    ↓
Validate columns
    ↓
Transform data
    ↓
Format values
    ↓
Click Generate
    ↓
main.generate_report_from_template()
    ↓
Load PowerPoint template
    ↓
For each slide in template:
    ↓
    For each component:
        ↓
        ppt_generator.create_table_slide()
        ↓
        Add data to slide
        ↓
        Apply styling
    ↓
Save presentation
    ↓
Display success message
```

### Template Creation Flow

```
User Action (Template Builder)
    ↓
Fill template info
    ↓
Add data mappings
    ↓
Configure slides
    ↓
Add components
    ↓
Set processing rules
    ↓
Click Save
    ↓
TemplateBuilderGUI.update_template_from_form()
    ↓
Collect form data
    ↓
Build template object
    ↓
TemplateManager.validate_template()
    ↓
Check required fields
    ↓
Validate structure
    ↓
TemplateManager.save_template()
    ↓
Generate filename
    ↓
Write JSON file
    ↓
Display success message
```

## Component Architecture

### Template Structure

```json
{
  "template_id": "unique-id",
  "metadata": {
    "name": "Template Name",
    "client": "Client Name",
    "description": "Description",
    "version": "1.0",
    "created_at": "ISO-8601 date",
    "updated_at": "ISO-8601 date"
  },
  "source": {
    "ppt_template_path": "path/to/template.pptx"
  },
  "data": {
    "mapping": {
      "sheet_name": "Sheet1",
      "columns": {
        "Excel Column": "internal_name"
      }
    },
    "processing": {
      "sort_by": "column_name",
      "sort_order": "asc|desc",
      "filters": [],
      "aggregations": []
    }
  },
  "slides": [
    {
      "slide_index": 0,
      "slide_type": "table|chart|mixed",
      "title": "Slide Title",
      "components": [
        {
          "type": "table|chart|text",
          "config": {...}
        }
      ]
    }
  ],
  "formatting": {
    "numbers": {...},
    "dates": {...},
    "currency": {...}
  }
}
```

### Component Types

#### Table Component
```json
{
  "type": "table",
  "columns": ["col1", "col2"],
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
```

#### Chart Component (Future)
```json
{
  "type": "chart",
  "chart_type": "bar|line|pie|column",
  "data_columns": {
    "x_axis": "column_name",
    "y_axis": "column_name"
  },
  "position": {...},
  "styling": {
    "title": "Chart Title",
    "legend": true,
    "colors": ["#FF0000", "#00FF00"]
  }
}
```

## Error Handling Strategy

### Current Implementation
```python
try:
    # Operation
except SpecificError as e:
    print(f"Error: {e}")
    return None
```

### Recommended Implementation
```python
# Custom exceptions
class TemplateError(Exception): pass
class DataProcessingError(Exception): pass
class GenerationError(Exception): pass

# Usage
try:
    template = load_template()
except TemplateError as e:
    logger.error(f"Template error: {e}")
    raise
```

## Configuration Management

### Current State
- Hardcoded values in code
- No centralized configuration

### Recommended Approach
```python
# config.py
class Config:
    TEMPLATES_DIR = "templates/configs"
    OUTPUT_DIR = "output"
    DATA_DIR = "data"

    # Data processing
    DEFAULT_DECIMAL_PLACES = 2
    DEFAULT_CURRENCY = "₺"

    # UI
    DEFAULT_WINDOW_SIZE = "900x700"

    # Logging
    LOG_LEVEL = "INFO"
    LOG_FILE = "reportforge.log"
```

## Performance Considerations

### Current Performance
- Synchronous operations
- No caching
- Full data reload each time

### Optimization Opportunities

#### 1. Asynchronous Operations
```python
import asyncio
import threading

def generate_report_async(template, data):
    thread = threading.Thread(
        target=generate_report_from_template,
        args=(template, data)
    )
    thread.start()
```

#### 2. Caching
```python
from functools import lru_cache

@lru_cache(maxsize=10)
def load_template(template_id):
    # Template loaded once, cached
    pass
```

#### 3. Lazy Loading
```python
# Load data only when needed
class LazyDataFrame:
    def __init__(self, file_path):
        self.file_path = file_path
        self._data = None

    @property
    def data(self):
        if self._data is None:
            self._data = pd.read_excel(self.file_path)
        return self._data
```

## Security Considerations

### Current Issues
- No path validation
- No input sanitization
- File operations without checks

### Security Improvements

#### 1. Path Validation
```python
import os
from pathlib import Path

def validate_path(path, base_dir):
    """Ensure path is within base directory"""
    abs_path = Path(path).resolve()
    abs_base = Path(base_dir).resolve()

    if not str(abs_path).startswith(str(abs_base)):
        raise SecurityError("Path outside allowed directory")

    return abs_path
```

#### 2. Input Sanitization
```python
import re

def sanitize_filename(filename):
    """Remove dangerous characters from filename"""
    # Remove path separators and special chars
    clean = re.sub(r'[^\w\s-]', '', filename)
    return clean.strip()
```

#### 3. File Size Limits
```python
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

def check_file_size(file_path):
    size = os.path.getsize(file_path)
    if size > MAX_FILE_SIZE:
        raise ValueError(f"File too large: {size} bytes")
```

## Testing Strategy

### Unit Tests
```python
# test_template_manager.py
import unittest

class TestTemplateManager(unittest.TestCase):
    def setUp(self):
        self.manager = TemplateManager()

    def test_create_template(self):
        template = self.manager.create_template(
            name="Test",
            client="Client"
        )
        self.assertIsNotNone(template)
        self.assertEqual(template['name'], "Test")
```

### Integration Tests
```python
# test_report_generation.py
def test_end_to_end_generation():
    # Create template
    # Load Excel file
    # Generate report
    # Verify output
    pass
```

## Future Architecture Enhancements

### 1. Plugin System
```python
class ComponentPlugin:
    def render(self, slide, data, config):
        raise NotImplementedError

# User can create custom plugins
class CustomChartPlugin(ComponentPlugin):
    def render(self, slide, data, config):
        # Custom rendering logic
        pass
```

### 2. Event System
```python
class EventBus:
    def emit(self, event, data):
        # Notify listeners
        pass

# Usage
event_bus.on('report_generated', send_email)
event_bus.on('template_saved', backup_template)
```

### 3. Microservices Architecture (Long-term)
```
┌────────────┐     ┌────────────┐     ┌────────────┐
│   Web UI   │────>│    API     │────>│  Template  │
│            │     │  Gateway   │     │  Service   │
└────────────┘     └────────────┘     └────────────┘
                          │
                          ├────────>┌────────────┐
                          │         │   Data     │
                          │         │  Service   │
                          │         └────────────┘
                          │
                          └────────>┌────────────┐
                                   │Generation  │
                                   │  Service   │
                                   └────────────┘
```

## Deployment Architecture

### Current: Desktop Application
```
User's Computer
    │
    ├── Python 3.8+
    ├── Dependencies (pandas, python-pptx, etc.)
    ├── Application Code
    └── Data Files (templates, excel, output)
```

### Future: Web Application
```
┌─────────────────┐
│   Web Browser   │
└────────┬────────┘
         │ HTTPS
┌────────┴────────┐
│  Web Server     │
│  (Flask/Django) │
└────────┬────────┘
         │
┌────────┴────────┐
│  Application    │
│  Server         │
└────────┬────────┘
         │
┌────────┴────────┐
│  Database       │
│  (PostgreSQL)   │
└─────────────────┘
```

## Conclusion

This architecture provides a solid foundation for ReportForge with clear separation of concerns, extensibility, and maintainability. Future enhancements should focus on:

1. Adding proper error handling and logging
2. Implementing async operations
3. Adding caching and optimization
4. Creating comprehensive test coverage
5. Building plugin system for extensibility

The modular design allows incremental improvements without major rewrites.
