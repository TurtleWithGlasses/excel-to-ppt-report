# ReportForge - Developer Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Development Setup](#development-setup)
3. [Project Structure](#project-structure)
4. [Core Concepts](#core-concepts)
5. [Adding Features](#adding-features)
6. [Testing](#testing)
7. [Code Style](#code-style)
8. [Contributing](#contributing)

---

## Getting Started

### Prerequisites
- **Python**: 3.8 or higher
- **Git**: For version control
- **IDE**: VS Code, PyCharm, or any Python IDE
- **Knowledge**: Python, pandas, basic PowerPoint concepts

### Quick Setup

```bash
# Clone repository
git clone <repository-url>
cd "PPT Report Generator"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (create dev-requirements.txt)
pip install pytest black flake8 mypy

# Run application
python scripts/gui.py
```

---

## Development Setup

### Recommended IDE Configuration

#### VS Code
Create `.vscode/settings.json`:
```json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length=100"],
  "editor.formatOnSave": true,
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests"]
}
```

#### PyCharm
- Enable Python integrated tools
- Set test runner to pytest
- Configure Black as external tool

### Environment Variables

Create `.env` file:
```bash
# Development settings
DEBUG=True
LOG_LEVEL=DEBUG

# Paths
TEMPLATES_DIR=templates/configs
OUTPUT_DIR=output
DATA_DIR=data

# Testing
TEST_MODE=True
```

---

## Project Structure

```
PPT Report Generator/
│
├── scripts/                    # Main application code
│   ├── __init__.py
│   ├── main.py                # Report generation engine
│   ├── gui.py                 # Main GUI application
│   ├── template_builder_gui.py # Template builder GUI
│   ├── template_manager.py    # Template CRUD operations
│   ├── data_processing.py     # Excel data processing
│   └── ppt_generator.py       # PowerPoint generation
│
├── templates/                  # PowerPoint templates
│   ├── configs/               # Template JSON files
│   └── *.pptx                 # PowerPoint template files
│
├── data/                       # Sample Excel files
│   └── example_data.xlsx
│
├── output/                     # Generated reports
│
├── tests/                      # Test files
│   ├── __init__.py
│   ├── test_template_manager.py
│   ├── test_data_processing.py
│   ├── test_ppt_generator.py
│   └── fixtures/              # Test data
│
├── docs/                       # Documentation
│   ├── PROJECT_OVERVIEW.md
│   ├── USER_GUIDE.md
│   ├── ARCHITECTURE.md
│   ├── DEVELOPER_GUIDE.md     # This file
│   └── API_REFERENCE.md
│
├── requirements.txt            # Production dependencies
├── dev-requirements.txt        # Development dependencies
├── README.md                   # Project README
├── TEMPLATE_GUIDE.md           # Template guide
└── .gitignore                  # Git ignore rules
```

---

## Core Concepts

### 1. Template System

Templates are JSON files that define report structure:

```python
{
  "template_id": "unique-id",
  "name": "Template Name",
  "data_mapping": {
    "sheet_name": "Sheet1",
    "columns": {"Excel Col": "internal_name"}
  },
  "slides": [
    {
      "slide_index": 0,
      "components": [...]
    }
  ]
}
```

**Key Points**:
- Templates are reusable configurations
- JSON format for easy editing
- Validation ensures structure correctness

### 2. Data Processing Pipeline

```
Excel File → Load → Validate → Transform → Format → Output
```

**Implementation**:
```python
def load_and_process_data(file_path, sheet_name):
    # 1. Load
    data = pd.read_excel(file_path, sheet_name=sheet_name)

    # 2. Validate
    validate_columns(data)

    # 3. Transform
    data = transform_data(data)

    # 4. Format
    data = format_numbers(data)

    return data
```

### 3. Component Architecture

Components are building blocks of slides:
- **Table Component**: Display data in tables
- **Chart Component**: Visualize data (future)
- **Text Component**: Add text boxes (future)

**Adding New Component**:
```python
class ChartComponent:
    def __init__(self, config):
        self.config = config

    def render(self, slide, data):
        # Rendering logic
        pass
```

---

## Adding Features

### Adding a New Chart Type

#### Step 1: Define Chart Configuration
```python
# In template_manager.py
def add_bar_chart_component(slide_config, x_axis, y_axis, position):
    chart_component = {
        "type": "chart",
        "chart_type": "bar",
        "data_columns": {
            "x_axis": x_axis,
            "y_axis": y_axis
        },
        "position": position
    }
    slide_config["components"].append(chart_component)
    return slide_config
```

#### Step 2: Implement Chart Generation
```python
# In ppt_generator.py
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE

def create_bar_chart(slide, data, config):
    """Create bar chart on slide"""
    # Extract configuration
    x_axis = config["data_columns"]["x_axis"]
    y_axis = config["data_columns"]["y_axis"]
    position = config["position"]

    # Prepare chart data
    chart_data = CategoryChartData()
    chart_data.categories = data[x_axis].tolist()
    chart_data.add_series('Values', data[y_axis].tolist())

    # Add chart to slide
    x, y = Inches(position["left"]), Inches(position["top"])
    cx, cy = Inches(position["width"]), Inches(position["height"])

    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.BAR_CLUSTERED,
        x, y, cx, cy,
        chart_data
    ).chart

    # Styling
    chart.has_legend = config.get("styling", {}).get("legend", True)

    return chart
```

#### Step 3: Integrate with Main Generation
```python
# In main.py
for component in slide_config.get('components', []):
    component_type = component.get('type')

    if component_type == 'table':
        create_table_slide(slide, data)
    elif component_type == 'chart':
        chart_type = component.get('chart_type')
        if chart_type == 'bar':
            create_bar_chart(slide, data, component)
        elif chart_type == 'line':
            create_line_chart(slide, data, component)
```

#### Step 4: Add GUI Support
```python
# In template_builder_gui.py
def add_chart_component(self):
    """Add chart component dialog"""
    dialog = tk.Toplevel(self.root)
    dialog.title("Add Chart Component")

    # Chart type selection
    ttk.Label(dialog, text="Chart Type:").grid(row=0, column=0)
    chart_type = ttk.Combobox(
        dialog,
        values=["bar", "line", "pie", "column"]
    )
    chart_type.grid(row=0, column=1)

    # X-axis column
    ttk.Label(dialog, text="X-Axis Column:").grid(row=1, column=0)
    x_axis = ttk.Entry(dialog)
    x_axis.grid(row=1, column=1)

    # Y-axis column
    ttk.Label(dialog, text="Y-Axis Column:").grid(row=2, column=0)
    y_axis = ttk.Entry(dialog)
    y_axis.grid(row=2, column=1)

    def on_add():
        # Create component configuration
        component = {
            "type": "chart",
            "chart_type": chart_type.get(),
            "data_columns": {
                "x_axis": x_axis.get(),
                "y_axis": y_axis.get()
            }
        }
        # Add to listbox
        self.components_listbox.insert(
            tk.END,
            f"Chart: {chart_type.get()} ({x_axis.get()} vs {y_axis.get()})"
        )
        dialog.destroy()

    ttk.Button(dialog, text="Add", command=on_add).grid(row=3, column=0, columnspan=2)
```

#### Step 5: Write Tests
```python
# In tests/test_ppt_generator.py
import unittest
import pandas as pd
from pptx import Presentation

class TestChartGeneration(unittest.TestCase):
    def setUp(self):
        self.presentation = Presentation()
        self.slide = self.presentation.slides.add_slide(
            self.presentation.slide_layouts[5]
        )
        self.data = pd.DataFrame({
            'Category': ['A', 'B', 'C'],
            'Values': [10, 20, 30]
        })

    def test_create_bar_chart(self):
        config = {
            "data_columns": {"x_axis": "Category", "y_axis": "Values"},
            "position": {"left": 1, "top": 1, "width": 8, "height": 5}
        }
        chart = create_bar_chart(self.slide, self.data, config)
        self.assertIsNotNone(chart)
        self.assertEqual(len(chart.series), 1)
```

---

## Testing

### Setting Up Tests

Create `tests/conftest.py`:
```python
import pytest
import pandas as pd
from pathlib import Path

@pytest.fixture
def sample_data():
    """Sample DataFrame for testing"""
    return pd.DataFrame({
        'Company': ['A', 'B', 'C'],
        'Revenue': [1000, 2000, 3000],
        'Growth': [10, 20, 30]
    })

@pytest.fixture
def sample_template():
    """Sample template configuration"""
    return {
        "template_id": "test-123",
        "name": "Test Template",
        "client": "Test Client",
        "data_mapping": {
            "sheet_name": "Sheet1",
            "columns": {
                "Company": "company",
                "Revenue": "revenue"
            }
        },
        "slides": []
    }

@pytest.fixture
def temp_dir(tmp_path):
    """Temporary directory for test files"""
    return tmp_path
```

### Writing Unit Tests

```python
# tests/test_template_manager.py
import unittest
from template_manager import TemplateManager

class TestTemplateManager(unittest.TestCase):
    def setUp(self):
        self.manager = TemplateManager()

    def test_create_template(self):
        """Test template creation"""
        template = self.manager.create_template(
            name="Test",
            client="Client",
            description="Test description"
        )

        self.assertIsNotNone(template)
        self.assertEqual(template['name'], "Test")
        self.assertEqual(template['client'], "Client")
        self.assertIn('template_id', template)

    def test_validate_template(self):
        """Test template validation"""
        template = self.manager.create_template("Test", "Client")
        is_valid, errors = self.manager.validate_template(template)

        # Empty template should have validation errors
        self.assertFalse(is_valid)
        self.assertIn("sheet_name", str(errors))
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_template_manager.py

# Run with coverage
pytest --cov=scripts --cov-report=html

# Run with verbose output
pytest -v
```

---

## Code Style

### Python Style Guide

Follow **PEP 8** with these specifics:
- Line length: 100 characters
- Use 4 spaces for indentation
- Use type hints where appropriate

### Formatting with Black

```bash
# Format all files
black scripts/

# Check without formatting
black --check scripts/

# Format specific file
black scripts/template_manager.py
```

### Linting with Flake8

```bash
# Lint all files
flake8 scripts/

# Ignore specific warnings
flake8 --ignore=E501,W503 scripts/
```

### Type Checking with MyPy

```bash
# Type check
mypy scripts/
```

### Example Code Style

```python
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class TemplateManager:
    """
    Manages report templates.

    This class handles CRUD operations for templates including
    creation, loading, saving, and validation.

    Attributes:
        templates_dir (str): Directory where templates are stored
    """

    def __init__(self, templates_dir: str = "templates/configs") -> None:
        """
        Initialize template manager.

        Args:
            templates_dir: Directory for template storage
        """
        self.templates_dir = templates_dir
        self._ensure_directory()

    def create_template(
        self,
        name: str,
        client: str,
        description: str = "",
    ) -> Dict[str, Any]:
        """
        Create a new template configuration.

        Args:
            name: Template name
            client: Client or brand name
            description: Optional description

        Returns:
            Template configuration dictionary

        Raises:
            ValueError: If name or client is empty
        """
        if not name or not client:
            raise ValueError("Name and client are required")

        template = {
            "template_id": self._generate_id(),
            "name": name,
            "client": client,
            "description": description,
        }

        logger.info(f"Created template: {name} for {client}")
        return template
```

---

## Common Development Tasks

### Adding Logging

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('reportforge.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Usage
logger.info("Template loaded successfully")
logger.warning("Column not found, using default")
logger.error("Failed to generate report", exc_info=True)
```

### Adding Configuration

```python
# config.py
import os
from pathlib import Path

class Config:
    """Application configuration"""
    BASE_DIR = Path(__file__).parent
    TEMPLATES_DIR = BASE_DIR / "templates" / "configs"
    OUTPUT_DIR = BASE_DIR / "output"
    DATA_DIR = BASE_DIR / "data"

    # Data processing
    DEFAULT_DECIMAL_PLACES = 2
    DEFAULT_CURRENCY = "₺"
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

    # UI
    WINDOW_SIZE = "900x700"
    THEME = "clam"

    @classmethod
    def ensure_directories(cls):
        """Create required directories"""
        cls.TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Usage
from config import Config

Config.ensure_directories()
manager = TemplateManager(str(Config.TEMPLATES_DIR))
```

### Adding Custom Exceptions

```python
# exceptions.py
class ReportForgeError(Exception):
    """Base exception for ReportForge"""
    pass

class TemplateError(ReportForgeError):
    """Template-related errors"""
    pass

class DataProcessingError(ReportForgeError):
    """Data processing errors"""
    pass

class GenerationError(ReportForgeError):
    """Report generation errors"""
    pass

# Usage
from exceptions import TemplateError

def load_template(template_id):
    if not template_exists(template_id):
        raise TemplateError(f"Template not found: {template_id}")
```

---

## Debugging Tips

### Debug Mode

```python
# Enable debug mode
DEBUG = True

if DEBUG:
    print(f"Template: {template}")
    print(f"Data shape: {data.shape}")
```

### Using Python Debugger

```python
# Insert breakpoint
import pdb; pdb.set_trace()

# Or use built-in breakpoint() (Python 3.7+)
breakpoint()
```

### Logging for Debugging

```python
logger.debug(f"Processing {len(data)} rows")
logger.debug(f"Template config: {template}")
```

---

## Performance Optimization

### Profiling Code

```python
import cProfile
import pstats

# Profile function
profiler = cProfile.Profile()
profiler.enable()

generate_report_from_template(...)

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)
```

### Optimization Tips

1. **Use vectorized operations** instead of loops
2. **Cache expensive operations**
3. **Use generators** for large datasets
4. **Profile before optimizing**

---

## Contributing Workflow

### 1. Create Feature Branch
```bash
git checkout -b feature/chart-generation
```

### 2. Make Changes
- Write code
- Add tests
- Update documentation

### 3. Run Tests
```bash
pytest
black scripts/
flake8 scripts/
```

### 4. Commit Changes
```bash
git add .
git commit -m "Add bar chart generation feature"
```

### 5. Push and Create PR
```bash
git push origin feature/chart-generation
```

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines.

---

## Resources

### Python Libraries Documentation
- [pandas](https://pandas.pydata.org/docs/)
- [python-pptx](https://python-pptx.readthedocs.io/)
- [openpyxl](https://openpyxl.readthedocs.io/)
- [tkinter](https://docs.python.org/3/library/tkinter.html)

### Learning Resources
- [PEP 8 Style Guide](https://pep8.org/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [pytest Documentation](https://docs.pytest.org/)

---

## Getting Help

- Check existing documentation in `/docs`
- Review code comments
- Ask in GitHub Discussions
- Open an issue for bugs

Happy coding! 🚀
