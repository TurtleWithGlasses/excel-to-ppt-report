# ReportForge - Quick Start Guide

## Installation

1. **Install Python 3.8+** (if not already installed)
   - Download from: https://www.python.org/downloads/

2. **Navigate to Project Directory**
   ```bash
   cd c:/Users/mhmts/PycharmProjects/ppt_report_generator
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Option 1: Using the Batch File (Windows)
Double-click `RUN_APP.bat` and select:
- Option 1: Launch Main App (Report Generator)
- Option 2: Launch Template Builder

### Option 2: Using Command Line

**Main App (Report Generator):**
```bash
python main.py
```

**Template Builder:**
```bash
python main.py --builder
```

## Usage Guide

### Main App - Generate Reports

1. **Step 1: Import Data**
   - Click "Import Data" button
   - Select your Excel file (.xlsx or .xls)
   - ✓ marks the step as complete

2. **Step 2: Select Template**
   - Click "Select Template" button
   - Choose from available templates:
     - BSH Monthly Media Report
     - Sanofi Pharma Media Report
     - SOCAR Energy Sector Template
     - And more...
   - ✓ marks the step as complete

3. **Step 3: Prepare Report**
   - Enter report name (default: Report_YYYYMMDD)
   - Click "Prepare Report" button
   - Watch progress bar as slides are generated
   - Preview slides in the preview area

4. **Step 4: Download Report**
   - Review slides using Previous/Next buttons
   - Edit slides if needed
   - Click "Download Report" button
   - Choose save location
   - Done! Your .pptx file is ready

### Template Builder - Create Custom Templates

1. **Template Settings (Left Panel)**
   - Enter template name (e.g., "BSH Monthly Media Report")
   - Select industry
   - Upload logo (optional)
   - Choose brand colors (Primary, Secondary, Accent)
   - Select font family

2. **Add Slides**
   - Click "+ Add Slide" button
   - Choose slide type:
     - Blank Slide
     - Title Slide
     - Table Slide
     - Chart Slide
     - Mixed Content
     - Summary/Insights Slide
   - Enter slide name

3. **Add Components to Slides**
   - Select a slide from the list
   - Drag components from the Components Library (right panel):
     - 📊 Table Component
     - 📈 Chart Component
     - 📝 Text Component
     - 🖼️ Image Component
     - 💡 Summary Component
   - Configure each component (data source, styling, position)

4. **Save Template**
   - Click "Save Template" button
   - Choose save location
   - Template saved as JSON file

5. **Load Template**
   - Click "Load Template" button
   - Select existing .json template
   - Edit and save

## Example Workflows

### Example 1: BSH Monthly Media Report

```
1. Open Main App
2. Import: "BSH_November_2025.xlsx"
3. Select Template: "BSH Monthly Media Report"
4. Prepare Report
5. Download: "BSH_November_Report.pptx"
Total Time: 5 minutes
```

### Example 2: Create Sanofi Template

```
1. Open Template Builder
2. Template Name: "Sanofi Pharma Media Report"
3. Industry: Pharmaceutical
4. Add logo: sanofi_logo.png
5. Colors: Primary #003DA5, Secondary #FF6600
6. Add 8 slides:
   - Cover
   - Table of Contents
   - Executive Summary (Table Component)
   - Trend Analysis (Chart Component)
   - Tone Analysis (Chart Component)
   - Top Publications (Table Component)
   - Online Coverage (Mixed Content)
   - Summary (Summary Component)
7. Save Template: "Sanofi_Pharma_Template.json"
Total Time: 30-60 minutes (one-time setup)
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'PyQt6'"
**Solution:** Install dependencies:
```bash
pip install -r ../requirements.txt
```

### Issue: "No module named 'gui'"
**Solution:** Make sure you're running from the correct directory:
```bash
cd "PPT Report Generator"
python main.py
```

### Issue: Template not showing in Main App
**Solution:** Templates must be saved in `templates/configs/` directory

## Next Steps

1. ✅ Test both interfaces
2. ✅ Create your first template in Template Builder
3. ✅ Generate your first report in Main App
4. 📚 Read full documentation in `/docs` folder
5. 🎨 Customize templates for your brand

## Support

- **Documentation**: See `/docs` folder
- **Example Files**: See `/Example Files` folder
- **Issues**: GitHub Issues (if open source)

---

**Built with ❤️ to automate repetitive tasks across every industry!**
