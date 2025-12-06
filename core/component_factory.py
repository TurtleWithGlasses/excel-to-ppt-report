"""
ComponentFactory - Creates component instances from JSON configuration

This factory pattern enables template-driven report generation by instantiating
the correct component type based on configuration dictionaries.
"""

from typing import Dict, Any, List, Optional
from components import (
    BaseComponent,
    TextComponent,
    TableComponent,
    ImageComponent,
    ChartComponent,
    SummaryComponent
)


class ComponentFactory:
    """
    Factory class for creating component instances from configuration.

    Supports all 6 component types:
    - text: TextComponent
    - table: TableComponent
    - image: ImageComponent
    - chart: ChartComponent
    - summary: SummaryComponent
    """

    # Component type mapping
    COMPONENT_TYPES = {
        'text': TextComponent,
        'table': TableComponent,
        'image': ImageComponent,
        'chart': ChartComponent,
        'summary': SummaryComponent
    }

    @classmethod
    def create_component(cls, config: Dict[str, Any], template: Optional[Dict[str, Any]] = None) -> BaseComponent:
        """
        Create a component instance from configuration.

        Args:
            config: Component configuration dictionary
                Must include 'type' key with valid component type
            template: Optional template dictionary (for brand colors and settings)

        Returns:
            Component instance (subclass of BaseComponent)

        Raises:
            ValueError: If component type is invalid or missing
            Exception: If component initialization fails

        Example:
            config = {
                'type': 'text',
                'content': 'Hello {name}',
                'position': {'x': 0.5, 'y': 1.0},
                'size': {'width': 9.0, 'height': 1.0},
                'style': {'font_size': 24, 'bold': True}
            }
            component = ComponentFactory.create_component(config, template=template_dict)
        """
        if not isinstance(config, dict):
            raise ValueError("Configuration must be a dictionary")

        component_type = config.get('type')

        if not component_type:
            raise ValueError("Component configuration must include 'type' key")

        component_class = cls.COMPONENT_TYPES.get(component_type)

        if component_class is None:
            valid_types = ', '.join(cls.COMPONENT_TYPES.keys())
            raise ValueError(
                f"Invalid component type: '{component_type}'. "
                f"Valid types are: {valid_types}"
            )

        try:
            component = component_class(config, template=template)
            return component
        except Exception as e:
            raise Exception(
                f"Failed to create {component_type} component: {str(e)}"
            ) from e

    @classmethod
    def create_components(cls, configs: List[Dict[str, Any]], template: Optional[Dict[str, Any]] = None) -> List[BaseComponent]:
        """
        Create multiple components from a list of configurations.

        Args:
            configs: List of component configuration dictionaries
            template: Optional template dictionary (for brand colors and settings)

        Returns:
            List of component instances

        Raises:
            ValueError: If configs is not a list
            Exception: If any component creation fails

        Example:
            configs = [
                {'type': 'text', 'content': 'Title', ...},
                {'type': 'table', 'data_source': {...}, ...},
                {'type': 'chart', 'chart_type': 'column', ...}
            ]
            components = ComponentFactory.create_components(configs, template=template_dict)
        """
        if not isinstance(configs, list):
            raise ValueError("Configurations must be a list")

        components = []

        for idx, config in enumerate(configs):
            try:
                component = cls.create_component(config, template=template)
                components.append(component)
            except Exception as e:
                raise Exception(
                    f"Failed to create component at index {idx}: {str(e)}"
                ) from e

        return components

    @classmethod
    def validate_config(cls, config: Dict[str, Any], template: Optional[Dict[str, Any]] = None) -> bool:
        """
        Validate a component configuration without creating the instance.

        Args:
            config: Component configuration dictionary
            template: Optional template dictionary (for brand colors and settings)

        Returns:
            True if configuration is valid

        Raises:
            ValueError: If configuration is invalid

        Example:
            config = {'type': 'text', 'content': 'Test', ...}
            is_valid = ComponentFactory.validate_config(config, template=template_dict)
        """
        if not isinstance(config, dict):
            raise ValueError("Configuration must be a dictionary")

        component_type = config.get('type')

        if not component_type:
            raise ValueError("Component configuration must include 'type' key")

        if component_type not in cls.COMPONENT_TYPES:
            valid_types = ', '.join(cls.COMPONENT_TYPES.keys())
            raise ValueError(
                f"Invalid component type: '{component_type}'. "
                f"Valid types are: {valid_types}"
            )

        # Create and validate component
        component_class = cls.COMPONENT_TYPES[component_type]
        try:
            component = component_class(config, template=template)
            component.validate()
            return True
        except Exception as e:
            raise ValueError(
                f"Component configuration validation failed: {str(e)}"
            ) from e

    @classmethod
    def get_supported_types(cls) -> List[str]:
        """
        Get list of supported component types.

        Returns:
            List of component type strings

        Example:
            types = ComponentFactory.get_supported_types()
            # Returns: ['text', 'table', 'image', 'chart', 'summary']
        """
        return list(cls.COMPONENT_TYPES.keys())

    @classmethod
    def get_component_class(cls, component_type: str) -> Optional[type]:
        """
        Get the component class for a given type.

        Args:
            component_type: Component type string

        Returns:
            Component class or None if type not found

        Example:
            cls = ComponentFactory.get_component_class('text')
            # Returns: TextComponent class
        """
        return cls.COMPONENT_TYPES.get(component_type)


# Example configurations for each component type
EXAMPLE_CONFIGS = {
    'text': {
        'type': 'text',
        'content': 'Report for {company} - {month}',
        'position': {'x': 0.5, 'y': 0.5},
        'size': {'width': 9.0, 'height': 1.0},
        'variables': {'company': 'BSH', 'month': 'November'},
        'style': {
            'font_name': 'Calibri',
            'font_size': 32,
            'bold': True,
            'alignment': 'center',
            'color': '#1F2937'
        }
    },
    'table': {
        'type': 'table',
        'position': {'x': 0.5, 'y': 2.0},
        'size': {'width': 9.0, 'height': 4.0},
        'data_source': {
            'columns': ['Company', 'Total', 'Positive', 'Negative'],
            'sort_by': 'Total',
            'ascending': False,
            'top_n': 10
        },
        'style': {
            'header_row': True,
            'zebra_striping': True,
            'border': True,
            'header_color': '#2563EB',
            'header_text_color': '#FFFFFF',
            'font_size': 10
        }
    },
    'image': {
        'type': 'image',
        'position': {'x': 8.5, 'y': 0.5},
        'size': {'width': 1.0, 'height': 0.8},
        'data_source': {
            'path': 'assets/logo.png',
            'type': 'file'
        },
        'style': {
            'maintain_aspect': True
        }
    },
    'chart': {
        'type': 'chart',
        'chart_type': 'column',
        'position': {'x': 0.5, 'y': 2.0},
        'size': {'width': 9.0, 'height': 4.0},
        'data_source': {
            'x_column': 'Company',
            'y_column': 'Total',
            'sort_by': 'Total',
            'top_n': 10
        },
        'style': {
            'colors': ['#2563EB', '#10B981', '#F59E0B'],
            'show_values': True,
            'title': 'Media Mentions by Company',
            'y_label': 'Number of Mentions',
            'grid': True,
            'legend_position': 'bottom'
        }
    },
    'summary': {
        'type': 'summary',
        'position': {'x': 0.5, 'y': 5.0},
        'size': {'width': 9.0, 'height': 2.0},
        'data_source': {
            'insight_types': ['key_metrics', 'highlights', 'trends'],
            'metric_columns': ['Total', 'Positive', 'Negative'],
            'compare_column': 'Company',
            'time_column': 'Month',
            'max_items': 5
        },
        'style': {
            'layout': 'callout_boxes',
            'show_icons': True,
            'highlight_color': '#EFF6FF'
        }
    }
}


def test_factory():
    """
    Test function to verify ComponentFactory works correctly.
    Run this to test all component creation.
    """
    print("=" * 60)
    print("ComponentFactory Test")
    print("=" * 60)

    print("\n1. Testing supported types:")
    types = ComponentFactory.get_supported_types()
    print(f"   Supported types: {', '.join(types)}")

    print("\n2. Testing individual component creation:")
    for component_type in types:
        try:
            config = EXAMPLE_CONFIGS[component_type]
            component = ComponentFactory.create_component(config)
            print(f"   ✅ {component_type}: {type(component).__name__}")
        except Exception as e:
            print(f"   ❌ {component_type}: {str(e)}")

    print("\n3. Testing batch component creation:")
    try:
        all_configs = list(EXAMPLE_CONFIGS.values())
        components = ComponentFactory.create_components(all_configs)
        print(f"   ✅ Created {len(components)} components successfully")
    except Exception as e:
        print(f"   ❌ Batch creation failed: {str(e)}")

    print("\n4. Testing validation:")
    for component_type in types:
        try:
            config = EXAMPLE_CONFIGS[component_type]
            is_valid = ComponentFactory.validate_config(config)
            print(f"   ✅ {component_type}: Valid")
        except Exception as e:
            print(f"   ❌ {component_type}: {str(e)}")

    print("\n5. Testing error handling:")
    try:
        ComponentFactory.create_component({'type': 'invalid_type'})
    except ValueError as e:
        print(f"   ✅ Invalid type caught: {str(e)[:50]}...")

    try:
        ComponentFactory.create_component({})
    except ValueError as e:
        print(f"   ✅ Missing type caught: {str(e)[:50]}...")

    print("\n" + "=" * 60)
    print("✅ ComponentFactory Test Complete!")
    print("=" * 60)


if __name__ == '__main__':
    test_factory()
