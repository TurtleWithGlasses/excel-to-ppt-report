# Real Data Testing Plan

## Overview
This document outlines the comprehensive testing plan for ReportForge with real production data from BSH, Sanofi, and SOCAR.

## Testing Objectives

1. **Data Compatibility**
   - Verify system handles real-world Excel file structures
   - Test with various data formats (numbers, dates, text, percentages)
   - Validate column mapping across different naming conventions

2. **Component Rendering**
   - Ensure all 6 component types render correctly with real data
   - Test edge cases (empty data, missing columns, special characters)
   - Verify chart rendering with actual metrics

3. **Performance**
   - Measure generation time with realistic data volumes
   - Test memory usage with large Excel files
   - Validate batch generation capabilities

4. **Error Handling**
   - Test graceful failures with malformed data
   - Verify clear error messages for missing columns
   - Ensure system doesn't crash with unexpected data

## Test Scenarios

### Scenario 1: BSH Consumer Electronics Report

**Data Requirements:**
- Monthly media coverage statistics
- Product mention counts across channels
- Sentiment analysis (positive/negative/neutral)
- Top media outlets
- Share of voice metrics

**Components to Test:**
- Text: Month/year substitution, company name
- Table: Media coverage breakdown by channel
- Chart (Column): Monthly trend of mentions
- Chart (Pie): Sentiment distribution
- Summary: Auto-generated insights

**Expected Results:**
- All text variables substituted correctly
- Tables render with proper formatting
- Charts display actual data trends
- Summary insights reflect real metrics

### Scenario 2: Sanofi Pharmaceutical Report

**Data Requirements:**
- Competitor analysis across multiple companies
- Product categories and mentions
- Media reach and impression data
- Regional breakdown
- Time series data (weekly/monthly)

**Components to Test:**
- Text: Competitor names, time periods
- Table: Competitor comparison matrix
- Chart (Stacked Column): Category breakdown over time
- Chart (Line): Trend analysis
- Summary: Competitive insights

**Expected Results:**
- Multi-competitor data handled correctly
- Stacked charts show proper segmentation
- Line charts display trends accurately
- Summary identifies key competitors

### Scenario 3: SOCAR Energy Sector Report

**Data Requirements:**
- Regional media coverage (multiple regions)
- Energy sector keywords tracking
- Multi-metric analysis (mentions, reach, sentiment)
- Monthly historical data
- Media outlet rankings

**Components to Test:**
- Text: Region names, time periods
- Table: Regional breakdown with multiple metrics
- Chart (Stacked Bar): Regional comparison
- Chart (Column): Historical trends
- Image: Company logo, charts
- Summary: Regional insights

**Expected Results:**
- Regional data properly segmented
- Multi-metric tables formatted correctly
- Stacked bars show regional distribution
- Images placed correctly

## Test Cases

### Test Case 1: Happy Path - Complete Data
**Input:** Excel file with all required columns populated
**Expected:** Report generates successfully with all components

### Test Case 2: Missing Optional Columns
**Input:** Excel file missing non-critical columns
**Expected:** Report generates with warnings, uses defaults

### Test Case 3: Column Name Variations
**Input:** Excel with different column naming (e.g., "Date" vs "date" vs "Tarih")
**Expected:** Column mapping handles case variations or provides clear error

### Test Case 4: Empty Data Rows
**Input:** Excel with blank rows or cells
**Expected:** System skips empty rows, continues processing

### Test Case 5: Special Characters
**Input:** Data with Turkish characters (ş, ğ, ı, ö, ü, ç)
**Expected:** All characters render correctly in PowerPoint

### Test Case 6: Large Dataset
**Input:** Excel with 1000+ rows
**Expected:** Report generates within reasonable time (<30 seconds)

### Test Case 7: Missing Required Column
**Input:** Excel missing critical column (e.g., "date" for time series)
**Expected:** Clear error message identifying missing column

### Test Case 8: Invalid Data Types
**Input:** Text values in numeric columns
**Expected:** Graceful error handling or conversion

### Test Case 9: Date Format Variations
**Input:** Different date formats (DD/MM/YYYY, MM/DD/YYYY, YYYY-MM-DD)
**Expected:** System parses dates correctly or provides clear error

### Test Case 10: Zero/Negative Values
**Input:** Charts with zero or negative values
**Expected:** Charts render correctly with appropriate scales

## Testing Methodology

### Phase 1: Data Validation (Before Report Generation)
1. Load Excel file
2. Validate required columns exist
3. Check data types match expectations
4. Identify any formatting issues
5. Report validation results to user

### Phase 2: Component-by-Component Testing
1. Test each component type individually
2. Use sample data files with known expected outputs
3. Compare generated slides to expected results
4. Document any discrepancies

### Phase 3: End-to-End Testing
1. Generate complete reports for all 3 industries
2. Review generated PowerPoint files manually
3. Verify all slides present and properly formatted
4. Check for any rendering issues

### Phase 4: Edge Case Testing
1. Test boundary conditions (empty data, single row, huge files)
2. Test error scenarios (missing files, corrupted data)
3. Test special characters and localization
4. Test concurrent generation (multiple reports)

## Data Validation Checklist

### Excel File Structure:
- [ ] File exists and is readable
- [ ] Has at least one worksheet
- [ ] Column headers are present (row 1)
- [ ] Data starts at row 2
- [ ] No completely empty columns

### Column Requirements (BSH Template):
Required:
- [ ] date (datetime column)
- [ ] media_outlet (text column)
- [ ] mentions (numeric column)
- [ ] sentiment (categorical: positive/negative/neutral)

Optional:
- [ ] reach (numeric)
- [ ] category (text)

### Column Requirements (Sanofi Template):
Required:
- [ ] date (datetime column)
- [ ] competitor (text column)
- [ ] product (text column)
- [ ] mentions (numeric column)

Optional:
- [ ] category (text)
- [ ] region (text)

### Column Requirements (SOCAR Template):
Required:
- [ ] date (datetime column)
- [ ] region (text column)
- [ ] mentions (numeric column)
- [ ] reach (numeric column)

Optional:
- [ ] sentiment (categorical)
- [ ] media_outlet (text)

## Expected Outputs

### For Each Test:
1. **Success Report:**
   - Report generated successfully
   - File size > 100KB (indicates content rendered)
   - All slides present (BSH: 6, Sanofi: 6, SOCAR: 7)
   - No error messages in console

2. **Validation Report:**
   - List of any data quality issues found
   - Warnings about missing optional columns
   - Suggestions for data improvements

3. **Performance Metrics:**
   - Generation time (target: <10 seconds for normal files)
   - Memory usage
   - File size

## Error Handling Improvements Needed

Based on testing, implement:

1. **Pre-Generation Validation:**
   - Check all required columns exist before starting
   - Validate data types match expectations
   - Provide clear error messages with column names

2. **Column Mapping Helper:**
   - Suggest column mappings based on similarity
   - Allow user to manually map columns
   - Save mapping preferences per template

3. **Data Quality Warnings:**
   - Warn about high percentage of empty values
   - Alert about potential data type mismatches
   - Suggest data cleaning steps

4. **Graceful Degradation:**
   - Generate partial report if some components fail
   - Mark failed components clearly
   - Provide detailed error log

## Success Criteria

Testing is successful if:

1. ✅ All 3 industry templates generate reports with real data
2. ✅ At least 90% of components render correctly
3. ✅ Error messages are clear and actionable
4. ✅ Generation time < 30 seconds for typical files
5. ✅ System handles edge cases without crashing
6. ✅ Turkish characters render correctly
7. ✅ No data corruption or loss
8. ✅ Generated PowerPoints are professional quality

## Testing Tools

### Automated Testing:
```python
# test_real_data.py
import os
from core import PPTGenerator

def test_template(template_path, data_path, output_name):
    """Test template with real data"""
    try:
        generator = PPTGenerator()
        output = generator.generate_from_config(
            template_path=template_path,
            data_path=data_path,
            variables={'month': 'Test', 'year': '2025'}
        )
        print(f"✅ {output_name}: SUCCESS - {output}")
        return True
    except Exception as e:
        print(f"❌ {output_name}: FAILED - {str(e)}")
        return False

# Test all templates
test_template('templates/configs/BSH_Template.json',
              'data/real/BSH_Real_Data.xlsx',
              'BSH')
test_template('templates/configs/Sanofi_Template.json',
              'data/real/Sanofi_Real_Data.xlsx',
              'Sanofi')
test_template('templates/configs/SOCAR_Template.json',
              'data/real/SOCAR_Real_Data.xlsx',
              'SOCAR')
```

### Manual Testing Checklist:
- [ ] Open generated PowerPoint files
- [ ] Check each slide visually
- [ ] Verify data accuracy (compare to Excel)
- [ ] Test editing generated files (ensure no corruption)
- [ ] Print preview (ensure print-ready quality)

## Timeline

**Phase 1 (Day 1):** Create data validation script
**Phase 2 (Day 2):** Test with sample real data
**Phase 3 (Day 3):** Fix identified issues
**Phase 4 (Day 4):** Complete end-to-end testing
**Phase 5 (Day 5):** Documentation and final validation

## Next Steps After Testing

1. Document all issues found
2. Prioritize fixes (critical vs nice-to-have)
3. Implement column mapping validation
4. Add data quality reporting
5. Create user guide with data requirements
6. Update templates with better error handling

---

**Status:** 🔄 Ready to Begin
**Last Updated:** 2025-11-30
**Priority:** HIGH - Critical for production readiness
