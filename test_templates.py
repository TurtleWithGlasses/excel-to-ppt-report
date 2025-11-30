"""
Test all templates with sample data

This script tests the BSH, Sanofi, and SOCAR templates with sample data
to verify the complete system works end-to-end.
"""

from core import PPTGenerator
import os


def test_bsh_template():
    """Test BSH template with sample data."""
    print("\n" + "=" * 60)
    print("Testing BSH Template")
    print("=" * 60)

    try:
        generator = PPTGenerator()

        print("\n1. Loading template...")
        generator.load_template('templates/configs/BSH_Template.json')
        template_info = generator.get_template_info()
        print(f"   Template: {template_info['name']}")
        print(f"   Slides: {template_info['slide_count']}")

        print("\n2. Loading sample data...")
        generator.load_data('data/samples/BSH_Sample_Data.xlsx')
        data_info = generator.get_data_info()
        print(f"   Rows: {data_info['rows']}")
        print(f"   Columns: {data_info['columns']}")

        print("\n3. Setting variables...")
        generator.set_variables({
            'month': 'Kasım',
            'year': '2024',
            'date': '2024-11-30'
        })
        print("   Variables set: month, year, date")

        print("\n4. Generating PowerPoint...")
        output_path = generator.generate('output/BSH_Test_Report.pptx')

        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path) / 1024
            print(f"   [OK] Generated: {output_path}")
            print(f"   File size: {file_size:.1f} KB")
            return True
        else:
            print("   [FAILED] Output file not created")
            return False

    except Exception as e:
        print(f"   [ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_sanofi_template():
    """Test Sanofi template with sample data."""
    print("\n" + "=" * 60)
    print("Testing Sanofi Template")
    print("=" * 60)

    try:
        generator = PPTGenerator()

        print("\n1. Loading template...")
        generator.load_template('templates/configs/Sanofi_Template.json')
        template_info = generator.get_template_info()
        print(f"   Template: {template_info['name']}")
        print(f"   Slides: {template_info['slide_count']}")

        print("\n2. Loading sample data...")
        generator.load_data('data/samples/Sanofi_Sample_Data.xlsx')
        data_info = generator.get_data_info()
        print(f"   Rows: {data_info['rows']}")
        print(f"   Columns: {data_info['columns']}")

        print("\n3. Setting variables...")
        generator.set_variables({
            'month': 'Ekim',
            'year': '2025',
            'date': '2025-10-31'
        })
        print("   Variables set: month, year, date")

        print("\n4. Generating PowerPoint...")
        output_path = generator.generate('output/Sanofi_Test_Report.pptx')

        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path) / 1024
            print(f"   [OK] Generated: {output_path}")
            print(f"   File size: {file_size:.1f} KB")
            return True
        else:
            print("   [FAILED] Output file not created")
            return False

    except Exception as e:
        print(f"   [ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_socar_template():
    """Test SOCAR template with sample data."""
    print("\n" + "=" * 60)
    print("Testing SOCAR Template")
    print("=" * 60)

    try:
        generator = PPTGenerator()

        print("\n1. Loading template...")
        generator.load_template('templates/configs/SOCAR_Template.json')
        template_info = generator.get_template_info()
        print(f"   Template: {template_info['name']}")
        print(f"   Slides: {template_info['slide_count']}")

        print("\n2. Loading sample data...")
        generator.load_data('data/samples/SOCAR_Sample_Data.xlsx')
        data_info = generator.get_data_info()
        print(f"   Rows: {data_info['rows']}")
        print(f"   Columns: {data_info['columns']}")

        print("\n3. Setting variables...")
        generator.set_variables({
            'month': 'Ekim',
            'year': '2025',
            'date': '2025-10-31'
        })
        print("   Variables set: month, year, date")

        print("\n4. Generating PowerPoint...")
        output_path = generator.generate('output/SOCAR_Test_Report.pptx')

        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path) / 1024
            print(f"   [OK] Generated: {output_path}")
            print(f"   File size: {file_size:.1f} KB")
            return True
        else:
            print("   [FAILED] Output file not created")
            return False

    except Exception as e:
        print(f"   [ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def run_all_template_tests():
    """Run all template tests."""
    print("=" * 60)
    print("ReportForge Template Test Suite")
    print("=" * 60)
    print("\nTesting all industry templates with sample data...")

    results = {
        'BSH': test_bsh_template(),
        'Sanofi': test_sanofi_template(),
        'SOCAR': test_socar_template()
    }

    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    successful = sum(1 for r in results.values() if r)
    total = len(results)

    for template, success in results.items():
        status = "[OK]" if success else "[FAILED]"
        print(f"  {status} {template} Template")

    print("\n" + "-" * 60)
    print(f"Results: {successful}/{total} templates passed")
    print(f"Success rate: {(successful/total*100):.0f}%")
    print("=" * 60)

    if successful == total:
        print("\n[OK] ALL TEMPLATES WORKING!")
        print("\nGenerated reports:")
        print("  - output/BSH_Test_Report.pptx")
        print("  - output/Sanofi_Test_Report.pptx")
        print("  - output/SOCAR_Test_Report.pptx")
        print("\nOpen these files in PowerPoint to view the results.")
    else:
        print("\n[WARNING] Some templates failed. Check errors above.")

    print("=" * 60)


if __name__ == '__main__':
    run_all_template_tests()
