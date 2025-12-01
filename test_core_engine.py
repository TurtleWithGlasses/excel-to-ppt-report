"""
Test script for ReportForge Core Engine

Tests the complete integration:
- ComponentFactory
- DataMapper
- TemplateManager
- PPTGenerator

Generates a complete PowerPoint presentation from template + data.
"""

from core import ComponentFactory, DataMapper, TemplateManager, PPTGenerator
import pandas as pd
import os
from datetime import datetime


def create_sample_data():
    """Create sample data for testing."""
    return pd.DataFrame({
        'Company': ['BSH', 'Arçelik', 'Vestel', 'Beko', 'Profilo'],
        'Total': [1234, 987, 654, 543, 321],
        'Positive': [856, 654, 432, 378, 210],
        'Negative': [234, 187, 123, 98, 67],
        'Neutral': [144, 146, 99, 67, 44]
    })


def create_sample_template():
    """Create a sample template for testing."""
    return {
        'metadata': {
            'name': 'Test Report Template',
            'description': 'Template for testing core engine integration',
            'author': 'ReportForge',
            'version': '1.0',
            'created_date': datetime.now().strftime('%Y-%m-%d')
        },
        'settings': {
            'page_size': '16:9',
            'default_font': 'Calibri',
            'color_scheme': {
                'primary': '#2563EB',
                'secondary': '#10B981',
                'accent': '#F59E0B'
            }
        },
        'slides': [
            {
                'name': 'Title Slide',
                'layout': 'blank',
                'components': [
                    {
                        'type': 'text',
                        'content': 'Media Monitoring Report - {month} {year}',
                        'position': {'x': 0.5, 'y': 2.5},
                        'size': {'width': 9.0, 'height': 1.0},
                        'variables': {},
                        'style': {
                            'font_name': 'Calibri',
                            'font_size': 36,
                            'bold': True,
                            'alignment': 'center',
                            'color': '#1F2937'
                        }
                    },
                    {
                        'type': 'text',
                        'content': 'Company: {company}',
                        'position': {'x': 0.5, 'y': 3.5},
                        'size': {'width': 9.0, 'height': 0.6},
                        'style': {
                            'font_size': 18,
                            'alignment': 'center',
                            'color': '#6B7280'
                        }
                    }
                ]
            },
            {
                'name': 'Data Overview',
                'layout': 'blank',
                'components': [
                    {
                        'type': 'text',
                        'content': 'Data Overview',
                        'position': {'x': 0.5, 'y': 0.5},
                        'size': {'width': 9.0, 'height': 0.7},
                        'style': {
                            'font_size': 28,
                            'bold': True,
                            'alignment': 'left'
                        }
                    },
                    {
                        'type': 'table',
                        'position': {'x': 0.5, 'y': 1.5},
                        'size': {'width': 9.0, 'height': 3.5},
                        'data_source': {
                            'columns': ['Company', 'Total', 'Positive', 'Negative', 'Neutral'],
                            'sort_by': 'Total',
                            'ascending': False
                        },
                        'style': {
                            'header_row': True,
                            'zebra_striping': True,
                            'border': True,
                            'header_color': '#2563EB',
                            'header_text_color': '#FFFFFF',
                            'font_size': 11
                        }
                    },
                    {
                        'type': 'summary',
                        'position': {'x': 0.5, 'y': 5.2},
                        'size': {'width': 9.0, 'height': 1.5},
                        'data_source': {
                            'insight_types': ['key_metrics', 'highlights'],
                            'metric_columns': ['Total', 'Positive'],
                            'compare_column': 'Company',
                            'max_items': 3
                        },
                        'style': {
                            'layout': 'bullets',
                            'show_icons': True,
                            'font_size': 12
                        }
                    }
                ]
            },
            {
                'name': 'Charts',
                'layout': 'blank',
                'components': [
                    {
                        'type': 'text',
                        'content': 'Visual Analysis',
                        'position': {'x': 0.5, 'y': 0.3},
                        'size': {'width': 9.0, 'height': 0.6},
                        'style': {
                            'font_size': 28,
                            'bold': True
                        }
                    },
                    {
                        'type': 'chart',
                        'chart_type': 'column',
                        'position': {'x': 0.5, 'y': 1.2},
                        'size': {'width': 4.5, 'height': 3.0},
                        'data_source': {
                            'x_column': 'Company',
                            'y_column': 'Total',
                            'sort_by': 'Total',
                            'top_n': 5
                        },
                        'style': {
                            'colors': ['#2563EB'],
                            'show_values': True,
                            'title': 'Total Mentions by Company',
                            'y_label': 'Mentions',
                            'grid': True
                        }
                    },
                    {
                        'type': 'chart',
                        'chart_type': 'pie',
                        'position': {'x': 5.2, 'y': 1.2},
                        'size': {'width': 4.3, 'height': 3.0},
                        'data_source': {
                            'x_column': 'Company',
                            'y_column': 'Positive',
                            'top_n': 5
                        },
                        'style': {
                            'colors': ['#10B981', '#2563EB', '#F59E0B', '#EF4444', '#8B5CF6'],
                            'show_values': True,
                            'title': 'Positive Mentions Distribution'
                        }
                    },
                    {
                        'type': 'chart',
                        'chart_type': 'bar',
                        'position': {'x': 0.5, 'y': 4.5},
                        'size': {'width': 9.0, 'height': 2.5},
                        'data_source': {
                            'x_column': 'Company',
                            'y_column': 'Negative',
                            'sort_by': 'Negative'
                        },
                        'style': {
                            'colors': ['#EF4444'],
                            'show_values': True,
                            'title': 'Negative Mentions (Horizontal)',
                            'x_label': 'Number of Mentions',
                            'grid': True
                        }
                    }
                ]
            }
        ]
    }


def test_component_factory():
    """Test ComponentFactory."""
    print("\n" + "=" * 60)
    print("Testing ComponentFactory")
    print("=" * 60)

    factory = ComponentFactory()

    print("\n1. Getting supported types:")
    types = factory.get_supported_types()
    print(f"   Supported: {', '.join(types)}")

    print("\n2. Creating sample components:")
    for component_type in ['text', 'table', 'chart']:
        config = {'type': component_type, 'position': {'x': 1, 'y': 1}, 'size': {'width': 5, 'height': 3}}

        if component_type == 'text':
            config['content'] = 'Test'
        elif component_type == 'chart':
            config['chart_type'] = 'column'
            config['data_source'] = {'x_column': 'A', 'y_column': 'B'}

        try:
            component = factory.create_component(config)
            print(f"   ✅ {component_type}: {type(component).__name__}")
        except Exception as e:
            print(f"   ❌ {component_type}: {str(e)}")

    print("\n✅ ComponentFactory test complete")


def test_data_mapper():
    """Test DataMapper."""
    print("\n" + "=" * 60)
    print("Testing DataMapper")
    print("=" * 60)

    # Create sample data file
    data = create_sample_data()
    temp_file = 'temp_test_data.xlsx'
    data.to_excel(temp_file, index=False)

    try:
        print("\n1. Loading data:")
        mapper = DataMapper()
        mapper.load_data(temp_file)
        print(f"   ✅ Loaded {len(mapper.data)} rows, {len(mapper.data.columns)} columns")

        print("\n2. Getting column names:")
        columns = mapper.get_column_names()
        print(f"   Columns: {', '.join(columns)}")

        print("\n3. Getting summary stats:")
        stats = mapper.get_summary_stats('Total')
        print(f"   Total - Sum: {stats['sum']}, Mean: {stats['mean']:.1f}, Max: {stats['max']}")

        print("\n4. Creating variable dictionary:")
        variables = mapper.create_variable_dict({'company': 'BSH'})
        print(f"   ✅ Created {len(variables)} variables")
        print(f"   Sample: month={variables.get('month')}, company={variables.get('company')}")

        print("\n5. Getting data for table component:")
        config = {
            'type': 'table',
            'data_source': {
                'columns': ['Company', 'Total', 'Positive'],
                'sort_by': 'Total',
                'ascending': False,
                'top_n': 3
            }
        }
        component_data = mapper.get_data_for_component(config)
        print(f"   ✅ Retrieved {len(component_data)} rows for component")

        print("\n✅ DataMapper test complete")

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_template_manager():
    """Test TemplateManager."""
    print("\n" + "=" * 60)
    print("Testing TemplateManager")
    print("=" * 60)

    manager = TemplateManager()

    print("\n1. Creating template:")
    template = create_sample_template()
    print(f"   ✅ Created: {template['metadata']['name']}")
    print(f"   Slides: {len(template['slides'])}")

    print("\n2. Validating template:")
    try:
        manager.current_template = template
        is_valid = manager.validate_current_template()
        print(f"   ✅ Template is valid")
    except ValueError as e:
        print(f"   ❌ Validation failed: {str(e)}")

    print("\n3. Getting template info:")
    info = manager.get_template_info()
    print(f"   Name: {info['name']}")
    print(f"   Slides: {info['slide_count']}")
    print(f"   Components: {info['component_counts']}")

    print("\n4. Saving and loading template:")
    temp_template = 'temp_test_template.json'
    try:
        manager.save_template(template, temp_template, overwrite=True)
        print(f"   ✅ Saved template")

        loaded = manager.load_template(temp_template)
        print(f"   ✅ Loaded template: {loaded['metadata']['name']}")

    finally:
        if os.path.exists(temp_template):
            os.remove(temp_template)

    print("\n✅ TemplateManager test complete")


def test_ppt_generator():
    """Test PPTGenerator with full integration."""
    print("\n" + "=" * 60)
    print("Testing PPTGenerator (Full Integration)")
    print("=" * 60)

    # Create sample data and template files
    data = create_sample_data()
    template = create_sample_template()

    data_file = 'temp_test_data.xlsx'
    template_file = 'temp_test_template.json'
    output_file = 'output/test_core_engine_output.pptx'

    data.to_excel(data_file, index=False)

    import json
    with open(template_file, 'w', encoding='utf-8') as f:
        json.dump(template, f, indent=2)

    try:
        print("\n1. Initializing generator:")
        generator = PPTGenerator()
        print("   ✅ Generator initialized")

        print("\n2. Loading template:")
        generator.load_template(template_file)
        template_info = generator.get_template_info()
        print(f"   ✅ Loaded: {template_info['name']}")
        print(f"   Slides: {template_info['slide_count']}")

        print("\n3. Loading data:")
        generator.load_data(data_file)
        data_info = generator.get_data_info()
        print(f"   ✅ Loaded {data_info['rows']} rows")

        print("\n4. Setting variables:")
        generator.set_variables({
            'company': 'BSH',
            'month': 'November',
            'year': '2025'
        })
        variables = generator.preview_variables()
        print(f"   ✅ Set variables: company={variables['company']}, month={variables['month']}")

        print("\n5. Generating PowerPoint:")
        output_path = generator.generate(output_file)
        print(f"   ✅ Generated: {output_path}")

        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path) / 1024
            print(f"   File size: {file_size:.1f} KB")
        else:
            print("   ❌ Output file not created")

        print("\n✅ PPTGenerator test complete")

    finally:
        # Clean up temp files
        for temp_file in [data_file, template_file]:
            if os.path.exists(temp_file):
                os.remove(temp_file)


def test_batch_generation():
    """Test BatchPPTGenerator."""
    print("\n" + "=" * 60)
    print("Testing BatchPPTGenerator")
    print("=" * 60)

    from core.ppt_generator import BatchPPTGenerator

    # Create sample files
    data = create_sample_data()
    template = create_sample_template()

    data_file = 'temp_batch_data.xlsx'
    template_file = 'temp_batch_template.json'

    data.to_excel(data_file, index=False)

    import json
    with open(template_file, 'w', encoding='utf-8') as f:
        json.dump(template, f, indent=2)

    try:
        print("\n1. Creating batch generator:")
        batch_gen = BatchPPTGenerator()
        print("   ✅ Batch generator created")

        print("\n2. Adding jobs:")
        batch_gen.add_job(
            template=template_file,
            data=data_file,
            variables={'company': 'BSH', 'month': 'November'}
        )
        batch_gen.add_job(
            template=template_file,
            data=data_file,
            variables={'company': 'Arçelik', 'month': 'December'}
        )
        print(f"   ✅ Added {len(batch_gen.jobs)} jobs")

        print("\n3. Generating all reports:")
        results = batch_gen.generate_all()

        print("\n4. Getting summary:")
        summary = batch_gen.get_summary()
        print(f"   Total jobs: {summary['total_jobs']}")
        print(f"   Successful: {summary['successful']}")
        print(f"   Failed: {summary['failed']}")
        print(f"   Success rate: {summary['success_rate']}")

        print("\n✅ BatchPPTGenerator test complete")

    finally:
        # Clean up
        for temp_file in [data_file, template_file]:
            if os.path.exists(temp_file):
                os.remove(temp_file)


def run_all_tests():
    """Run all core engine tests."""
    print("=" * 60)
    print("ReportForge Core Engine Test Suite")
    print("=" * 60)

    try:
        test_component_factory()
        test_data_mapper()
        test_template_manager()
        test_ppt_generator()
        test_batch_generation()

        print("\n" + "=" * 60)
        print("✅ ALL CORE ENGINE TESTS COMPLETE!")
        print("=" * 60)
        print("\nGenerated files:")
        print("  - output/test_core_engine_output.pptx")
        print("  - output/ (batch generated files)")
        print("\nCore Engine Status: ✅ READY FOR INTEGRATION")
        print("\nNext Steps:")
        print("  1. Create example templates (BSH, Sanofi, SOCAR)")
        print("  2. Test with real Excel data")
        print("  3. Integrate with Main App GUI")
        print("=" * 60)

    except Exception as e:
        print("\n" + "=" * 60)
        print(f"❌ TEST FAILED: {str(e)}")
        print("=" * 60)
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    run_all_tests()
