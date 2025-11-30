"""
PPTGenerator - Main PowerPoint generation engine

This is the core engine that brings everything together:
- Loads templates
- Loads and maps data
- Creates components
- Generates PowerPoint presentations

This is the main entry point for report generation.
"""

from typing import Dict, Any, List, Optional, Union
from pptx import Presentation
from pptx.util import Inches
import os
from datetime import datetime

from core.component_factory import ComponentFactory
from core.data_mapper import DataMapper
from core.template_manager import TemplateManager


class PPTGenerator:
    """
    Main PowerPoint report generation engine.

    Orchestrates the entire report generation process:
    1. Load template
    2. Load and map data
    3. Create presentation
    4. Add slides
    5. Render components
    6. Save PowerPoint file

    Example:
        generator = PPTGenerator()
        generator.load_template('templates/configs/BSH_Template.json')
        generator.load_data('data/BSH_November.xlsx')
        output_path = generator.generate('output/BSH_Report.pptx')
    """

    def __init__(
        self,
        template_dir: str = "templates/configs",
        output_dir: str = "output"
    ):
        """
        Initialize PPTGenerator.

        Args:
            template_dir: Directory containing template JSON files
            output_dir: Directory for generated PowerPoint files
        """
        self.template_manager = TemplateManager(template_dir)
        self.data_mapper = DataMapper()
        self.component_factory = ComponentFactory()

        self.output_dir = output_dir
        self.presentation: Optional[Presentation] = None
        self.custom_variables: Dict[str, Any] = {}

        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

    def load_template(self, template_path: str) -> Dict[str, Any]:
        """
        Load a PowerPoint template.

        Args:
            template_path: Path to template JSON file

        Returns:
            Template dictionary

        Example:
            generator.load_template('templates/configs/BSH_Template.json')
        """
        template = self.template_manager.load_template(template_path)
        return template

    def load_data(self, data_path: str, sheet_name: Union[str, int] = 0) -> None:
        """
        Load data from Excel/CSV file.

        Args:
            data_path: Path to data file
            sheet_name: Sheet name or index for Excel files

        Example:
            generator.load_data('data/BSH_November.xlsx')
        """
        self.data_mapper.load_data(data_path, sheet_name)

    def set_variables(self, variables: Dict[str, Any]) -> None:
        """
        Set custom variables for text substitution.

        Args:
            variables: Dictionary of variables

        Example:
            generator.set_variables({
                'company': 'BSH',
                'month': 'November',
                'report_type': 'Monthly Media Analysis'
            })
        """
        self.custom_variables.update(variables)

    def generate(
        self,
        output_path: Optional[str] = None,
        template_pptx: Optional[str] = None
    ) -> str:
        """
        Generate PowerPoint presentation.

        Args:
            output_path: Path to save generated PowerPoint
                        If None, auto-generates based on template name
            template_pptx: Path to PowerPoint template file (.pptx)
                          If None, creates blank presentation

        Returns:
            Path to generated PowerPoint file

        Example:
            path = generator.generate('output/BSH_November_Report.pptx')
        """
        # Check if template is loaded
        if not self.template_manager.current_template:
            raise ValueError("No template loaded. Call load_template() first.")

        # Create presentation
        if template_pptx and os.path.exists(template_pptx):
            self.presentation = Presentation(template_pptx)
        else:
            self.presentation = Presentation()
            self._set_presentation_size()

        # Get template
        template = self.template_manager.current_template

        # Generate slides
        slides = template.get('slides', [])
        for slide_config in slides:
            self._generate_slide(slide_config)

        # Determine output path
        if not output_path:
            output_path = self._generate_output_path(template)

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Save presentation
        self.presentation.save(output_path)

        return output_path

    def _set_presentation_size(self) -> None:
        """Set presentation slide size based on template settings."""
        if not self.presentation:
            return

        template = self.template_manager.current_template
        settings = template.get('settings', {})
        page_size = settings.get('page_size', '16:9')

        # Standard PowerPoint sizes
        if page_size == '16:9':
            self.presentation.slide_width = Inches(10)
            self.presentation.slide_height = Inches(5.625)
        elif page_size == '4:3':
            self.presentation.slide_width = Inches(10)
            self.presentation.slide_height = Inches(7.5)

    def _generate_slide(self, slide_config: Dict[str, Any]) -> None:
        """
        Generate a single slide.

        Args:
            slide_config: Slide configuration from template
        """
        if not self.presentation:
            raise ValueError("Presentation not initialized")

        # Get layout
        layout_name = slide_config.get('layout', 'blank')
        layout_index = self._get_layout_index(layout_name)

        # Add slide
        slide_layout = self.presentation.slide_layouts[layout_index]
        slide = self.presentation.slides.add_slide(slide_layout)

        # Get components
        components_config = slide_config.get('components', [])

        # Render each component
        for component_config in components_config:
            self._render_component(slide, component_config)

    def _get_layout_index(self, layout_name: str) -> int:
        """
        Get slide layout index by name.

        Args:
            layout_name: Layout name (title, blank, etc.)

        Returns:
            Layout index
        """
        layout_map = {
            'title': 0,
            'title_content': 1,
            'section': 2,
            'two_content': 3,
            'comparison': 4,
            'blank': 5,
            'content': 6
        }

        return layout_map.get(layout_name.lower(), 5)  # Default to blank

    def _render_component(self, slide, component_config: Dict[str, Any]) -> None:
        """
        Render a component on a slide.

        Args:
            slide: PowerPoint slide object
            component_config: Component configuration
        """
        try:
            # Create component
            component = self.component_factory.create_component(component_config)

            # Get data for component
            component_data = self.data_mapper.get_data_for_component(
                component_config,
                self.custom_variables
            )

            # Render component
            component.render(slide, component_data)

        except IndexError as e:
            # Handle tuple/list index errors specifically
            import traceback
            print(f"Warning: Failed to render component (index error): {str(e)}")
            print(f"Component config: {component_config.get('type', 'unknown')}")
            traceback.print_exc()
            # Continue with other components
        except Exception as e:
            print(f"Warning: Failed to render component: {str(e)}")
            import traceback
            traceback.print_exc()  # Print full traceback for debugging
            # Continue with other components

    def _generate_output_path(self, template: Dict[str, Any]) -> str:
        """
        Generate output path based on template name and timestamp.

        Args:
            template: Template dictionary

        Returns:
            Output file path
        """
        metadata = template.get('metadata', {})
        template_name = metadata.get('name', 'Report')

        # Clean filename
        clean_name = template_name.replace(' ', '_').replace('/', '_')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        filename = f"{clean_name}_{timestamp}.pptx"
        return os.path.join(self.output_dir, filename)

    def generate_from_config(
        self,
        template_path: str,
        data_path: str,
        output_path: Optional[str] = None,
        variables: Optional[Dict[str, Any]] = None,
        sheet_name: Union[str, int] = 0
    ) -> str:
        """
        Generate PowerPoint from template and data (convenience method).

        Args:
            template_path: Path to template JSON file
            data_path: Path to data file (Excel/CSV)
            output_path: Path to save generated PowerPoint
            variables: Custom variables for text substitution
            sheet_name: Sheet name or index for Excel files

        Returns:
            Path to generated PowerPoint file

        Example:
            generator = PPTGenerator()
            output = generator.generate_from_config(
                template_path='templates/configs/BSH_Template.json',
                data_path='data/BSH_November.xlsx',
                variables={'company': 'BSH', 'month': 'November'}
            )
        """
        # Load template
        self.load_template(template_path)

        # Load data
        self.load_data(data_path, sheet_name)

        # Set variables
        if variables:
            self.set_variables(variables)

        # Generate
        return self.generate(output_path)

    def get_template_info(self) -> Dict[str, Any]:
        """
        Get information about loaded template.

        Returns:
            Template information dictionary
        """
        return self.template_manager.get_template_info()

    def get_data_info(self) -> Dict[str, Any]:
        """
        Get information about loaded data.

        Returns:
            Data information dictionary
        """
        return self.data_mapper.get_info()

    def validate_template(self) -> bool:
        """
        Validate current template.

        Returns:
            True if valid

        Raises:
            ValueError: If template is invalid
        """
        return self.template_manager.validate_current_template()

    def preview_variables(self) -> Dict[str, Any]:
        """
        Preview available variables for text substitution.

        Returns:
            Dictionary of all available variables
        """
        return self.data_mapper.create_variable_dict(self.custom_variables)

    def reset(self) -> None:
        """Reset generator to initial state."""
        self.presentation = None
        self.custom_variables = {}
        self.data_mapper.reset()


class BatchPPTGenerator:
    """
    Batch PowerPoint generation for multiple reports.

    Example:
        batch_gen = BatchPPTGenerator()
        batch_gen.add_job(
            template='templates/configs/BSH_Template.json',
            data='data/BSH_November.xlsx',
            variables={'company': 'BSH'}
        )
        batch_gen.add_job(
            template='templates/configs/Sanofi_Template.json',
            data='data/Sanofi_November.xlsx',
            variables={'company': 'Sanofi'}
        )
        results = batch_gen.generate_all()
    """

    def __init__(self, output_dir: str = "output"):
        """
        Initialize BatchPPTGenerator.

        Args:
            output_dir: Directory for generated PowerPoint files
        """
        self.output_dir = output_dir
        self.jobs: List[Dict[str, Any]] = []
        self.results: List[Dict[str, Any]] = []

    def add_job(
        self,
        template: str,
        data: str,
        output: Optional[str] = None,
        variables: Optional[Dict[str, Any]] = None,
        sheet_name: Union[str, int] = 0
    ) -> None:
        """
        Add a generation job to the batch.

        Args:
            template: Path to template JSON file
            data: Path to data file
            output: Output path (optional)
            variables: Custom variables
            sheet_name: Sheet name or index
        """
        self.jobs.append({
            'template': template,
            'data': data,
            'output': output,
            'variables': variables or {},
            'sheet_name': sheet_name
        })

    def generate_all(self) -> List[Dict[str, Any]]:
        """
        Generate all jobs in the batch.

        Returns:
            List of results with status and output paths
        """
        self.results = []

        for idx, job in enumerate(self.jobs):
            print(f"Processing job {idx + 1}/{len(self.jobs)}...")

            try:
                generator = PPTGenerator(output_dir=self.output_dir)

                output_path = generator.generate_from_config(
                    template_path=job['template'],
                    data_path=job['data'],
                    output_path=job['output'],
                    variables=job['variables'],
                    sheet_name=job['sheet_name']
                )

                self.results.append({
                    'job_index': idx,
                    'status': 'success',
                    'output_path': output_path,
                    'template': job['template'],
                    'data': job['data']
                })

                print(f"✅ Job {idx + 1} completed: {output_path}")

            except Exception as e:
                self.results.append({
                    'job_index': idx,
                    'status': 'failed',
                    'error': str(e),
                    'template': job['template'],
                    'data': job['data']
                })

                print(f"❌ Job {idx + 1} failed: {str(e)}")

        return self.results

    def get_summary(self) -> Dict[str, Any]:
        """
        Get summary of batch generation results.

        Returns:
            Summary dictionary
        """
        if not self.results:
            return {'status': 'No jobs completed'}

        successful = sum(1 for r in self.results if r['status'] == 'success')
        failed = sum(1 for r in self.results if r['status'] == 'failed')

        return {
            'total_jobs': len(self.jobs),
            'successful': successful,
            'failed': failed,
            'success_rate': f"{(successful / len(self.jobs) * 100):.1f}%",
            'results': self.results
        }


# Example usage
if __name__ == '__main__':
    print("=" * 60)
    print("PPTGenerator Test")
    print("=" * 60)

    print("\nThis is a placeholder test.")
    print("Full integration test requires:")
    print("  1. Template JSON file")
    print("  2. Sample Excel data file")
    print("  3. Component library")
    print("\nRun test_core_engine.py for complete testing.")

    print("\n" + "=" * 60)
    print("✅ PPTGenerator Module Loaded!")
    print("=" * 60)
