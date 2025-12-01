"""
Data Validation Script for ReportForge
Validates Excel data files before report generation
"""

import pandas as pd
import os
import sys
from typing import Dict, List, Tuple

class DataValidator:
    """Validates Excel data files for PowerPoint report generation"""

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []

    def validate_file(self, file_path: str, template_name: str) -> Tuple[bool, Dict]:
        """
        Validate an Excel file for a specific template

        Returns:
            (is_valid, report_dict)
        """
        self.errors = []
        self.warnings = []
        self.info = []

        # Step 1: File exists and readable
        if not os.path.exists(file_path):
            self.errors.append(f"File not found: {file_path}")
            return False, self._generate_report()

        try:
            # Step 2: Load Excel file
            df = pd.read_excel(file_path)
            self.info.append(f"File loaded: {len(df)} rows, {len(df.columns)} columns")

            # Step 3: Check if empty
            if df.empty:
                self.errors.append("Excel file is empty (no data rows)")
                return False, self._generate_report()

            # Step 4: Get required columns for template
            required_cols, optional_cols = self._get_template_columns(template_name)

            # Step 5: Validate required columns
            missing_required = []
            for col in required_cols:
                if col not in df.columns:
                    missing_required.append(col)

            if missing_required:
                self.errors.append(f"Missing required columns: {', '.join(missing_required)}")
                self.info.append(f"Available columns: {', '.join(df.columns.tolist())}")
                return False, self._generate_report()

            # Step 6: Check optional columns
            missing_optional = []
            for col in optional_cols:
                if col not in df.columns:
                    missing_optional.append(col)

            if missing_optional:
                self.warnings.append(f"Missing optional columns: {', '.join(missing_optional)}")

            # Step 7: Validate data types and content
            self._validate_data_quality(df, required_cols + optional_cols)

            # Step 8: Generate summary
            is_valid = len(self.errors) == 0
            return is_valid, self._generate_report()

        except Exception as e:
            self.errors.append(f"Error reading Excel file: {str(e)}")
            return False, self._generate_report()

    def _get_template_columns(self, template_name: str) -> Tuple[List[str], List[str]]:
        """Get required and optional columns for a template"""

        # Define column requirements based on actual template analysis
        templates = {
            'BSH': {
                'required': ['Firma', 'Net Etki', 'Erişim', 'Reklam Eşdeğeri'],
                'optional': ['Algı', 'Medya Kapsam', 'Medya Tür', 'Medya Şehir']
            },
            'Sanofi': {
                'required': ['FİRMALAR', 'OLUMLU', 'OLUMSUZ', 'TOTAL'],
                'optional': ['sentiment_type', 'value']
            },
            'SOCAR': {
                'required': ['Bölge', 'Net Etki', 'Erişim', 'Toplam Haber'],
                'optional': ['Algı', 'Kategori', 'Medya Türü', 'Haber Sayısı']
            }
        }

        # Try to match template name
        for key in templates:
            if key.lower() in template_name.lower():
                return templates[key]['required'], templates[key]['optional']

        # Default: no specific requirements
        return [], []

    def _validate_data_quality(self, df: pd.DataFrame, columns: List[str]):
        """Validate data quality for specific columns"""

        for col in columns:
            if col not in df.columns:
                continue

            # Check for empty values
            empty_count = df[col].isna().sum()
            if empty_count > 0:
                percentage = (empty_count / len(df)) * 100
                if percentage > 50:
                    self.warnings.append(f"Column '{col}': {percentage:.1f}% empty values ({empty_count}/{len(df)} rows)")
                elif percentage > 0:
                    self.info.append(f"Column '{col}': {empty_count} empty values ({percentage:.1f}%)")

            # Check data type based on column name
            if 'date' in col.lower():
                # Should be datetime
                if not pd.api.types.is_datetime64_any_dtype(df[col]):
                    try:
                        pd.to_datetime(df[col], errors='coerce')
                        self.info.append(f"Column '{col}': Can be converted to datetime")
                    except Exception:
                        self.warnings.append(f"Column '{col}': Expected date format, got {df[col].dtype}")

            elif any(keyword in col.lower() for keyword in ['mentions', 'reach', 'impressions', 'count']):
                # Should be numeric
                if not pd.api.types.is_numeric_dtype(df[col]):
                    self.warnings.append(f"Column '{col}': Expected numeric, got {df[col].dtype}")
                else:
                    # Check for negative values
                    if (df[col] < 0).any():
                        neg_count = (df[col] < 0).sum()
                        self.warnings.append(f"Column '{col}': Contains {neg_count} negative values")

            # Check for special characters issues
            if df[col].dtype == 'object':
                # Sample first few values
                sample = df[col].dropna().head(3).tolist()
                if sample:
                    self.info.append(f"Column '{col}': Sample values: {sample}")

    def _generate_report(self) -> Dict:
        """Generate validation report"""
        return {
            'errors': self.errors,
            'warnings': self.warnings,
            'info': self.info,
            'is_valid': len(self.errors) == 0
        }

    def print_report(self, report: Dict):
        """Print validation report to console"""
        print("\n" + "="*70)
        print("DATA VALIDATION REPORT")
        print("="*70)

        if report['errors']:
            print("\n[X] ERRORS (must fix):")
            for i, error in enumerate(report['errors'], 1):
                print(f"  {i}. {error}")

        if report['warnings']:
            print("\n[!] WARNINGS (should review):")
            for i, warning in enumerate(report['warnings'], 1):
                print(f"  {i}. {warning}")

        if report['info']:
            print("\n[i] INFORMATION:")
            for i, info in enumerate(report['info'], 1):
                print(f"  {i}. {info}")

        print("\n" + "="*70)
        if report['is_valid']:
            print("[OK] VALIDATION PASSED - Data is ready for report generation")
        else:
            print("[FAIL] VALIDATION FAILED - Fix errors before generating report")
        print("="*70 + "\n")


def validate_sample_data():
    """Validate all sample data files"""
    validator = DataValidator()

    # Test data files
    test_files = [
        ('data/samples/BSH_Sample_Data.xlsx', 'BSH'),
        ('data/samples/Sanofi_Sample_Data.xlsx', 'Sanofi'),
        ('data/samples/SOCAR_Sample_Data.xlsx', 'SOCAR')
    ]

    results = []

    for file_path, template_name in test_files:
        print(f"\n{'='*70}")
        print(f"Validating: {file_path}")
        print(f"Template: {template_name}")
        print('='*70)

        is_valid, report = validator.validate_file(file_path, template_name)
        validator.print_report(report)

        results.append({
            'file': file_path,
            'template': template_name,
            'valid': is_valid
        })

    # Summary
    print("\n" + "="*70)
    print("VALIDATION SUMMARY")
    print("="*70)
    for result in results:
        status = "[PASS]" if result['valid'] else "[FAIL]"
        print(f"{status} - {result['template']}: {result['file']}")
    print("="*70 + "\n")


def main():
    """Main entry point"""
    if len(sys.argv) > 2:
        # Validate specific file
        file_path = sys.argv[1]
        template_name = sys.argv[2]

        validator = DataValidator()
        is_valid, report = validator.validate_file(file_path, template_name)
        validator.print_report(report)

        sys.exit(0 if is_valid else 1)
    else:
        # Validate all sample data
        validate_sample_data()


if __name__ == '__main__':
    main()
