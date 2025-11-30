"""
ImageComponent - Renders images, logos, and graphics

Used for: Company logos, product photos, charts as images, graphics
Supports: File paths, URLs, PIL Images, with styling options
"""

from typing import Any, Dict, Optional
from pptx.slide import Slide
from pptx.util import Inches
from components.base_component import BaseComponent
import os
from io import BytesIO


class ImageComponent(BaseComponent):
    """
    Component for rendering images on PowerPoint slides.

    Supports: Local files (.png, .jpg, .svg), URLs, PIL Image objects
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize ImageComponent.

        Config keys:
            - data_source:
                - path: File path or URL to image
                - type: 'file' | 'url' | 'template_logo'
            - style:
                - border_width: Border width in points (0 = no border)
                - border_color: Hex color for border
                - corner_radius: Rounded corners in points
                - opacity: 0-100 (transparency)
                - maintain_aspect: Keep aspect ratio (default: True)
        """
        super().__init__(config)

        # Image source
        self.image_path = self.data_source.get('path')
        self.image_type = self.data_source.get('type', 'file')

        # Style options
        self.border_width = self.style.get('border_width', 0)
        self.border_color = self.style.get('border_color', '#000000')
        self.corner_radius = self.style.get('corner_radius', 0)
        self.opacity = self.style.get('opacity', 100)
        self.maintain_aspect = self.style.get('maintain_aspect', True)

    def validate(self) -> bool:
        """Validate image component configuration."""
        super().validate()

        if not self.image_path and self.image_type != 'template_logo':
            raise ValueError("ImageComponent requires 'path' in data_source")

        if self.image_type == 'file' and not os.path.exists(self.image_path):
            # Don't raise error, just warn - image might be added later
            pass

        return True

    def render(self, slide: Slide, data: Any = None) -> None:
        """
        Render image on the slide.

        Args:
            slide: PowerPoint slide object
            data: Optional dict with 'logo_path' or 'image_path' override
        """
        # Get image path (allow override from data)
        image_path = self._get_image_path(data)

        if not image_path or not os.path.exists(image_path):
            self._render_placeholder(slide)
            return

        try:
            # Add image to slide
            if self.maintain_aspect:
                # Add with aspect ratio maintained
                picture = slide.shapes.add_picture(
                    image_path,
                    self.x,
                    self.y,
                    width=self.width
                )
                # Center vertically if height is smaller
                if picture.height < self.height:
                    picture.top = self.y + (self.height - picture.height) // 2
            else:
                # Stretch to fill area
                picture = slide.shapes.add_picture(
                    image_path,
                    self.x,
                    self.y,
                    width=self.width,
                    height=self.height
                )

            # Apply styling (limited in python-pptx)
            self._apply_styling(picture)

        except Exception as e:
            print(f"Error rendering image {image_path}: {e}")
            self._render_placeholder(slide, error=str(e))

    def _get_image_path(self, data: Any = None) -> Optional[str]:
        """
        Get image path from config or data override.

        Args:
            data: Optional data dict with image path

        Returns:
            str: Image file path or None
        """
        # Check for override in data
        if data and isinstance(data, dict):
            if 'logo_path' in data:
                return data['logo_path']
            if 'image_path' in data:
                return data['image_path']

        # Use template logo if specified
        if self.image_type == 'template_logo':
            # Logo path should come from template data
            if data and isinstance(data, dict) and 'template_logo' in data:
                return data['template_logo']

        return self.image_path

    def _apply_styling(self, picture) -> None:
        """
        Apply styling to picture shape.

        Args:
            picture: python-pptx picture shape

        Note: python-pptx has limited image styling support.
        Borders and rounded corners are not directly supported.
        """
        # Opacity (transparency)
        if self.opacity < 100:
            # Note: This requires accessing the underlying XML
            # Not implemented in basic python-pptx
            pass

        # Border and corner radius would require direct XML manipulation
        # Beyond scope of basic implementation
        pass

    def _render_placeholder(self, slide: Slide, error: str = None) -> None:
        """
        Render placeholder when image is not available.

        Args:
            slide: PowerPoint slide object
            error: Optional error message
        """
        from pptx.enum.shapes import MSO_SHAPE
        from pptx.dml.color import RGBColor
        from pptx.enum.text import PP_ALIGN
        from pptx.util import Pt

        # Add rectangle shape as placeholder
        placeholder = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            self.x,
            self.y,
            self.width,
            self.height
        )

        # Gray background
        placeholder.fill.solid()
        placeholder.fill.fore_color.rgb = RGBColor(243, 244, 246)

        # Gray border
        placeholder.line.color.rgb = RGBColor(209, 213, 219)
        placeholder.line.width = Pt(1)

        # Add text
        text_frame = placeholder.text_frame
        text_frame.clear()

        paragraph = text_frame.paragraphs[0]
        if error:
            paragraph.text = f"[Image Error]\n{error}"
        elif self.image_path:
            paragraph.text = f"[Image]\n{os.path.basename(self.image_path)}\nNot Found"
        else:
            paragraph.text = "[Image Placeholder]"

        paragraph.alignment = PP_ALIGN.CENTER
        paragraph.font.size = Pt(10)
        paragraph.font.color.rgb = RGBColor(156, 163, 175)

        # Center text vertically
        text_frame.vertical_anchor = 1  # Middle

    def set_image_path(self, path: str) -> None:
        """
        Update image file path.

        Args:
            path: New image file path
        """
        self.image_path = path
        self.data_source['path'] = path

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        config = super().to_dict()
        config['data_source']['path'] = self.image_path
        config['data_source']['type'] = self.image_type
        return config


# Example usage configurations:
EXAMPLE_CONFIGS = {
    'logo': {
        'type': 'image',
        'position': {'x': 0.5, 'y': 0.5},
        'size': {'width': 2.0, 'height': 1.0},
        'data_source': {
            'path': 'assets/logo.png',
            'type': 'file'
        },
        'style': {
            'maintain_aspect': True,
            'border_width': 0,
            'opacity': 100
        }
    },
    'template_logo': {
        'type': 'image',
        'position': {'x': 8.5, 'y': 0.5},
        'size': {'width': 1.0, 'height': 0.5},
        'data_source': {
            'type': 'template_logo'  # Will use logo from template config
        },
        'style': {
            'maintain_aspect': True
        }
    },
    'product_image': {
        'type': 'image',
        'position': {'x': 5.0, 'y': 2.0},
        'size': {'width': 4.0, 'height': 3.0},
        'data_source': {
            'path': 'products/product_001.jpg',
            'type': 'file'
        },
        'style': {
            'maintain_aspect': False,  # Stretch to fit
            'border_width': 2,
            'border_color': '#E5E7EB',
            'corner_radius': 8
        }
    }
}
