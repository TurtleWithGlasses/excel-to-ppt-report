"""
ReportForge Core Engine Package
Component factory, data mapping, template management, and PPT generation
"""

from core.component_factory import ComponentFactory
from core.data_mapper import DataMapper
from core.template_manager import TemplateManager
from core.ppt_generator import PPTGenerator

__all__ = [
    'ComponentFactory',
    'DataMapper',
    'TemplateManager',
    'PPTGenerator',
]
