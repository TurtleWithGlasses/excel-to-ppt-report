"""
BaseComponent - Abstract base class for all report components

This is the foundation class that all components (Table, Chart, Text, Image, Summary)
inherit from. It defines the common interface and shared functionality.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from pptx.slide import Slide
from pptx.util import Inches, Pt


class BaseComponent(ABC):
    """
    Abstract base class for all PowerPoint report components.

    All components must implement the render() method to generate
    their content on a PowerPoint slide.
    """

    def __init__(self, config: Dict[str, Any], template: Optional[Dict[str, Any]] = None):
        """
        Initialize component with configuration.

        Args:
            config (dict): Component configuration containing:
                - type: Component type (table, chart, text, image, summary)
                - position: {x, y} coordinates in inches
                - size: {width, height} in inches
                - data_source: Data configuration (varies by component)
                - style: Visual styling options
            template (dict, optional): Template dictionary with settings (for brand colors)
        """
        self.config = config
        self.type = config.get('type', 'unknown')
        self.template = template  # Store template reference for brand colors

        # Position and size (in inches)
        position = config.get('position', {'x': 0.5, 'y': 1.0})
        self.x = Inches(position.get('x', 0.5))
        self.y = Inches(position.get('y', 1.0))

        size = config.get('size', {'width': 9.0, 'height': 5.0})
        self.width = Inches(size.get('width', 9.0))
        self.height = Inches(size.get('height', 5.0))

        # Data source configuration
        self.data_source = config.get('data_source', {})

        # Style configuration
        self.style = config.get('style', {})

        # Note: validate() should be called by subclasses after they set their attributes
        # to avoid AttributeError when validate() tries to access subclass-specific attributes

    def validate(self) -> bool:
        """
        Validate component configuration.

        Returns:
            bool: True if valid, raises ValueError if invalid

        Raises:
            ValueError: If configuration is invalid
        """
        if not self.type:
            raise ValueError("Component type is required")

        if self.width.inches <= 0 or self.height.inches <= 0:
            raise ValueError("Component size must be positive")

        if self.x.inches < 0 or self.y.inches < 0:
            raise ValueError("Component position must be non-negative")

        return True

    @abstractmethod
    def render(self, slide: Slide, data: Any) -> None:
        """
        Render the component on a PowerPoint slide.

        This method must be implemented by all component subclasses.

        Args:
            slide: python-pptx Slide object to render on
            data: Data to render (structure varies by component)

        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError("Subclasses must implement render() method")

    def get_font_size(self, default: int = 11) -> Pt:
        """
        Get font size from style configuration.

        Args:
            default: Default font size in points

        Returns:
            Pt: Font size in points
        """
        size = self.style.get('font_size', default)
        return Pt(size)

    def get_color(self, color_key: str, default: str = '#000000') -> tuple:
        """
        Get RGB color from hex string.

        Args:
            color_key: Key in style dict (e.g., 'text_color', 'background_color')
            default: Default hex color

        Returns:
            tuple: RGB values (r, g, b) as integers 0-255
        """
        hex_color = self.style.get(color_key, default)
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def get_alignment(self) -> str:
        """
        Get text alignment from style.

        Returns:
            str: Alignment ('left', 'center', 'right', 'justify')
        """
        return self.style.get('alignment', 'left')

    def get_font_name(self) -> str:
        """
        Get font name from style.

        Returns:
            str: Font family name
        """
        return self.style.get('font_name', 'Calibri')

    def get_bold(self) -> bool:
        """
        Get bold setting from style.

        Returns:
            bool: True if bold
        """
        return self.style.get('bold', False)

    def get_italic(self) -> bool:
        """
        Get italic setting from style.

        Returns:
            bool: True if italic
        """
        return self.style.get('italic', False)

    def get_template_colors(self) -> Optional[Dict[str, str]]:
        """
        Get brand colors from template settings.

        Returns:
            Dictionary of color names to hex values, or None if not available
            Example: {'primary': '#2563EB', 'secondary': '#10B981', ...}

        Example:
            colors = self.get_template_colors()
            if colors:
                primary = colors.get('primary')
        """
        if not self.template:
            return None

        settings = self.template.get('settings', {})
        color_scheme = settings.get('color_scheme', {})

        if not color_scheme:
            return None

        return color_scheme

    def get_template_color_list(self) -> List[str]:
        """
        Get brand colors as a list of hex values for use in charts/components.

        Returns:
            List of hex color strings in order: primary, secondary, accent, negative, neutral
            Falls back to default colors if template colors not available

        Example:
            colors = self.get_template_color_list()
            # Returns: ['#2563EB', '#10B981', '#F59E0B', '#EF4444', '#6B7280']
        """
        color_scheme = self.get_template_colors()

        if not color_scheme:
            # Default fallback colors
            return ['#2563EB', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899']

        # Extract colors in priority order
        colors = []
        color_keys = ['primary', 'secondary', 'accent', 'negative', 'neutral']

        for key in color_keys:
            if key in color_scheme:
                colors.append(color_scheme[key])

        # Add any additional colors from scheme
        for key, value in color_scheme.items():
            if key not in color_keys and isinstance(value, str) and value.startswith('#'):
                colors.append(value)

        # Ensure we have at least some colors
        if not colors:
            return ['#2563EB', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899']

        return colors

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert component to dictionary (for JSON serialization).

        Returns:
            dict: Component configuration
        """
        return {
            'type': self.type,
            'position': {
                'x': self.x.inches,
                'y': self.y.inches
            },
            'size': {
                'width': self.width.inches,
                'height': self.height.inches
            },
            'data_source': self.data_source,
            'style': self.style
        }

    @classmethod
    def from_dict(cls, config: Dict[str, Any]) -> 'BaseComponent':
        """
        Create component from dictionary configuration.

        Args:
            config: Component configuration dictionary

        Returns:
            BaseComponent: Component instance
        """
        return cls(config)

    def __repr__(self) -> str:
        """String representation of component."""
        return f"{self.__class__.__name__}(type='{self.type}', pos=({self.x.inches}, {self.y.inches}), size=({self.width.inches}, {self.height.inches}))"
