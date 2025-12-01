"""
TemplateManager - Loads and manages PowerPoint report templates

This module handles template loading, validation, and management. Templates are
JSON files that define the structure of PowerPoint reports.
"""

from typing import Dict, Any, List, Optional
import json
import os
from pathlib import Path


class TemplateManager:
    """
    Manages PowerPoint report templates.

    Templates are JSON files that define:
    - Report metadata (name, description, author)
    - Slide layouts and components
    - Default styling
    - Data source mappings

    Template Structure:
    {
        "metadata": {
            "name": "BSH Monthly Report",
            "description": "Monthly media monitoring report for BSH",
            "author": "ReportForge",
            "version": "1.0",
            "created_date": "2025-01-15"
        },
        "settings": {
            "page_size": "16:9",
            "default_font": "Calibri",
            "color_scheme": {...}
        },
        "slides": [
            {
                "name": "Title Slide",
                "layout": "title",
                "components": [...]
            },
            ...
        ]
    }
    """

    def __init__(self, template_dir: str = "templates/configs"):
        """
        Initialize TemplateManager.

        Args:
            template_dir: Directory containing template JSON files
        """
        self.template_dir = template_dir
        self.current_template: Optional[Dict[str, Any]] = None
        self.template_path: Optional[str] = None

        # Create template directory if it doesn't exist
        Path(template_dir).mkdir(parents=True, exist_ok=True)

    def load_template(self, template_path: str) -> Dict[str, Any]:
        """
        Load a template from JSON file.

        Args:
            template_path: Path to template JSON file

        Returns:
            Template dictionary

        Raises:
            FileNotFoundError: If template file doesn't exist
            ValueError: If template is invalid JSON or fails validation

        Example:
            manager = TemplateManager()
            template = manager.load_template('templates/configs/BSH_Template.json')
        """
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template not found: {template_path}")

        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template = json.load(f)

            # Validate template
            self._validate_template(template)

            self.current_template = template
            self.template_path = template_path

            return template

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in template file: {str(e)}") from e
        except Exception as e:
            raise ValueError(f"Failed to load template: {str(e)}") from e

    def save_template(
        self,
        template: Dict[str, Any],
        file_path: str,
        overwrite: bool = False
    ) -> str:
        """
        Save a template to JSON file.

        Args:
            template: Template dictionary
            file_path: Path to save template
            overwrite: Allow overwriting existing file

        Returns:
            Path to saved template

        Raises:
            ValueError: If template is invalid
            FileExistsError: If file exists and overwrite=False

        Example:
            manager = TemplateManager()
            path = manager.save_template(template, 'templates/configs/new_template.json')
        """
        # Validate before saving
        self._validate_template(template)

        # Check if file exists
        if os.path.exists(file_path) and not overwrite:
            raise FileExistsError(
                f"Template file already exists: {file_path}. "
                f"Use overwrite=True to replace it."
            )

        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(template, f, indent=2, ensure_ascii=False)

            return file_path

        except Exception as e:
            raise Exception(f"Failed to save template: {str(e)}") from e

    def _validate_template(self, template: Dict[str, Any]) -> bool:
        """
        Validate template structure.

        Args:
            template: Template dictionary

        Returns:
            True if valid

        Raises:
            ValueError: If template is invalid
        """
        if not isinstance(template, dict):
            raise ValueError("Template must be a dictionary")

        # Check required top-level keys
        if 'slides' not in template:
            raise ValueError("Template must include 'slides' key")

        if not isinstance(template['slides'], list):
            raise ValueError("'slides' must be a list")

        if len(template['slides']) == 0:
            raise ValueError("Template must have at least one slide")

        # Validate metadata if present
        if 'metadata' in template:
            self._validate_metadata(template['metadata'])

        # Validate slides
        for idx, slide in enumerate(template['slides']):
            self._validate_slide(slide, idx)

        return True

    def _validate_metadata(self, metadata: Dict[str, Any]) -> bool:
        """Validate template metadata."""
        if not isinstance(metadata, dict):
            raise ValueError("Metadata must be a dictionary")

        recommended_keys = ['name', 'description', 'version']
        for key in recommended_keys:
            if key not in metadata:
                print(f"Warning: Metadata missing recommended key: '{key}'")

        return True

    def _validate_slide(self, slide: Dict[str, Any], index: int) -> bool:
        """
        Validate individual slide configuration.

        Args:
            slide: Slide dictionary
            index: Slide index (for error messages)

        Returns:
            True if valid

        Raises:
            ValueError: If slide is invalid
        """
        if not isinstance(slide, dict):
            raise ValueError(f"Slide {index} must be a dictionary")

        # Check for components
        if 'components' not in slide:
            raise ValueError(f"Slide {index} must include 'components' key")

        if not isinstance(slide['components'], list):
            raise ValueError(f"Slide {index} 'components' must be a list")

        # Validate components
        for comp_idx, component in enumerate(slide['components']):
            self._validate_component(component, index, comp_idx)

        return True

    def _validate_component(
        self,
        component: Dict[str, Any],
        slide_idx: int,
        comp_idx: int
    ) -> bool:
        """
        Validate component configuration.

        Args:
            component: Component dictionary
            slide_idx: Slide index
            comp_idx: Component index

        Returns:
            True if valid

        Raises:
            ValueError: If component is invalid
        """
        if not isinstance(component, dict):
            raise ValueError(
                f"Component {comp_idx} in slide {slide_idx} must be a dictionary"
            )

        if 'type' not in component:
            raise ValueError(
                f"Component {comp_idx} in slide {slide_idx} must include 'type' key"
            )

        valid_types = ['text', 'table', 'image', 'chart', 'summary']
        if component['type'] not in valid_types:
            raise ValueError(
                f"Component {comp_idx} in slide {slide_idx} has invalid type: "
                f"{component['type']}. Valid types: {', '.join(valid_types)}"
            )

        # Check for position and size
        if 'position' not in component:
            print(
                f"Warning: Component {comp_idx} in slide {slide_idx} "
                f"missing 'position' - will use defaults"
            )

        if 'size' not in component:
            print(
                f"Warning: Component {comp_idx} in slide {slide_idx} "
                f"missing 'size' - will use defaults"
            )

        return True

    def list_templates(self) -> List[Dict[str, str]]:
        """
        List all available templates in template directory.

        Returns:
            List of dictionaries with template information

        Example:
            manager = TemplateManager()
            templates = manager.list_templates()
            for template in templates:
                print(f"{template['name']} - {template['path']}")
        """
        templates = []

        if not os.path.exists(self.template_dir):
            return templates

        for file in os.listdir(self.template_dir):
            if file.endswith('.json'):
                file_path = os.path.join(self.template_dir, file)

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        template = json.load(f)

                    metadata = template.get('metadata', {})

                    templates.append({
                        'file_name': file,
                        'path': file_path,
                        'name': metadata.get('name', file.replace('.json', '')),
                        'description': metadata.get('description', 'No description'),
                        'version': metadata.get('version', 'Unknown'),
                        'slides': len(template.get('slides', []))
                    })

                except Exception as e:
                    print(f"Warning: Failed to read template {file}: {str(e)}")

        return templates

    def get_template_info(self, template_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Get information about a template.

        Args:
            template_path: Path to template (uses current if None)

        Returns:
            Dictionary with template information

        Example:
            manager = TemplateManager()
            manager.load_template('templates/configs/BSH_Template.json')
            info = manager.get_template_info()
        """
        template = self.current_template

        if template_path:
            template = self.load_template(template_path)

        if not template:
            return {'status': 'No template loaded'}

        metadata = template.get('metadata', {})
        settings = template.get('settings', {})
        slides = template.get('slides', [])

        # Count components by type
        component_counts = {}
        for slide in slides:
            for component in slide.get('components', []):
                comp_type = component.get('type', 'unknown')
                component_counts[comp_type] = component_counts.get(comp_type, 0) + 1

        return {
            'name': metadata.get('name', 'Unknown'),
            'description': metadata.get('description', ''),
            'version': metadata.get('version', 'Unknown'),
            'author': metadata.get('author', 'Unknown'),
            'slide_count': len(slides),
            'component_counts': component_counts,
            'settings': settings,
            'path': self.template_path
        }

    def get_slide(self, slide_index: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific slide from current template.

        Args:
            slide_index: Index of slide to retrieve

        Returns:
            Slide dictionary or None

        Example:
            manager = TemplateManager()
            manager.load_template('template.json')
            first_slide = manager.get_slide(0)
        """
        if not self.current_template:
            raise ValueError("No template loaded")

        slides = self.current_template.get('slides', [])

        if slide_index < 0 or slide_index >= len(slides):
            return None

        return slides[slide_index]

    def get_all_slides(self) -> List[Dict[str, Any]]:
        """
        Get all slides from current template.

        Returns:
            List of slide dictionaries
        """
        if not self.current_template:
            raise ValueError("No template loaded")

        return self.current_template.get('slides', [])

    def create_empty_template(
        self,
        name: str,
        description: str = "",
        author: str = "ReportForge"
    ) -> Dict[str, Any]:
        """
        Create an empty template structure.

        Args:
            name: Template name
            description: Template description
            author: Template author

        Returns:
            Empty template dictionary

        Example:
            manager = TemplateManager()
            template = manager.create_empty_template(
                name="My Report",
                description="Custom report template"
            )
        """
        from datetime import datetime

        template = {
            'metadata': {
                'name': name,
                'description': description,
                'author': author,
                'version': '1.0',
                'created_date': datetime.now().strftime('%Y-%m-%d'),
                'modified_date': datetime.now().strftime('%Y-%m-%d')
            },
            'settings': {
                'page_size': '16:9',
                'default_font': 'Calibri',
                'default_font_size': 11,
                'color_scheme': {
                    'primary': '#2563EB',
                    'secondary': '#10B981',
                    'accent': '#F59E0B',
                    'text': '#1F2937',
                    'background': '#FFFFFF'
                }
            },
            'slides': []
        }

        self.current_template = template
        return template

    def add_slide(
        self,
        name: str,
        layout: str = 'blank',
        components: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Add a slide to current template.

        Args:
            name: Slide name
            layout: Slide layout type
            components: List of component configurations

        Returns:
            Updated template

        Example:
            manager = TemplateManager()
            template = manager.create_empty_template("Test")
            manager.add_slide("Title Slide", layout="title", components=[...])
        """
        if not self.current_template:
            raise ValueError("No template loaded. Create or load a template first.")

        slide = {
            'name': name,
            'layout': layout,
            'components': components or []
        }

        self.current_template['slides'].append(slide)
        return self.current_template

    def validate_current_template(self) -> bool:
        """
        Validate the current template.

        Returns:
            True if valid

        Raises:
            ValueError: If template is invalid
        """
        if not self.current_template:
            raise ValueError("No template loaded")

        return self._validate_template(self.current_template)


# Example usage and test
if __name__ == '__main__':
    print("=" * 60)
    print("TemplateManager Test")
    print("=" * 60)

    manager = TemplateManager()

    print("\n1. Creating empty template:")
    template = manager.create_empty_template(
        name="Test Report",
        description="Test template for demonstration"
    )
    print(f"   ✅ Created: {template['metadata']['name']}")

    print("\n2. Adding slides:")
    manager.add_slide("Title Slide", layout="title", components=[
        {
            'type': 'text',
            'content': 'Test Report - {month}',
            'position': {'x': 0.5, 'y': 3.0},
            'size': {'width': 9.0, 'height': 1.0},
            'style': {'font_size': 32, 'bold': True, 'alignment': 'center'}
        }
    ])
    print(f"   ✅ Added slide: Title Slide")

    manager.add_slide("Data Slide", layout="blank", components=[
        {
            'type': 'table',
            'position': {'x': 0.5, 'y': 1.5},
            'size': {'width': 9.0, 'height': 4.0},
            'data_source': {'columns': ['Company', 'Total']},
            'style': {'header_row': True}
        },
        {
            'type': 'chart',
            'chart_type': 'column',
            'position': {'x': 0.5, 'y': 5.5},
            'size': {'width': 9.0, 'height': 2.0},
            'data_source': {'x_column': 'Company', 'y_column': 'Total'}
        }
    ])
    print(f"   ✅ Added slide: Data Slide")

    print("\n3. Validating template:")
    try:
        manager.validate_current_template()
        print("   ✅ Template is valid")
    except ValueError as e:
        print(f"   ❌ Validation failed: {str(e)}")

    print("\n4. Getting template info:")
    info = manager.get_template_info()
    print(f"   Name: {info['name']}")
    print(f"   Slides: {info['slide_count']}")
    print(f"   Components: {info['component_counts']}")

    print("\n5. Saving template:")
    temp_path = 'temp_test_template.json'
    try:
        saved_path = manager.save_template(template, temp_path, overwrite=True)
        print(f"   ✅ Saved to: {saved_path}")

        print("\n6. Loading template:")
        loaded = manager.load_template(temp_path)
        print(f"   ✅ Loaded: {loaded['metadata']['name']}")

        print("\n7. Getting slides:")
        slides = manager.get_all_slides()
        print(f"   ✅ Retrieved {len(slides)} slides")

    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)

    print("\n" + "=" * 60)
    print("✅ TemplateManager Test Complete!")
    print("=" * 60)
