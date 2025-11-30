# ReportForge - UI Design Specification

## Overview
ReportForge has **two main interfaces**:
1. **Main App (Report Generator)**: Simple 4-step workflow for end users
2. **Template Builder**: Advanced interface for creating and editing templates

---

## 1. Main App Interface (Report Generator)

### Layout Structure

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ReportForge - Report Generator                                        [_][□][X]│
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐  ┌────────────┐│
│  │   Import Data  │→ │Select Template │→ │ Prepare Report │→ │  Download  ││
│  │                │  │                │  │                │  │   Report   ││
│  └────────────────┘  └────────────────┘  └────────────────┘  └────────────┘│
│   Users will import    Users will select   The report will be  Report will be│
│   excel files         template            prepared by excel   downloaded on │
│                                           importation         local file    │
│                                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  Report name: [________________________________]                             │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        Slide ... of ...                              │   │
│  │                                                                       │   │
│  │                                                                       │   │
│  │                                                                       │   │
│  │        After the report is prepared,                                 │   │
│  │        the slides will be shown here                                 │   │
│  │        page by page. The user will be                                │   │
│  │        able to edit the pages too.                                   │   │
│  │                                                                       │   │
│  │                                                                       │   │
│  │                                                                       │   │
│  │                                                                       │   │
│  │                                                                       │   │
│  │                                                                       │   │
│  │                                                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                               │
│  [◄ Previous]  [Edit Slide]  [Delete Slide]  [Add Slide]  [Next ►]         │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Component Details

#### Top Progress Bar (4 Steps)
- **Step 1: Import Data**
  - Button opens file dialog
  - Accepts: `.xlsx`, `.xls`, `.csv`
  - Shows uploaded file name below button
  - Status indicator: ✓ (green) when complete

- **Step 2: Select Template**
  - Dropdown menu with template list
  - Templates grouped by industry:
    - Fashion & Retail (BSH, LC Waikiki)
    - Pharmaceutical (Sanofi)
    - Energy (SOCAR)
    - Financial, Sales, Custom
  - Shows template preview thumbnail
  - "Create New Template" button links to Template Builder
  - Status indicator: ✓ (green) when selected

- **Step 3: Prepare Report**
  - Button to generate report
  - Progress bar during generation
  - Shows: "Generating slides... 15/55 complete"
  - Status indicator: ✓ (green) when complete

- **Step 4: Download Report**
  - Button to download .pptx file
  - File name auto-generated: `{ReportName}_{Date}.pptx`
  - Option to choose save location
  - Status indicator: ✓ (green) when downloaded

#### Report Name Field
- Text input for custom report name
- Default: `Report_{Date}`
- Max 100 characters
- Validates: No special characters except `_` and `-`

#### Slide Preview Area
- **Before Generation**: Shows placeholder message
- **After Generation**:
  - Large preview of current slide
  - Slide counter: "Slide 5 of 55"
  - Editable: Click elements to modify (text, colors, position)
  - Zoom controls: 50%, 75%, 100%, 125%, 150%

#### Bottom Control Buttons
- **◄ Previous**: Navigate to previous slide (disabled on slide 1)
- **Edit Slide**: Opens inline editor for current slide
  - Edit text boxes
  - Adjust chart colors
  - Reposition elements
- **Delete Slide**: Remove current slide (with confirmation)
- **Add Slide**: Insert new blank/templated slide after current
- **Next ►**: Navigate to next slide (disabled on last slide)

### Color Scheme
- **Primary**: `#2563EB` (Blue) - Buttons, active steps
- **Secondary**: `#10B981` (Green) - Success indicators, ✓ marks
- **Background**: `#F9FAFB` (Light gray)
- **Text**: `#111827` (Dark gray)
- **Borders**: `#E5E7EB` (Medium gray)
- **Hover**: `#1D4ED8` (Darker blue)

### Fonts
- **Headers**: `Segoe UI Bold`, 16pt
- **Body**: `Segoe UI`, 11pt
- **Buttons**: `Segoe UI Semibold`, 12pt

---

## 2. Template Builder Interface

### Layout Structure

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ReportForge - Template Builder                                       [_][□][X]│
├──────────────────────┬──────────────────────────────────────────────────────┤
│  TEMPLATE SETTINGS   │  SLIDE PREVIEW                                       │
│                      │                                                      │
│ Template Name:       │  ┌────────────────────────────────────────────┐    │
│ [______________]     │  │                                            │    │
│                      │  │         [LOGO]                             │    │
│ Industry:            │  │                                            │    │
│ [▼ Select Industry]  │  │    Report Title Here                       │    │
│                      │  │    Subtitle / Date                         │    │
│ Logo:                │  │                                            │    │
│ [Browse...] logo.png │  │                                            │    │
│                      │  │                                            │    │
│ Brand Colors:        │  │                                            │    │
│ Primary:   [■]#2563EB│  │                                            │    │
│ Secondary: [■]#10B981│  │                                            │    │
│ Accent:    [■]#F59E0B│  └────────────────────────────────────────────┘    │
│                      │  Slide 1 of 8                                       │
│ Font Family:         │  [◄ Previous] [▶ Next]                              │
│ [▼ Segoe UI]         │                                                      │
│                      ├──────────────────────────────────────────────────────┤
│ ──────────────────── │  COMPONENTS LIBRARY                                  │
│                      │                                                      │
│ SLIDE STRUCTURE      │  Drag components to add to slide:                   │
│                      │                                                      │
│ Slides:              │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐    │
│ ☑ 1. Cover           │  │Table │ │Chart │ │ Text │ │Image │ │Summary│    │
│ ☑ 2. Table of Content│  │  📊  │ │  📈  │ │  📝  │ │  🖼️  │ │  💡   │    │
│ ☑ 3. Executive Summary│ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘    │
│ ☑ 4. Data Table      │                                                      │
│ ☑ 5. Chart - Column  │  ──────────────────────────────────────────────     │
│ ☑ 6. Chart - Pie     │  SELECTED COMPONENT: Table Component                │
│ ☑ 7. Trends          │                                                      │
│ ☑ 8. Summary         │  Component Type: Table                              │
│                      │                                                      │
│ [+ Add Slide]        │  Data Source:                                       │
│ [- Remove Slide]     │  [▼ Sheet1]  Column: [▼ Company Name]              │
│ [↑] [↓] Reorder      │                                                      │
│                      │  Table Style:                                       │
│ ──────────────────── │  ☐ Header Row    ☑ Zebra Striping                  │
│                      │  ☑ Border        ☐ Grid Lines                       │
│ [Save Template]      │                                                      │
│ [Load Template]      │  Position:  X: [50]  Y: [100]                       │
│ [Export as JSON]     │  Size:      W: [600] H: [300]                       │
│                      │                                                      │
│                      │  Font Size: [11] pt                                 │
│                      │  Header Color: [■] #2563EB                          │
│                      │  Row Color:    [■] #FFFFFF                          │
│                      │                                                      │
│                      │  [Apply Changes]  [Remove Component]                │
└──────────────────────┴──────────────────────────────────────────────────────┘
```

### Component Details

#### Left Panel: Template Settings

**Template Info Section**
- **Template Name**: Text input (e.g., "BSH Monthly Media Report")
- **Industry Dropdown**:
  - Fashion & Retail
  - Pharmaceutical
  - Energy & Utilities
  - Banking & Finance
  - Technology
  - FMCG
  - Custom / Other
- **Logo Upload**:
  - Browse button → file dialog
  - Preview thumbnail (100x100px)
  - Supports: `.png`, `.jpg`, `.svg`
  - Position on slides: Top-left, Top-right, Bottom-left, Bottom-right

**Brand Colors**
- **Primary Color**: Color picker → used for headers, titles
- **Secondary Color**: Color picker → used for accents, highlights
- **Accent Color**: Color picker → used for charts, callouts
- **Preview**: Live preview on slide shows color changes

**Typography**
- **Font Family Dropdown**:
  - Segoe UI (default)
  - Calibri
  - Arial
  - Times New Roman
  - Custom (upload .ttf file)
- **Header Size**: 18-32pt slider
- **Body Size**: 10-16pt slider

**Slide Structure Section**
- **Slide List**:
  - Checkbox list of all slides in template
  - Each slide shows:
    - Number (1, 2, 3...)
    - Name (Cover, Executive Summary, etc.)
    - Type icon (📄 text, 📊 table, 📈 chart)
  - Drag-and-drop to reorder
  - Click to preview in center panel

- **Slide Management Buttons**:
  - **+ Add Slide**: Opens "New Slide" dialog
  - **- Remove Slide**: Delete selected slide (with confirmation)
  - **↑ ↓ Reorder**: Move slide up/down in sequence

**Action Buttons**
- **Save Template**:
  - Saves as `.json` in `templates/configs/`
  - Auto-names: `{TemplateName}_{Date}.json`
- **Load Template**:
  - Opens file dialog
  - Loads existing `.json` template for editing
- **Export as JSON**:
  - Downloads template config
  - Shareable with other users

#### Center Panel: Slide Preview

**Preview Canvas**
- **Live Preview**: Shows current slide with all components
- **Interactive**:
  - Click components to select
  - Drag to reposition
  - Resize handles on selection
  - Grid lines (show on hover)
  - Snap-to-grid (10px increments)

**Navigation**
- **Slide Counter**: "Slide 3 of 8"
- **Previous/Next Buttons**: Navigate through slides
- **Zoom**: 50%, 75%, 100%, 125%, 150%

#### Right Panel: Components Library

**Component Palette**
- **Drag-and-Drop Components**:

  1. **📊 Table Component**
     - Icon: Table grid
     - Hover tooltip: "Data table for structured information"

  2. **📈 Chart Component**
     - Icon: Bar chart
     - Hover tooltip: "Visualizations (bar, column, pie, line)"

  3. **📝 Text Component**
     - Icon: Text lines
     - Hover tooltip: "Titles, headings, paragraphs"

  4. **🖼️ Image Component**
     - Icon: Picture frame
     - Hover tooltip: "Logos, photos, graphics"

  5. **💡 Summary Component**
     - Icon: Lightbulb
     - Hover tooltip: "Auto-generated insights from data"

**Component Configuration Panel**
(Shown when component is selected)

**For Table Component:**
- **Data Source**:
  - Sheet Dropdown: Select Excel sheet
  - Column Mapping: Map Excel columns to table columns
    - Source Column: `[▼ Kurum]` → Display Name: `[Company]`
  - Row Filter: Include/exclude rows based on criteria
  - Sort: Choose column, ascending/descending

- **Table Style**:
  - ☑ Header Row (bold, colored background)
  - ☑ Zebra Striping (alternating row colors)
  - ☑ Border (table outline)
  - ☐ Grid Lines (internal cell borders)

- **Formatting**:
  - Font Size: 8-16pt slider
  - Header Background: Color picker
  - Header Text Color: Color picker
  - Row Background (Odd): Color picker
  - Row Background (Even): Color picker
  - Text Alignment: Left, Center, Right

- **Position & Size**:
  - X Position: 0-720 (slide width in points)
  - Y Position: 0-540 (slide height in points)
  - Width: 100-720
  - Height: 100-540

**For Chart Component:**
- **Chart Type Dropdown**:
  - Column Chart (vertical bars)
  - Bar Chart (horizontal bars)
  - Pie Chart
  - Line Chart
  - Stacked Column Chart
  - Stacked Bar Chart

- **Data Source**:
  - Sheet: `[▼ Sheet1]`
  - X-Axis Data: `[▼ Month]` (categories)
  - Y-Axis Data: `[▼ Sales]` (values)
  - Series: `[▼ Company]` (for multi-series charts)

- **Chart Style**:
  - Color Scheme:
    - Brand Colors (uses template colors)
    - Custom (color picker for each series)
  - Legend Position: Top, Bottom, Left, Right, None
  - Show Data Labels: ☐ Yes
  - Grid Lines: ☑ Horizontal, ☐ Vertical

- **Axes**:
  - X-Axis Title: `[Categories]`
  - Y-Axis Title: `[Values]`
  - Y-Axis Range: Auto / Manual (min/max)

- **Position & Size**: Same as Table

**For Text Component:**
- **Content**:
  - Text Input: Multi-line text box
  - Placeholder Variables: `{date}`, `{reportName}`, `{company}`
  - Dynamic Text: Pull from Excel cell reference

- **Formatting**:
  - Font Family: `[▼ Segoe UI]`
  - Font Size: 8-48pt
  - Font Style: ☐ Bold, ☐ Italic, ☐ Underline
  - Color: Color picker
  - Alignment: Left, Center, Right, Justify

- **Position & Size**: Same as Table

**For Image Component:**
- **Image Source**:
  - Upload File: Browse button
  - Use Logo: Checkbox (uses template logo)
  - URL: Input for web images

- **Styling**:
  - Border: Width (0-5px), Color
  - Corner Radius: 0-20px (rounded corners)
  - Opacity: 0-100%

- **Position & Size**: Same as Table

**For Summary Component:**
- **Auto-Insights Type**:
  - ☑ Key Metrics (top 3 numbers from data)
  - ☑ Trends (increase/decrease vs previous period)
  - ☑ Highlights (highest/lowest values)
  - ☐ AI-Generated (requires API key)

- **Data Source**:
  - Sheet: `[▼ Sheet1]`
  - Metric Columns: Multi-select columns to analyze

- **Layout**:
  - Style: Bullet points, Numbered list, Callout boxes
  - Max Items: 3-10

- **Formatting**: Same as Text Component

**Action Buttons**
- **Apply Changes**: Save component configuration
- **Remove Component**: Delete from slide
- **Duplicate Component**: Create copy on same slide

---

## 3. New Slide Dialog

When user clicks **[+ Add Slide]** in Template Builder:

```
┌───────────────────────────────────────┐
│  Add New Slide                   [X]  │
├───────────────────────────────────────┤
│                                       │
│  Slide Type:                          │
│  ○ Blank Slide                        │
│  ○ Title Slide                        │
│  ○ Table Slide                        │
│  ○ Chart Slide                        │
│  ○ Mixed Content (Table + Chart)      │
│  ○ Summary/Insights Slide             │
│                                       │
│  Slide Name:                          │
│  [_______________________________]    │
│                                       │
│  Insert After:                        │
│  [▼ Slide 3: Executive Summary]       │
│                                       │
│  [Cancel]              [Add Slide]    │
└───────────────────────────────────────┘
```

---

## 4. Excel Column Mapping Dialog

When template needs to map Excel columns to components:

```
┌─────────────────────────────────────────────────────┐
│  Map Excel Columns                             [X]  │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Excel Sheet: [▼ Sheet1 - Media Analysis]          │
│                                                     │
│  Component: Executive Summary Table                │
│                                                     │
│  Column Mappings:                                  │
│  ┌──────────────────┬──────────────────────────┐  │
│  │ Excel Column     │ Display As               │  │
│  ├──────────────────┼──────────────────────────┤  │
│  │ [▼ Kurum]        │ [Company Name        ]   │  │
│  │ [▼ Toplam]       │ [Total Mentions      ]   │  │
│  │ [▼ Olumlu]       │ [Positive            ]   │  │
│  │ [▼ Olumsuz]      │ [Negative            ]   │  │
│  │ [▼ Nötr]         │ [Neutral             ]   │  │
│  │ [▼ SoV]          │ [Share of Voice %    ]   │  │
│  └──────────────────┴──────────────────────────┘  │
│                                                     │
│  Preview:                                          │
│  ┌──────────────────────────────────────────────┐ │
│  │ Company Name  │ Total │ Positive │ Negative  │ │
│  ├───────────────┼───────┼──────────┼───────────┤ │
│  │ BSH           │ 1,234 │ 856      │ 234       │ │
│  │ Arçelik       │ 987   │ 654      │ 187       │ │
│  └──────────────────────────────────────────────┘ │
│                                                     │
│  [Cancel]           [Save Mapping]                 │
└─────────────────────────────────────────────────────┘
```

---

## 5. User Workflows

### Workflow 1: Generate Report (End User)

1. **Launch Main App**
2. **Step 1**: Click "Import Data" → Select Excel file
3. **Step 2**: Click "Select Template" → Choose from dropdown (e.g., "BSH Monthly Media Report")
4. **Step 3**: Enter report name → Click "Prepare Report"
   - Progress bar shows generation (15/55 slides...)
5. **Step 4**: Review slides in preview area
   - Use ◄ ► to navigate
   - Click "Edit Slide" to make changes
   - Delete or add slides as needed
6. **Step 5**: Click "Download Report" → Choose save location → Done!

**Time**: 3-5 minutes for 55-page report

---

### Workflow 2: Create Template (Power User)

1. **Launch Template Builder**
2. **Template Settings** (Left Panel):
   - Enter template name: "Sanofi Pharma Media Report"
   - Select industry: "Pharmaceutical"
   - Upload logo: `sanofi_logo.png`
   - Set brand colors: Primary #003DA5, Secondary #FF6600
   - Choose font: Segoe UI
3. **Add Slides**:
   - Click "+ Add Slide" 8 times for 8-slide template
   - Name each: Cover, TOC, Executive Summary, Trends, etc.
4. **Configure Slide 1 (Cover)**:
   - Drag **Image Component** → Add logo (top-right)
   - Drag **Text Component** → Add title "Monthly Media Report"
   - Drag **Text Component** → Add date `{date}`
5. **Configure Slide 3 (Executive Summary)**:
   - Drag **Table Component** → Drop on canvas
   - Set data source: Sheet1
   - Map columns: Kurum→Company, Toplam→Total, etc.
   - Style: Header row ✓, Zebra striping ✓
   - Position: X=50, Y=100, W=600, H=300
6. **Configure Slide 5 (Trends Chart)**:
   - Drag **Chart Component** → Drop on canvas
   - Chart type: Line Chart
   - X-Axis: Month, Y-Axis: Total Mentions
   - Series: Company
   - Style: Brand colors, Legend at bottom
7. **Repeat** for all slides
8. **Save Template**: Click "Save Template" → `Sanofi_Pharma_Template.json`
9. **Test**: Go to Main App → Select template → Generate report

**Time**: 30-60 minutes for initial template creation
**Reuse**: Forever! Use monthly with new data in 5 minutes

---

## 6. Technical Implementation Notes

### PyQt6 Widgets to Use

**Main App:**
- `QMainWindow` - Main container
- `QHBoxLayout` - Progress steps (4 buttons)
- `QLineEdit` - Report name field
- `QGraphicsView` + `QGraphicsScene` - Slide preview area
- `QPushButton` - All buttons (Previous, Next, Edit, etc.)
- `QFileDialog` - File picker for Excel import
- `QComboBox` - Template dropdown

**Template Builder:**
- `QMainWindow` - Main container
- `QSplitter` - 3-panel layout (left settings, center preview, right components)
- `QListWidget` - Slide list (drag-drop enabled)
- `QGraphicsView` + `QGraphicsScene` - Slide preview canvas
- `QDockWidget` - Component palette (can be floating)
- `QFormLayout` - Settings forms (colors, fonts, etc.)
- `QColorDialog` - Color pickers
- `QSpinBox` - Position/size numeric inputs
- `QCheckBox` - Style options (borders, grid, etc.)

**Drag-and-Drop:**
- Enable `setAcceptDrops(True)` on preview canvas
- `QDrag` + `QMimeData` for component dragging
- Custom `QGraphicsItem` subclasses for components

**File Operations:**
- `json` module for template save/load
- `python-pptx` for PPT generation
- `pandas` for Excel reading

---

## 7. Responsive Design

### Window Sizes
- **Minimum**: 1024x768
- **Recommended**: 1366x768 or larger
- **Maximum**: Scales to 4K (3840x2160)

### Layout Adaptations
- **< 1200px width**: Template Builder switches to tabbed interface (Settings | Preview | Components)
- **< 1024px width**: Show warning "Please use larger screen for Template Builder"

---

## 8. Accessibility

- **Keyboard Navigation**: Tab through all controls
- **Screen Reader**: ARIA labels on all buttons and inputs
- **Color Contrast**: WCAG AA compliant (4.5:1 minimum)
- **Font Scaling**: Respect OS font size settings

---

## Next Steps

1. ✅ **Design Complete** (this document)
2. ⏳ **Implementation Phase 1**: Main App Interface
   - Create PyQt6 window structure
   - Implement 4-step workflow
   - Add slide preview area
3. ⏳ **Implementation Phase 2**: Template Builder Interface
   - Create 3-panel layout
   - Implement component palette
   - Add drag-drop functionality
4. ⏳ **Implementation Phase 3**: Integration
   - Connect Main App to Template Builder
   - Test with real Excel files (BSH, Sanofi, SOCAR)
   - Generate actual PPT files

---

**This design supports the universal, multi-industry vision of ReportForge!**
