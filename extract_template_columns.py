"""
Extract Required Columns from Templates
Analyzes template JSON files to extract all column names used in data sources
"""

import json
import os
from typing import Set, List


def extract_columns_from_template(template_path: str) -> Set[str]:
    """Extract all column names used in a template"""
    columns = set()

    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template_data = json.load(f)

        slides = template_data.get('slides', [])

        for slide in slides:
            components = slide.get('components', [])

            for component in components:
                data_source = component.get('data_source', {})

                if not data_source:
                    continue

                # Extract various column types
                column_keys = [
                    'x_column', 'y_column', 'series_column',
                    'compare_column', 'sort_by', 'columns',
                    'metric_columns'
                ]

                for key in column_keys:
                    value = data_source.get(key)

                    if isinstance(value, str):
                        columns.add(value)
                    elif isinstance(value, list):
                        columns.update(value)

        return columns

    except Exception as e:
        print(f"Error reading template {template_path}: {e}")
        return set()


def analyze_all_templates():
    """Analyze all templates and print column requirements"""
    templates_dir = "templates/configs"

    print("="*70)
    print("TEMPLATE COLUMN ANALYSIS")
    print("="*70)

    for filename in sorted(os.listdir(templates_dir)):
        if not filename.endswith('.json'):
            continue

        template_path = os.path.join(templates_dir, filename)

        # Get template name
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_data = json.load(f)

            if 'metadata' in template_data:
                template_name = template_data['metadata'].get('name', filename[:-5])
            else:
                template_name = template_data.get('name', filename[:-5])
        except:
            template_name = filename[:-5]

        # Extract columns
        columns = extract_columns_from_template(template_path)

        print(f"\n{template_name}")
        print(f"File: {filename}")
        print(f"Required Columns ({len(columns)}):")
        for col in sorted(columns):
            print(f"  - {col}")


if __name__ == '__main__':
    analyze_all_templates()
