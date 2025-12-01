# ReportForge - Interface Guide

## Overview

ReportForge has **two main interfaces** designed for different user needs:

1. **Main App (Report Generator)** - For end users generating reports
2. **Template Builder** - For power users creating custom templates

---

## Main App Interface (Report Generator)

### Purpose
Simple, 4-step workflow for generating PowerPoint reports from Excel data.

### Target Users
- Marketing professionals
- PR agencies
- Business analysts
- Anyone who needs to generate recurring reports

### Interface Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  ReportForge - Report Generator                          [_][□][X]│
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ Import   │→ │ Select   │→ │ Prepare  │→ │ Download │       │
│  │ Data     │  │ Template │  │ Report   │  │ Report   │       │
│  │    1     │  │    2     │  │    3     │  │    4     │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
│                                                                   │
│  ──────────────────────────────────────────────────────────────  │
│                                                                   │
│  Report name: [Report_20251129                        ]          │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Slide ... of ...                       │  │
│  │                                                           │  │
│  │                  [SLIDE PREVIEW AREA]                     │  │
│  │                                                           │  │
│  │         After the report is prepared,                     │  │
│  │         the slides will be shown here                     │  │
│  │         page by page.                                     │  │
│  │                                                           │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                   │
│  [◄ Previous] [Edit Slide] [Delete] [Add Slide] [Next ►]        │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Key Features

**4-Step Progress Bar:**
- Each step is a button that changes color when clicked
- Green ✓ indicates completed steps
- Blue indicates active step
- Gray indicates pending steps
- Visual arrows (→) show workflow direction

**Step 1: Import Data**
- Opens file dialog
- Accepts .xlsx and .xls files
- Shows uploaded filename
- Marks step complete with green ✓

**Step 2: Select Template**
- Dropdown with categorized templates:
  - Fashion & Retail (BSH, LC Waikiki)
  - Pharmaceutical (Sanofi)
  - Energy (SOCAR)
  - Financial, Custom
- "Create New Template" option launches Template Builder
- Shows selected template name

**Step 3: Prepare Report**
- Input field for custom report name
- Generate button starts report creation
- Progress bar shows generation status
- Slide counter updates as slides are created
- Preview area shows generated slides

**Step 4: Download Report**
- Save dialog for choosing location
- Default filename: {ReportName}_{Date}.pptx
- Confirmation message on success

**Slide Preview Area:**
- Large canvas showing current slide
- Slide counter: "Slide 5 of 55"
- Real-time rendering of slide content
- Editable elements (click to modify)

**Slide Controls:**
- **◄ Previous**: Navigate backward (disabled on first slide)
- **Edit Slide**: Inline editor for text, colors, positions
- **Delete Slide**: Remove current slide (with confirmation)
- **Add Slide**: Insert new slide after current
- **Next ►**: Navigate forward (disabled on last slide)

### Color Scheme
- **Primary Blue**: `#2563EB` - Active buttons, step indicators
- **Success Green**: `#10B981` - Completed steps, success messages
- **Danger Red**: `#EF4444` - Delete button, warnings
- **Background**: `#F9FAFB` - Soft gray background
- **White**: Slide preview area, input fields

---

## Template Builder Interface

### Purpose
Advanced interface for creating reusable report templates with custom components.

### Target Users
- Template designers
- Power users
- Agency managers
- Developers

### Interface Layout

```
┌───────────────────────────────────────────────────────────────────┐
│  ReportForge - Template Builder                           [_][□][X]│
├────────────┬───────────────────────────┬──────────────────────────┤
│ LEFT PANEL │     CENTER PANEL          │      RIGHT PANEL         │
│            │                           │                          │
│ TEMPLATE   │   SLIDE PREVIEW           │  COMPONENTS LIBRARY      │
│ SETTINGS   │                           │                          │
│            │  ┌─────────────────────┐  │  ┌──┐┌──┐┌──┐┌──┐┌──┐  │
│ Name:      │  │                     │  │  │📊││📈││📝││🖼️││💡│  │
│ [______]   │  │   [LOGO]            │  │  └──┘└──┘└──┘└──┘└──┘  │
│            │  │                     │  │  Table Chart Text ...   │
│ Industry:  │  │  Report Title       │  │                          │
│ [v Fashion]│  │  Subtitle           │  │  ──────────────────────  │
│            │  │                     │  │  SELECTED COMPONENT:     │
│ Logo:      │  │                     │  │                          │
│ [Browse..] │  │                     │  │  Component Type: Table   │
│            │  │                     │  │                          │
│ Colors:    │  └─────────────────────┘  │  Data Source:            │
│ Primary:■  │  Slide 1 of 8             │  [v Sheet1]              │
│ Secondary:■│  [◄ Previous] [Next ►]    │                          │
│ Accent: ■  │                           │  Table Style:            │
│            │                           │  ☑ Header Row            │
│ Font:      │                           │  ☑ Zebra Striping        │
│ [v Segoe]  │                           │                          │
│            │                           │  Position:               │
│ ────────── │                           │  X: [50]  Y: [100]       │
│            │                           │  Size:                   │
│ SLIDES:    │                           │  W: [600] H: [300]       │
│ ☑ 1. Cover │                           │                          │
│ ☑ 2. TOC   │                           │  [Apply] [Remove]        │
│ ☑ 3. Table │                           │                          │
│            │                           │                          │
│ [+ Add]    │                           │                          │
│ [- Remove] │                           │                          │
│ [↑] [↓]    │                           │                          │
│            │                           │                          │
│ ────────── │                           │                          │
│            │                           │                          │
│ [Save]     │                           │                          │
│ [Load]     │                           │                          │
│ [Export]   │                           │                          │
└────────────┴───────────────────────────┴──────────────────────────┘
```

### Left Panel: Template Settings

**Template Info:**
- Template Name input
- Industry dropdown (Fashion, Pharma, Energy, Finance, etc.)
- Logo upload button with preview

**Brand Colors:**
- Primary Color picker (headers, titles)
- Secondary Color picker (accents)
- Accent Color picker (charts, callouts)
- Live preview updates on slide

**Typography:**
- Font family dropdown (Segoe UI, Calibri, Arial, etc.)
- Header size slider
- Body size slider

**Slide Structure:**
- Checkbox list of all slides
- Drag-and-drop reordering
- Add/Remove slide buttons
- Up/Down arrows for reordering

**Action Buttons:**
- **Save Template**: Save as .json file
- **Load Template**: Open existing template
- **Export as JSON**: Share with others

### Center Panel: Slide Preview

**Preview Canvas:**
- 720x540 PowerPoint slide dimensions
- Live rendering of components
- Interactive elements (click to select)
- Grid lines for alignment
- Snap-to-grid (10px)

**Navigation:**
- Slide counter: "Slide 3 of 8"
- Previous/Next buttons
- Zoom controls (50%, 75%, 100%, 125%, 150%)

**Drag-and-Drop:**
- Drag components from right panel
- Drop onto canvas
- Resize with handles
- Reposition with mouse

### Right Panel: Components Library

**Component Palette:**
5 draggable component types:

1. **📊 Table Component**
   - Data tables
   - Executive summaries
   - KPI matrices

2. **📈 Chart Component**
   - Column, Bar, Pie, Line charts
   - Stacked charts
   - Trend analysis

3. **📝 Text Component**
   - Titles, headers
   - Paragraphs
   - Dynamic text variables

4. **🖼️ Image Component**
   - Logos
   - Photos
   - Graphics

5. **💡 Summary Component**
   - Auto-generated insights
   - Key metrics
   - Highlights

**Component Configuration:**
When a component is selected on the canvas, this panel shows:

**For Table Component:**
- Data Source (sheet, columns)
- Column mapping (Excel → Display)
- Table style (header, borders, zebra)
- Formatting (fonts, colors, alignment)
- Position (X, Y)
- Size (Width, Height)

**For Chart Component:**
- Chart type (Column, Bar, Pie, Line, Stacked)
- Data source (X-axis, Y-axis, Series)
- Color scheme (brand colors or custom)
- Legend position
- Axes labels
- Position & size

**For Text Component:**
- Content (text input)
- Placeholder variables ({date}, {company})
- Font (family, size, style, color)
- Alignment (left, center, right)
- Position & size

**For Image Component:**
- Image source (file upload or URL)
- Border (width, color)
- Corner radius
- Opacity
- Position & size

**For Summary Component:**
- Auto-insights type (metrics, trends, highlights)
- Data source (columns to analyze)
- Layout (bullets, numbered, callout)
- Max items to show
- Position & size

---

## Workflow Comparison

### End User (Main App)
```
Upload Excel → Choose Template → Generate → Download PPT
Time: 3-5 minutes
```

### Power User (Template Builder)
```
Design Template → Add Slides → Add Components → Configure → Save
Time: 30-60 minutes (one-time)

Then use in Main App:
Upload Excel → Choose Custom Template → Generate → Download PPT
Time: 3-5 minutes (every time)
```

---

## Keyboard Shortcuts

### Main App
- `Ctrl + O`: Import Excel file
- `Ctrl + G`: Generate report
- `Ctrl + S`: Download report
- `Left Arrow`: Previous slide
- `Right Arrow`: Next slide
- `Delete`: Delete current slide
- `Insert`: Add new slide

### Template Builder
- `Ctrl + N`: New template
- `Ctrl + S`: Save template
- `Ctrl + O`: Load template
- `Ctrl + A`: Add slide
- `Delete`: Remove selected slide
- `Ctrl + Up`: Move slide up
- `Ctrl + Down`: Move slide down

---

## Tips & Tricks

### Main App
1. **Batch Processing**: Keep the app open and process multiple files sequentially
2. **Template Switching**: Change templates mid-workflow to compare outputs
3. **Slide Editing**: Edit slides before downloading for quick customizations
4. **Report Naming**: Use descriptive names like "BSH_November_2025_Final"

### Template Builder
1. **Start Simple**: Begin with 3-4 slides, add more later
2. **Component Reuse**: Copy-paste component configs across slides
3. **Color Consistency**: Use brand color picker for all components
4. **Save Often**: Save template after each major change
5. **Test Early**: Generate a test report in Main App to verify template

---

## Next Steps

1. ✅ Run Main App: `python main.py`
2. ✅ Import sample Excel file
3. ✅ Select a template
4. ✅ Generate your first report
5. ✅ Run Template Builder: `python main.py --builder`
6. ✅ Create your first custom template
7. ✅ Use custom template in Main App

---

**Interfaces built with PyQt6 for cross-platform compatibility!**
