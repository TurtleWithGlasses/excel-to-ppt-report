# ReportForge - Clean Project Structure

## Current Project Structure ✅

```
ppt_report_generator/                    # Project root
│
├── 📁 .claude/                          # Claude AI configuration
├── 📁 .qodo/                            # Qodo configuration
├── 📁 .venv/                            # Virtual environment (Python packages)
│
├── 📁 data/                             # Sample data files
│   └── example_data.xlsx
│
├── 📁 docs/                             # 📚 Comprehensive documentation
│   ├── API_REFERENCE.md
│   ├── ARCHITECTURE.md
│   ├── COMPONENT_ARCHITECTURE.md
│   ├── DEVELOPER_GUIDE.md
│   ├── INTERFACE_GUIDE.md
│   ├── NAVIGATION_FLOW.md
│   ├── PROJECT_OVERVIEW.md
│   ├── README.md
│   ├── UI_DESIGN.md
│   └── USER_GUIDE.md
│
├── 📁 Example Files/                    # Example PDF reports (BSH, Sanofi, SOCAR)
│   ├── BSH Ekim Ayı Raporu 25.pdf
│   ├── Sanofi October Monthly Media Coverage Report 25.pdf
│   └── SOCAR Türkiye Aylık Medya Yansıma Raporu Ekim 25.pdf
│
├── 📁 gui/                              # 🖥️ GUI package - User interfaces
│   ├── __init__.py                      # Package initialization
│   ├── main_window.py                   # Main App (Report Generator)
│   └── template_builder.py              # Template Builder interface
│
├── 📁 output/                           # Generated PowerPoint files
│
├── 📁 scripts/                          # Utility scripts
│
├── 📁 templates/                        # Template storage
│   └── configs/                         # Template JSON configurations
│
├── 📄 main.py                           # 🚀 Application entry point
├── 📄 RUN_APP.bat                       # Windows launcher
├── 📄 requirements.txt                  # Python dependencies
│
├── 📄 README.md                         # Main project documentation
├── 📄 QUICKSTART.md                     # Quick start guide
├── 📄 CONTRIBUTING.md                   # Contribution guidelines
├── 📄 DOCUMENTATION_SUMMARY.md          # Documentation index
├── 📄 INTERFACE_IMPLEMENTATION.md       # Interface details
├── 📄 NAVIGATION_UPDATE.md              # Navigation system docs
├── 📄 TEMPLATE_GUIDE.md                 # Template creation guide
└── 📄 RESTRUCTURE_SUMMARY.md            # This reorganization summary

```

## Key Directories

### 📁 gui/ - User Interface Code
Contains both application interfaces built with PyQt6:
- **main_window.py** - Report Generator (4-step workflow)
- **template_builder.py** - Template creation and editing

### 📁 docs/ - Documentation
Complete documentation covering:
- Architecture and design
- User guides
- Developer guides
- API references
- UI/UX specifications

### 📁 data/ - Sample Data
Excel files for testing and examples

### 📁 templates/ - Template Storage
- **configs/** - JSON template configuration files
- Future: BSH_Template.json, Sanofi_Template.json, etc.

### 📁 Example Files/ - Reference Materials
Original PDF reports that inspired the project:
- BSH (Fashion retail)
- Sanofi (Pharmaceutical)
- SOCAR (Energy sector)

## Running the Application

### Method 1: Python Command Line
```bash
# Main App (Report Generator)
python main.py

# Template Builder
python main.py --builder
```

### Method 2: Windows Batch File
```bash
# Double-click or run:
RUN_APP.bat
# Then select: 1 (Main App) or 2 (Template Builder)
```

## Import Structure

Clean Python imports from root:

```python
# GUI imports
from gui.main_window import MainWindow
from gui.template_builder import TemplateBuilder

# Future component imports (when created)
from components.base_component import BaseComponent
from components.table_component import TableComponent
from components.chart_component import ChartComponent

# Future core imports (when created)
from core.ppt_generator import PPTGenerator
from core.template_manager import TemplateManager
from core.data_mapper import DataMapper
```

## File Organization

### Python Code (3 files)
- ✅ `main.py` - Entry point
- ✅ `gui/main_window.py` - Main App UI (428 lines)
- ✅ `gui/template_builder.py` - Template Builder UI (544 lines)

### Documentation (10+ files)
All `.md` files providing comprehensive documentation

### Configuration (2 files)
- ✅ `requirements.txt` - Python package dependencies
- ✅ `RUN_APP.bat` - Windows launcher script

## Dependencies

See `requirements.txt` for complete list:
- **PyQt6** - GUI framework
- **python-pptx** - PowerPoint generation
- **pandas** - Excel data processing
- **matplotlib** - Chart generation
- **openpyxl** - Excel file reading

## Future Structure (To Be Created)

```
ppt_report_generator/
├── components/                  # ⏳ TO CREATE
│   ├── __init__.py
│   ├── base_component.py
│   ├── table_component.py
│   ├── chart_component.py
│   ├── text_component.py
│   ├── image_component.py
│   └── summary_component.py
│
├── core/                        # ⏳ TO CREATE
│   ├── __init__.py
│   ├── ppt_generator.py
│   ├── template_manager.py
│   └── data_mapper.py
│
└── templates/configs/           # ⏳ TO CREATE
    ├── BSH_Template.json
    ├── Sanofi_Template.json
    └── SOCAR_Template.json
```

## Development Workflow

### 1. Setup Environment
```bash
cd ppt_report_generator
pip install -r requirements.txt
```

### 2. Run Application
```bash
python main.py              # Test Main App
python main.py --builder    # Test Template Builder
```

### 3. Add Features
Create new components in `components/` or core logic in `core/`

### 4. Update Documentation
Add/update docs in `docs/` folder

## Advantages of Current Structure

✅ **Clean** - No spaces in folder names
✅ **Standard** - Follows Python package conventions
✅ **Organized** - Logical folder hierarchy
✅ **Scalable** - Easy to add new modules
✅ **Professional** - Industry best practices
✅ **IDE-Friendly** - Works with all major IDEs
✅ **Cross-Platform** - Windows, macOS, Linux compatible

## Navigation

**From Project Root:**
- Main entry: `main.py`
- GUI code: `gui/`
- Documentation: `docs/`
- Templates: `templates/`
- Examples: `Example Files/`

**Quick Access:**
- Start app: `python main.py`
- Read docs: `README.md` → `docs/`
- Install deps: `requirements.txt`
- Windows: `RUN_APP.bat`

---

**Structure Status:** ✅ Clean and Ready for Development

**Last Updated:** November 30, 2024
