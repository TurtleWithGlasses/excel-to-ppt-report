# Component-Based Architecture

## Overview

ReportForge uses a **modular, component-based architecture** where each part of a report (table, chart, text box, image) is a separate class that can be independently created, edited, and reused across templates.

This design is inspired by modern web frameworks (React, Vue) and modern design tools (Figma, Canva) where UI elements are composable components.

## Design Philosophy

### Core Principles

1. **Modularity**: Each report element is a self-contained component
2. **Reusability**: Components can be used across multiple templates
3. **Customizability**: Every aspect of a component can be modified
4. **Composability**: Components can be combined to create complex layouts
5. **User-Friendly**: Non-technical users can create/edit components via GUI

### Why Component-Based?

**Problem with Traditional Approach:**
```python
# Old way - hardcoded, inflexible
def create_report(data):
    slide1 = add_table(data, columns=[...])
    slide2 = add_chart(data, type="bar")
    # Locked into specific structure
```

**Component-Based Solution:**
```python
# New way - modular, flexible
template = Template()
template.add_component(slide=1, component=TableComponent(...))
template.add_component(slide=2, component=ChartComponent(...))
# Users can add/remove/modify any component
```

## Component Class Hierarchy

```
BaseComponent (Abstract)
    │
    ├── TableComponent
    │   ├── SimpleTableComponent
    │   ├── StyledTableComponent
    │   └── PivotTableComponent
    │
    ├── ChartComponent
    │   ├── BarChartComponent
    │   ├── LineChartComponent
    │   ├── PieChartComponent
    │   └── ColumnChartComponent
    │
    ├── TextComponent
    │   ├── TitleComponent
    │   ├── HeadingComponent
    │   └── ParagraphComponent
    │
    ├── ImageComponent
    │   ├── LogoComponent
    │   └── PhotoComponent
    │
    └── SummaryComponent
        ├── ExecutiveSummaryComponent
        └── KeyInsightsComponent
```

## Base Component Interface

All components inherit from `BaseComponent`:

```python
from abc import ABC, abstractmethod
from typing import Dict, Any
import pandas as pd
from pptx.slide import Slide

class BaseComponent(ABC):
    """Base class for all report components"""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize component with configuration

        Args:
            config: Component configuration dictionary
                {
                    "position": {"left": 1, "top": 2, "width": 8, "height": 4},
                    "styling": {...},
                    "data_config": {...}
                }
        """
        self.config = config
        self.position = config.get("position", {})
        self.styling = config.get("styling", {})
        self.data_config = config.get("data_config", {})

    @abstractmethod
    def render(self, slide: Slide, data: pd.DataFrame) -> None:
        """
        Render component on PowerPoint slide

        Args:
            slide: PowerPoint slide object
            data: Processed data for this component
        """
        pass

    @abstractmethod
    def validate(self) -> bool:
        """Validate component configuration"""
        pass

    def to_dict(self) -> Dict[str, Any]:
        """Serialize component to dictionary"""
        return {
            "type": self.__class__.__name__,
            "config": self.config
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Deserialize component from dictionary"""
        return cls(config=data["config"])
```

## Component Implementations

### 1. TableComponent

**Purpose**: Display data in tabular format with customizable styling

```python
from components.base_component import BaseComponent
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

class TableComponent(BaseComponent):
    """Table component for displaying structured data"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.columns = config.get("columns", [])
        self.title = config.get("title", "")
        self.show_header = config.get("show_header", True)
        self.alternating_rows = config.get("alternating_rows", True)

    def render(self, slide: Slide, data: pd.DataFrame) -> None:
        """Render table on slide"""

        # Get position
        left = Inches(self.position.get("left", 1))
        top = Inches(self.position.get("top", 2))
        width = Inches(self.position.get("width", 8))
        height = Inches(self.position.get("height", 4))

        # Filter columns
        if self.columns:
            data = data[self.columns]

        # Create table
        rows = len(data) + (1 if self.show_header else 0)
        cols = len(data.columns)

        table_shape = slide.shapes.add_table(
            rows=rows,
            cols=cols,
            left=left,
            top=top,
            width=width,
            height=height
        )
        table = table_shape.table

        # Add header
        if self.show_header:
            for col_idx, col_name in enumerate(data.columns):
                cell = table.cell(0, col_idx)
                cell.text = str(col_name)
                self._apply_header_styling(cell)

        # Add data
        start_row = 1 if self.show_header else 0
        for row_idx, (_, row) in enumerate(data.iterrows()):
            for col_idx, value in enumerate(row):
                cell = table.cell(start_row + row_idx, col_idx)
                cell.text = str(value)
                self._apply_data_styling(cell, row_idx)

    def _apply_header_styling(self, cell):
        """Apply styling to header cells"""
        # Background color
        fill = cell.fill
        fill.solid()
        header_color = self.styling.get("header_color", "#003366")
        fill.fore_color.rgb = RGBColor.from_string(header_color.replace("#", ""))

        # Text formatting
        paragraph = cell.text_frame.paragraphs[0]
        paragraph.font.bold = self.styling.get("header_bold", True)
        paragraph.font.size = Pt(self.styling.get("header_font_size", 12))
        paragraph.font.color.rgb = RGBColor(255, 255, 255)  # White text
        paragraph.alignment = PP_ALIGN.CENTER

    def _apply_data_styling(self, cell, row_idx):
        """Apply styling to data cells"""
        paragraph = cell.text_frame.paragraphs[0]
        paragraph.font.size = Pt(self.styling.get("data_font_size", 11))

        # Alternating row colors
        if self.alternating_rows and row_idx % 2 == 1:
            fill = cell.fill
            fill.solid()
            fill.fore_color.rgb = RGBColor(240, 240, 240)  # Light gray

    def validate(self) -> bool:
        """Validate component configuration"""
        required = ["position"]
        return all(key in self.config for key in required)
```

**Usage Example:**

```python
# Create table component
table = TableComponent({
    "columns": ["Kurum", "Toplam", "Pozitif", "Negatif"],
    "title": "Yönetici Özeti",
    "position": {"left": 1, "top": 2, "width": 8, "height": 4},
    "styling": {
        "header_color": "#003366",
        "header_bold": True,
        "header_font_size": 12,
        "data_font_size": 11,
        "alternating_rows": True
    }
})

# Add to template
template.add_component(slide_index=1, component=table)
```

### 2. ChartComponent

**Purpose**: Visualize data as bar, line, pie, or column charts

```python
from components.base_component import BaseComponent
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Inches

class ChartComponent(BaseComponent):
    """Chart component for data visualization"""

    CHART_TYPES = {
        "bar": XL_CHART_TYPE.BAR_CLUSTERED,
        "column": XL_CHART_TYPE.COLUMN_CLUSTERED,
        "line": XL_CHART_TYPE.LINE,
        "pie": XL_CHART_TYPE.PIE
    }

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.chart_type = config.get("chart_type", "column")
        self.x_axis = config.get("x_axis", "")
        self.y_axis = config.get("y_axis", "")
        self.title = config.get("title", "")
        self.legend = config.get("legend", True)
        self.colors = config.get("colors", [])

    def render(self, slide: Slide, data: pd.DataFrame) -> None:
        """Render chart on slide"""

        # Get position
        left = Inches(self.position.get("left", 1))
        top = Inches(self.position.get("top", 2))
        width = Inches(self.position.get("width", 8))
        height = Inches(self.position.get("height", 5))

        # Prepare chart data
        chart_data = CategoryChartData()
        chart_data.categories = data[self.x_axis].tolist()

        # Add series
        series_name = self.y_axis
        chart_data.add_series(series_name, data[self.y_axis].tolist())

        # Create chart
        chart_type_enum = self.CHART_TYPES.get(self.chart_type, XL_CHART_TYPE.COLUMN_CLUSTERED)

        chart_shape = slide.shapes.add_chart(
            chart_type_enum,
            left, top, width, height,
            chart_data
        )

        chart = chart_shape.chart

        # Set title
        if self.title:
            chart.has_title = True
            chart.chart_title.text_frame.text = self.title

        # Configure legend
        chart.has_legend = self.legend

        # Apply custom colors
        if self.colors:
            self._apply_colors(chart)

    def _apply_colors(self, chart):
        """Apply custom colors to chart series"""
        from pptx.dml.color import RGBColor

        for idx, series in enumerate(chart.series):
            if idx < len(self.colors):
                color_hex = self.colors[idx].replace("#", "")
                rgb = RGBColor.from_string(color_hex)
                series.format.fill.solid()
                series.format.fill.fore_color.rgb = rgb

    def validate(self) -> bool:
        """Validate component configuration"""
        required = ["chart_type", "x_axis", "y_axis", "position"]
        return all(key in self.config for key in required)
```

**Usage Example:**

```python
# Create chart component
chart = ChartComponent({
    "chart_type": "column",
    "x_axis": "Kurum",
    "y_axis": "Toplam",
    "title": "Kurumların Yansıma Sayısı Bazında Karşılaştırılması",
    "legend": True,
    "colors": ["#003366", "#FF6600"],
    "position": {"left": 1, "top": 2, "width": 8, "height": 5}
})

# Add to template
template.add_component(slide_index=4, component=chart)
```

### 3. TextComponent

**Purpose**: Add text boxes, titles, and paragraphs

```python
from components.base_component import BaseComponent
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

class TextComponent(BaseComponent):
    """Text component for titles, headings, paragraphs"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.text = config.get("text", "")
        self.text_type = config.get("text_type", "paragraph")  # title, heading, paragraph

    def render(self, slide: Slide, data: pd.DataFrame) -> None:
        """Render text on slide"""

        left = Inches(self.position.get("left", 1))
        top = Inches(self.position.get("top", 1))
        width = Inches(self.position.get("width", 8))
        height = Inches(self.position.get("height", 1))

        # Add text box
        textbox = slide.shapes.add_textbox(left, top, width, height)
        text_frame = textbox.text_frame

        # Add text
        text_frame.text = self.text

        # Apply styling
        paragraph = text_frame.paragraphs[0]

        if self.text_type == "title":
            paragraph.font.size = Pt(self.styling.get("font_size", 32))
            paragraph.font.bold = True
        elif self.text_type == "heading":
            paragraph.font.size = Pt(self.styling.get("font_size", 20))
            paragraph.font.bold = True
        else:  # paragraph
            paragraph.font.size = Pt(self.styling.get("font_size", 14))

        # Alignment
        alignment = self.styling.get("alignment", "left")
        if alignment == "center":
            paragraph.alignment = PP_ALIGN.CENTER
        elif alignment == "right":
            paragraph.alignment = PP_ALIGN.RIGHT

    def validate(self) -> bool:
        """Validate component configuration"""
        return "text" in self.config and "position" in self.config
```

## Template Structure with Components

Templates are JSON files that define which components appear on which slides:

```json
{
  "template_id": "bsh_monthly_media_2025",
  "name": "BSH Monthly Media Report",
  "client": "BSH",

  "slides": [
    {
      "slide_index": 0,
      "title": "Cover Slide",
      "components": [
        {
          "type": "TextComponent",
          "config": {
            "text": "Aylık Medya Yansıma Raporu",
            "text_type": "title",
            "position": {"left": 2, "top": 3, "width": 6, "height": 2},
            "styling": {"font_size": 44, "alignment": "center"}
          }
        },
        {
          "type": "ImageComponent",
          "config": {
            "image_path": "assets/bsh_logo.png",
            "position": {"left": 8, "top": 6, "width": 1.5, "height": 1}
          }
        }
      ]
    },
    {
      "slide_index": 1,
      "title": "Yönetici Özeti",
      "components": [
        {
          "type": "TableComponent",
          "config": {
            "columns": ["Kurum", "Toplam", "Pozitif", "Negatif", "Erişim"],
            "position": {"left": 0.5, "top": 1.5, "width": 9, "height": 5},
            "styling": {
              "header_color": "#003366",
              "alternating_rows": true
            }
          }
        }
      ]
    },
    {
      "slide_index": 4,
      "title": "Comparison Chart",
      "components": [
        {
          "type": "ChartComponent",
          "config": {
            "chart_type": "column",
            "x_axis": "Kurum",
            "y_axis": "Toplam",
            "title": "Kurumların Yansıma Sayısı",
            "colors": ["#003366", "#FF6600"],
            "position": {"left": 1, "top": 2, "width": 8, "height": 5}
          }
        }
      ]
    }
  ]
}
```

## Component Factory Pattern

Components are created using a factory pattern:

```python
class ComponentFactory:
    """Factory for creating components from configuration"""

    _component_types = {
        "TableComponent": TableComponent,
        "ChartComponent": ChartComponent,
        "TextComponent": TextComponent,
        "ImageComponent": ImageComponent,
        "SummaryComponent": SummaryComponent
    }

    @classmethod
    def create_component(cls, component_type: str, config: Dict[str, Any]) -> BaseComponent:
        """
        Create component from type and configuration

        Args:
            component_type: Component class name
            config: Component configuration

        Returns:
            Component instance
        """
        component_class = cls._component_types.get(component_type)

        if not component_class:
            raise ValueError(f"Unknown component type: {component_type}")

        return component_class(config)

    @classmethod
    def register_component(cls, component_type: str, component_class):
        """Register custom component type"""
        cls._component_types[component_type] = component_class
```

**Usage:**

```python
from components.factory import ComponentFactory

# Create component from configuration
component_config = {
    "type": "TableComponent",
    "config": {...}
}

component = ComponentFactory.create_component(
    component_config["type"],
    component_config["config"]
)

# Render component
component.render(slide, data)
```

## Template Rendering Engine

The report generator iterates through components and renders them:

```python
def generate_report_from_template(template_path: str, excel_path: str, output_path: str):
    """Generate report using component-based template"""

    # Load template
    with open(template_path) as f:
        template_config = json.load(f)

    # Load PowerPoint base
    prs = Presentation(template_config["ppt_template_path"])

    # Load and process data
    data = pd.read_excel(excel_path)

    # Process each slide
    for slide_config in template_config["slides"]:
        slide_index = slide_config["slide_index"]
        slide = prs.slides[slide_index]

        # Render each component
        for component_config in slide_config.get("components", []):
            # Create component
            component = ComponentFactory.create_component(
                component_config["type"],
                component_config["config"]
            )

            # Validate component
            if not component.validate():
                print(f"Warning: Invalid component configuration")
                continue

            # Render component on slide
            component.render(slide, data)

    # Save presentation
    prs.save(output_path)
```

## User-Created Custom Components

Users can create their own components by extending BaseComponent:

```python
# my_custom_components.py

from components.base_component import BaseComponent

class BrandedHeaderComponent(BaseComponent):
    """Custom header with company branding"""

    def __init__(self, config):
        super().__init__(config)
        self.company_name = config.get("company_name", "")
        self.logo_path = config.get("logo_path", "")

    def render(self, slide, data):
        # Add company logo
        # Add company name
        # Add decorative elements
        pass

    def validate(self):
        return "company_name" in self.config

# Register custom component
from components.factory import ComponentFactory
ComponentFactory.register_component("BrandedHeaderComponent", BrandedHeaderComponent)
```

## Benefits of Component Architecture

### 1. **Modularity**
- Each component is self-contained
- Easy to test and debug
- Clear separation of concerns

### 2. **Reusability**
- Define components once, use everywhere
- Share components across templates
- Build component library over time

### 3. **Customizability**
- Every aspect can be configured
- Users create custom components
- No code changes needed for new layouts

### 4. **Maintainability**
- Changes to one component don't affect others
- Easy to add new component types
- Clear upgrade path

### 5. **User-Friendliness**
- GUI can expose component properties
- Visual editing of components
- No coding required for basic usage

## Future Enhancements

### 1. Component Marketplace
- Share custom components
- Download community components
- Rate and review components

### 2. Visual Component Editor
- Drag-and-drop positioning
- WYSIWYG editing
- Real-time preview

### 3. Smart Components
- AI-powered layouts
- Auto-sizing and positioning
- Data-driven component suggestions

### 4. Component Versioning
- Track component changes
- Rollback to previous versions
- Migration tools

## Conclusion

The component-based architecture provides maximum flexibility while maintaining ease of use. Users can create professional reports without coding, while developers can extend the system with custom components.

This approach scales from simple single-slide reports to complex multi-page presentations with dozens of different component types.
