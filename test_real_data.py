"""
Real Data Testing Script for ReportForge
Tests report generation with real/sample data files
"""

import os
import sys
import time
from datetime import datetime
from core import PPTGenerator
from validate_data import DataValidator


class ReportTester:
    """Automated testing for report generation"""

    def __init__(self):
        self.results = []

    def test_report_generation(self, template_path: str, data_path: str,
                               template_name: str, variables: dict = None) -> dict:
        """
        Test report generation with specific template and data

        Returns:
            dict with test results
        """
        result = {
            'template': template_name,
            'template_path': template_path,
            'data_path': data_path,
            'success': False,
            'error': None,
            'output_file': None,
            'file_size': 0,
            'generation_time': 0,
            'validation_passed': False
        }

        print(f"\n{'='*70}")
        print(f"Testing: {template_name}")
        print(f"Template: {template_path}")
        print(f"Data: {data_path}")
        print('='*70)

        # Step 1: Validate data first
        print("\n[1/4] Validating data file...")
        validator = DataValidator()
        is_valid, validation_report = validator.validate_file(data_path, template_name)
        result['validation_passed'] = is_valid

        if not is_valid:
            print("[X] Data validation failed!")
            validator.print_report(validation_report)
            result['error'] = "Data validation failed"
            return result

        print("[OK] Data validation passed")

        # Step 2: Check template exists
        print("\n[2/4] Checking template file...")
        if not os.path.exists(template_path):
            print(f"[X] Template file not found: {template_path}")
            result['error'] = "Template file not found"
            return result

        print("[OK] Template file exists")

        # Step 3: Generate report
        print("\n[3/4] Generating PowerPoint report...")

        # Default variables if not provided
        if variables is None:
            variables = {
                'month': datetime.now().strftime('%B'),
                'year': datetime.now().strftime('%Y'),
                'date': datetime.now().strftime('%d.%m.%Y'),
                'report_name': f"{template_name} Test Report"
            }

        try:
            start_time = time.time()
            generator = PPTGenerator()
            output_path = generator.generate_from_config(
                template_path=template_path,
                data_path=data_path,
                variables=variables
            )
            generation_time = time.time() - start_time

            result['success'] = True
            result['output_file'] = output_path
            result['generation_time'] = generation_time

            print(f"[OK] Report generated successfully in {generation_time:.2f} seconds")
            print(f"   Output: {output_path}")

        except Exception as e:
            result['error'] = str(e)
            print(f"[X] Report generation failed: {str(e)}")
            return result

        # Step 4: Validate output file
        print("\n[4/4] Validating output file...")
        if not os.path.exists(output_path):
            result['success'] = False
            result['error'] = "Output file not created"
            print("[X] Output file not found")
            return result

        file_size = os.path.getsize(output_path)
        result['file_size'] = file_size

        # File size check (should be > 50KB for real content)
        if file_size < 50000:
            result['success'] = False
            result['error'] = f"Output file too small ({file_size} bytes) - likely missing content"
            print(f"[!] WARNING: File size is only {file_size:,} bytes (expected > 50KB)")
        else:
            print(f"[OK] Output file size: {file_size:,} bytes ({file_size/1024:.1f} KB)")

        return result

    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)

        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r['success'])
        failed_tests = total_tests - passed_tests

        print(f"\nTotal Tests: {total_tests}")
        print(f"[OK] Passed: {passed_tests}")
        print(f"[X] Failed: {failed_tests}")

        print("\nDetailed Results:")
        print("-" * 70)

        for i, result in enumerate(self.results, 1):
            status = "[PASS]" if result['success'] else "[FAIL]"
            print(f"\n{i}. {result['template']}: {status}")
            print(f"   Template: {result['template_path']}")
            print(f"   Data: {result['data_path']}")

            if result['success']:
                print(f"   Output: {result['output_file']}")
                print(f"   Size: {result['file_size']:,} bytes ({result['file_size']/1024:.1f} KB)")
                print(f"   Time: {result['generation_time']:.2f} seconds")
            else:
                print(f"   Error: {result['error']}")

        print("\n" + "="*70)

        # Overall result
        if failed_tests == 0:
            print("*** ALL TESTS PASSED! ***")
        else:
            print(f"[!] {failed_tests} TEST(S) FAILED - Review errors above")

        print("="*70 + "\n")


def test_all_samples():
    """Test all sample data files"""
    tester = ReportTester()

    # Define test cases
    test_cases = [
        {
            'template_path': 'templates/configs/BSH_Template.json',
            'data_path': 'data/samples/BSH_Sample_Data.xlsx',
            'template_name': 'BSH',
            'variables': {'month': 'Kasım', 'year': '2024'}
        },
        {
            'template_path': 'templates/configs/Sanofi_Template.json',
            'data_path': 'data/samples/Sanofi_Sample_Data.xlsx',
            'template_name': 'Sanofi',
            'variables': {'month': 'November', 'year': '2024'}
        },
        {
            'template_path': 'templates/configs/SOCAR_Template.json',
            'data_path': 'data/samples/SOCAR_Sample_Data.xlsx',
            'template_name': 'SOCAR',
            'variables': {'month': 'November', 'year': '2024'}
        }
    ]

    print("\n" + "="*70)
    print("REPORTFORGE - REAL DATA TESTING")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

    # Run tests
    for test_case in test_cases:
        result = tester.test_report_generation(
            template_path=test_case['template_path'],
            data_path=test_case['data_path'],
            template_name=test_case['template_name'],
            variables=test_case.get('variables')
        )
        tester.results.append(result)

    # Print summary
    tester.print_summary()

    # Return exit code (0 = success, 1 = failure)
    failed_count = sum(1 for r in tester.results if not r['success'])
    return 0 if failed_count == 0 else 1


def test_single_template(template_path: str, data_path: str, template_name: str):
    """Test a single template with specific data"""
    tester = ReportTester()

    result = tester.test_report_generation(
        template_path=template_path,
        data_path=data_path,
        template_name=template_name
    )

    tester.results.append(result)
    tester.print_summary()

    return 0 if result['success'] else 1


def main():
    """Main entry point"""
    if len(sys.argv) > 3:
        # Test specific template
        template_path = sys.argv[1]
        data_path = sys.argv[2]
        template_name = sys.argv[3]

        exit_code = test_single_template(template_path, data_path, template_name)
        sys.exit(exit_code)
    else:
        # Test all samples
        exit_code = test_all_samples()
        sys.exit(exit_code)


if __name__ == '__main__':
    main()
