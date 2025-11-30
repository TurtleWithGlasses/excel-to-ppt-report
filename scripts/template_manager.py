"""
Template Manager Module
Handles creation, storage, and loading of report templates
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import uuid


class TemplateManager:
    """Manages report templates - creation, saving, loading, and validation"""
    
    def __init__(self, templates_dir: str = "templates/configs"):
        """
        Initialize the template manager
        
        Args:
            templates_dir: Directory to store template configuration files
        """
        self.templates_dir = templates_dir
        self._ensure_templates_directory()
    
    def _ensure_templates_directory(self):
        """Create templates directory if it doesn't exist"""
        if not os.path.exists(self.templates_dir):
            os.makedirs(self.templates_dir)
            print(f"Created templates directory: {self.templates_dir}")
    
    def create_template(
        self,
        name: str,
        client: str,
        description: str = "",
        ppt_template_path: str = "",
    ) -> Dict[str, Any]:
        """
        Create a new template configuration
        
        Args:
            name: Template name
            client: Client/brand name
            description: Template description
            ppt_template_path: Path to PowerPoint template file
            
        Returns:
            Template configuration dictionary
        """
        template_id = str(uuid.uuid4())[:8]
        template = {
            "template_id": template_id,
            "name": name,
            "client": client,
            "description": description,
            "ppt_template_path": ppt_template_path,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "version": "1.0",
            "data_mapping": {
                "sheet_name": "",
                "columns": {},
                "filters": []
            },
            "slides": [],
            "processing_rules": {
                "sort_by": "",
                "sort_order": "descending",
                "filters": [],
                "aggregations": []
            },
            "formatting": {
                "number_format": {
                    "decimal_places": 2,
                    "use_thousands_separator": True
                },
                "date_format": "%Y-%m-%d",
                "currency_symbol": "₺"
            }
        }
        return template
    
    def add_slide_config(
        self,
        template: Dict[str, Any],
        slide_index: int,
        slide_type: str,
        title: str = "",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Add a slide configuration to template
        
        Args:
            template: Template dictionary
            slide_index: Position of slide in presentation
            slide_type: Type of slide (table, chart, text, mixed)
            title: Slide title
            **kwargs: Additional slide configuration
            
        Returns:
            Updated template dictionary
        """
        slide_config = {
            "slide_index": slide_index,
            "slide_type": slide_type,
            "title": title,
            "components": kwargs.get("components", []),
            "layout": kwargs.get("layout", "default")
        }
        
        template["slides"].append(slide_config)
        template["updated_at"] = datetime.now().isoformat()
        return template
    
    def add_table_component(
        self,
        slide_config: Dict[str, Any],
        columns: List[str],
        position: Dict[str, float],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Add a table component to a slide
        
        Args:
            slide_config: Slide configuration dictionary
            columns: List of column names to include
            position: Position dict with left, top, width, height (in inches)
            **kwargs: Additional table configuration (styling, etc.)
            
        Returns:
            Updated slide configuration
        """
        table_component = {
            "type": "table",
            "columns": columns,
            "position": position,
            "styling": {
                "header_bold": kwargs.get("header_bold", True),
                "header_font_size": kwargs.get("header_font_size", 12),
                "data_font_size": kwargs.get("data_font_size", 11),
                "alternating_rows": kwargs.get("alternating_rows", True)
            }
        }
        
        slide_config["components"].append(table_component)
        return slide_config
    
    def add_chart_component(
        self,
        slide_config: Dict[str, Any],
        chart_type: str,
        data_columns: Dict[str, str],
        position: Dict[str, float],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Add a chart component to a slide
        
        Args:
            slide_config: Slide configuration dictionary
            chart_type: Type of chart (bar, line, pie, column)
            data_columns: Dict mapping x_axis and y_axis to column names
            position: Position dict with left, top, width, height
            **kwargs: Additional chart configuration
            
        Returns:
            Updated slide configuration
        """
        chart_component = {
            "type": "chart",
            "chart_type": chart_type,
            "data_columns": data_columns,
            "position": position,
            "styling": {
                "title": kwargs.get("title", ""),
                "legend": kwargs.get("legend", True),
                "data_labels": kwargs.get("data_labels", False),
                "colors": kwargs.get("colors", [])
            }
        }
        
        slide_config["components"].append(chart_component)
        return slide_config
    
    def add_text_component(
        self,
        slide_config: Dict[str, Any],
        text_type: str,
        position: Dict[str, float],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Add a text component to a slide
        
        Args:
            slide_config: Slide configuration dictionary
            text_type: Type of text (static, dynamic, ai_generated)
            position: Position dict
            **kwargs: Additional text configuration
            
        Returns:
            Updated slide configuration
        """
        text_component = {
            "type": "text",
            "text_type": text_type,
            "content": kwargs.get("content", ""),
            "data_source": kwargs.get("data_source", ""),
            "position": position,
            "styling": {
                "font_size": kwargs.get("font_size", 14),
                "bold": kwargs.get("bold", False),
                "color": kwargs.get("color", "black"),
                "alignment": kwargs.get("alignment", "left")
            }
        }
        
        slide_config["components"].append(text_component)
        return slide_config
    
    def save_template(self, template: Dict[str, Any]) -> str:
        """
        Save template to JSON file
        
        Args:
            template: Template configuration dictionary
            
        Returns:
            Path to saved template file
        """
        filename = f"{template['template_id']}_{template['client']}_{template['name']}.json"
        filename = filename.replace(" ", "_").replace("/", "_")
        filepath = os.path.join(self.templates_dir, filename)
        
        template["updated_at"] = datetime.now().isoformat()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=2, ensure_ascii=False)
        
        print(f"Template saved: {filepath}")
        return filepath
    
    def load_template(self, template_id_or_path: str) -> Optional[Dict[str, Any]]:
        """
        Load template from file
        
        Args:
            template_id_or_path: Template ID or full path to template file
            
        Returns:
            Template configuration dictionary or None if not found
        """
        # If it's a full path, load directly
        if os.path.exists(template_id_or_path):
            filepath = template_id_or_path
        else:
            # Search for template by ID
            filepath = self._find_template_by_id(template_id_or_path)
        
        if not filepath:
            print(f"Template not found: {template_id_or_path}")
            return None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                template = json.load(f)
            print(f"Template loaded: {template['name']}")
            return template
        except Exception as e:
            print(f"Error loading template: {e}")
            return None
    
    def _find_template_by_id(self, template_id: str) -> Optional[str]:
        """Find template file by ID"""
        for filename in os.listdir(self.templates_dir):
            if filename.startswith(template_id) and filename.endswith('.json'):
                return os.path.join(self.templates_dir, filename)
        return None
    
    def list_templates(self) -> List[Dict[str, Any]]:
        """
        List all available templates
        
        Returns:
            List of template summary dictionaries
        """
        templates = []
        
        if not os.path.exists(self.templates_dir):
            return templates
        
        for filename in os.listdir(self.templates_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.templates_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        template = json.load(f)
                    templates.append({
                        "template_id": template.get("template_id"),
                        "name": template.get("name"),
                        "client": template.get("client"),
                        "description": template.get("description"),
                        "created_at": template.get("created_at"),
                        "filepath": filepath
                    })
                except Exception as e:
                    print(f"Error reading template {filename}: {e}")
        
        return templates
    
    def delete_template(self, template_id: str) -> bool:
        """
        Delete a template
        
        Args:
            template_id: Template ID to delete
            
        Returns:
            True if deleted successfully, False otherwise
        """
        filepath = self._find_template_by_id(template_id)
        if filepath and os.path.exists(filepath):
            os.remove(filepath)
            print(f"Template deleted: {filepath}")
            return True
        return False
    
    def validate_template(self, template: Dict[str, Any]) -> tuple[bool, List[str]]:
        """
        Validate template configuration
        
        Args:
            template: Template dictionary to validate
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check required fields
        required_fields = ["template_id", "name", "client", "data_mapping", "slides"]
        for field in required_fields:
            if field not in template:
                errors.append(f"Missing required field: {field}")
        
        # Validate data mapping
        if "data_mapping" in template:
            if not template["data_mapping"].get("sheet_name"):
                errors.append("Data mapping must specify sheet_name")
        
        # Validate slides
        if "slides" in template and len(template["slides"]) == 0:
            errors.append("Template must have at least one slide configuration")
        
        return len(errors) == 0, errors
    
    def export_template(self, template_id: str, export_path: str) -> bool:
        """Export template to a different location"""
        template = self.load_template(template_id)
        if not template:
            return False
        
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=2, ensure_ascii=False)
        print(f"Template exported to: {export_path}")
        return True
    
    def import_template(self, import_path: str) -> Optional[str]:
        """Import template from a file"""
        if not os.path.exists(import_path):
            print(f"Import file not found: {import_path}")
            return None
        
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                template = json.load(f)
            
            # Validate and save
            is_valid, errors = self.validate_template(template)
            if not is_valid:
                print(f"Invalid template: {errors}")
                return None
            
            filepath = self.save_template(template)
            return filepath
        except Exception as e:
            print(f"Error importing template: {e}")
            return None


# Example usage and template creation helper
def create_example_template():
    """Create an example template for BSH media analysis"""
    manager = TemplateManager()
    
    # Create base template
    template = manager.create_template(
        name="BSH Monthly Media Report",
        client="BSH",
        description="Monthly media analysis report for BSH and competitors",
        ppt_template_path="templates/BSH Kasım Ayı Aylık Medya Yansıma Raporu 24.pptx"
    )
    
    # Configure data mapping
    template["data_mapping"] = {
        "sheet_name": "BSH",
        "columns": {
            "Firma": "company",
            "Erişim": "reach",
            "StxCm": "stxcm",
            "Reklam Eşdeğeri": "ad_value",
            "Editör": "sentiment"
        },
        "filters": []
    }
    
    # Configure processing rules
    template["processing_rules"] = {
        "sort_by": "Toplam",
        "sort_order": "descending",
        "aggregations": [
            {
                "type": "group_by",
                "columns": ["Firma", "Editör"],
                "aggregation": "count"
            },
            {
                "type": "sum",
                "columns": ["Erişim", "StxCm", "Reklam Eşdeğeri"],
                "group_by": "Firma"
            }
        ]
    }
    
    # Add slide 1: Summary Table
    slide1 = {
        "slide_index": 0,
        "slide_type": "table",
        "title": "Monthly Summary",
        "components": []
    }
    
    manager.add_table_component(
        slide1,
        columns=["Kurum", "Toplam", "Pozitif", "Negatif", "Erişim", "STXCM", "Reklam Eşdeğeri"],
        position={"left": 0.5, "top": 1.5, "width": 9, "height": 5},
        header_bold=True,
        alternating_rows=True
    )
    
    template["slides"].append(slide1)
    
    # Save template
    filepath = manager.save_template(template)
    print(f"\nExample template created: {filepath}")
    return template


if __name__ == "__main__":
    # Create and save example template
    template = create_example_template()
    
    # List all templates
    manager = TemplateManager()
    print("\nAvailable templates:")
    for tmpl in manager.list_templates():
        print(f"  - {tmpl['name']} ({tmpl['client']}) - ID: {tmpl['template_id']}")






