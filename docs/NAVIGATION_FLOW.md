# ReportForge - Navigation Flow

## Complete User Journey

```
┌──────────────────────────────────────────────────────────────────┐
│                         MAIN APP                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  📊 ReportForge - Report Generator  [🛠️ Create/Edit Templates]│  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │  Import  │→ │  Select  │→ │ Prepare  │→ │ Download │        │
│  │  Data    │  │ Template │  │  Report  │  │  Report  │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
│                      │                                            │
│                      │ Choose "Create New Template..."           │
│                      ↓                                            │
└──────────────────────┼───────────────────────────────────────────┘
                       │
                       │ Click "🛠️ Create/Edit Templates" button
                       │          OR
                       │ Select "Create New Template..." option
                       ↓
┌──────────────────────────────────────────────────────────────────┐
│                    TEMPLATE BUILDER                               │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  🛠️ ReportForge - Template Builder     [← Back to Main App] │  │
│  └────────────────────────────────────────────────────────────┘  │
│  ┌──────────┬──────────────────────────┬─────────────────────┐  │
│  │SETTINGS  │    SLIDE PREVIEW         │  COMPONENTS         │  │
│  │          │                          │                     │  │
│  │ Name:    │  ┌────────────────────┐  │  ┌──┐┌──┐┌──┐     │  │
│  │ Industry │  │  [Your Template]   │  │  │📊││📈││📝│     │  │
│  │ Colors   │  │                    │  │  └──┘└──┘└──┘     │  │
│  │ Logo     │  └────────────────────┘  │                     │  │
│  │          │                          │  Component Config   │  │
│  │ Slides:  │  [◄ Prev] [Next ►]      │                     │  │
│  │ ☑ Slide1 │                          │  [Apply] [Remove]   │  │
│  │ ☑ Slide2 │                          │                     │  │
│  │ [+] [-]  │                          │                     │  │
│  │          │                          │                     │  │
│  │ [Save]   │                          │                     │  │
│  │ [Load]   │                          │                     │  │
│  └──────────┴──────────────────────────┴─────────────────────┘  │
│                                                                   │
│                Click "← Back to Main App" or close window        │
│                              ↓                                    │
└──────────────────────────────┼───────────────────────────────────┘
                               │
                               │ (Unsaved changes check)
                               ↓
                       ┌───────────────┐
                       │ Save Changes? │
                       │ [Save]        │
                       │ [Discard]     │
                       │ [Cancel]      │
                       └───────┬───────┘
                               │
                               ↓
┌──────────────────────────────────────────────────────────────────┐
│                    BACK TO MAIN APP                               │
│                                                                   │
│  Template list refreshed (if new template was saved)             │
│  Continue with report generation workflow                        │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## Navigation Entry Points

### From Main App to Template Builder

**Entry Point 1: Header Button**
```
Main App → Click "🛠️ Create/Edit Templates" → Template Builder Opens
```

**Entry Point 2: Template Selection**
```
Main App → Step 2: Select Template → Choose "Create New Template..." →
Confirm "Yes" → Template Builder Opens
```

### From Template Builder to Main App

**Exit Point 1: Back Button**
```
Template Builder → Click "← Back to Main App" →
Check Unsaved Changes → Main App (Template Builder Closes)
```

**Exit Point 2: Window Close (X)**
```
Template Builder → Click [X] to close window →
Check Unsaved Changes → Main App (Template Builder Closes)
```

---

## Detailed Flow Diagrams

### Flow 1: First-Time User Creating Template

```
START: Main App Open
   ↓
[User clicks "🛠️ Create/Edit Templates"]
   ↓
Template Builder Window Opens
   ↓
[User enters template name: "My Template"]
   ↓
[User selects industry: "Fashion & Retail"]
   ↓
[User clicks "+ Add Slide" 5 times]
   ↓
[User configures each slide with components]
   ↓
[User clicks "Save Template"]
   ↓
File Dialog: Save as "My_Template.json"
   ↓
Template Saved Successfully
   ↓
[User clicks "← Back to Main App"]
   ↓
No Unsaved Changes (just saved)
   ↓
Template Builder Closes
   ↓
Main App: Template list refreshed
   ↓
"My Template" now available in dropdown
   ↓
END: User can now select and use template
```

### Flow 2: Quick Template Creation During Report Generation

```
START: Main App - Step 2 (Select Template)
   ↓
[User clicks "Select Template"]
   ↓
Template Selection Dialog Opens
   ↓
[User chooses "Create New Template..."]
   ↓
Confirmation: "Open Template Builder?"
   ↓
[User clicks "Yes"]
   ↓
Template Builder Window Opens
   ↓
[User quickly creates 3-slide template]
   ↓
[User clicks "Save Template"]
   ↓
Save Dialog: "Quick_Template.json"
   ↓
[User clicks "← Back to Main App"]
   ↓
Template Builder Closes
   ↓
Back to Step 2: Select Template
   ↓
"Quick_Template" now in dropdown
   ↓
[User selects "Quick_Template"]
   ↓
Continue to Step 3: Prepare Report
   ↓
END: Report generated with new template
```

### Flow 3: Editing Existing Template

```
START: Main App Open
   ↓
[User clicks "🛠️ Create/Edit Templates"]
   ↓
Template Builder Opens
   ↓
[User clicks "Load Template"]
   ↓
File Dialog: Select "BSH_Template.json"
   ↓
Template Loaded (8 slides)
   ↓
[User modifies Slide 5: Changes chart colors]
   ↓
[User adds new Slide 9]
   ↓
[User clicks "← Back to Main App"]
   ↓
Unsaved Changes Detected!
   ↓
Dialog: "Save changes before returning?"
   ├── [User clicks "Save"]
   │     ↓
   │   Save Dialog: Overwrite "BSH_Template.json"?
   │     ↓
   │   Template Saved
   │     ↓
   ├── [User clicks "Discard"]
   │     ↓
   │   Changes Discarded
   │     ↓
   └── [User clicks "Cancel"]
         ↓
       Stay in Template Builder
         ↓
       (User can continue editing)
         ↓
   Template Builder Closes (if saved/discarded)
   ↓
Main App: Updated "BSH_Template" available
   ↓
END: Template changes ready for use
```

---

## State Management

### Main App States

| State | Description | Template Builder Button |
|-------|-------------|-------------------------|
| **Initial** | App just opened | Enabled |
| **Excel Loaded** | File imported | Enabled |
| **Template Selected** | Template chosen | Enabled |
| **Generating** | Report in progress | Disabled (during generation) |
| **Report Ready** | Slides generated | Enabled |

### Template Builder States

| State | Description | Back Button Behavior |
|-------|-------------|---------------------|
| **Empty** | No slides added | Close immediately |
| **Has Slides** | Slides added | Check for unsaved changes |
| **Saved** | Just saved template | Close immediately |
| **Modified** | Changes after last save | Prompt to save |

---

## User Experience Scenarios

### Scenario 1: Power User (Agency Creating Multiple Templates)

```
Day 1: Setup Templates
━━━━━━━━━━━━━━━━━━━━━━
Main App → Template Builder
   Create "BSH_Template" (30 min)
   Save → Back

Main App → Template Builder
   Create "Sanofi_Template" (40 min)
   Save → Back

Main App → Template Builder
   Create "SOCAR_Template" (25 min)
   Save → Back

Day 2-30: Use Templates
━━━━━━━━━━━━━━━━━━━━━━━
Main App only:
   Import Excel → Select Template → Generate → Download
   (5 minutes per report, 3 reports/day)

Total Time Saved: 90% (from 30 hours → 3 hours/month)
```

### Scenario 2: Business User (Monthly Report)

```
Week 1: Create Template Once
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Main App → "Create/Edit Templates"
   Design template (45 min)
   Save as "Monthly_Sales.json"
   Back to Main App

Week 2-4: Reuse Template
━━━━━━━━━━━━━━━━━━━━━━━━━
Main App:
   Import new data
   Select "Monthly_Sales"
   Generate report
   Download
   (5 min/week)

Total Time: 1 hour (vs 10 hours manual)
Savings: 90%
```

### Scenario 3: Non-Technical User (First Time)

```
Initial Learning
━━━━━━━━━━━━━━━
1. Open Main App
2. See big orange "Create/Edit Templates" button
3. Click it → Template Builder opens
4. See 3 panels: Settings, Preview, Components
5. Follow on-screen prompts to build template
6. Click "Save Template"
7. Click "Back to Main App"
8. Template now available!

Subsequent Uses
━━━━━━━━━━━━━━━
1. Open Main App
2. Import Excel
3. Select template from dropdown
4. Generate & Download
5. Done!

Barrier to Entry: Very Low ✓
Technical Knowledge Required: None ✓
```

---

## Button Labels & Icons

### Main App
- **Primary Button**: `🛠️ Create/Edit Templates`
  - Icon: 🛠️ (Hammer and Wrench - represents building/editing)
  - Color: Amber/Orange (`#F59E0B`)
  - Position: Top-right header

### Template Builder
- **Navigation Button**: `← Back to Main App`
  - Icon: ← (Left Arrow - represents going back)
  - Color: Blue (`#3B82F6`)
  - Position: Top-right header

---

## Keyboard Shortcuts (Future Enhancement)

| Shortcut | Action | Context |
|----------|--------|---------|
| `Ctrl + T` | Open Template Builder | Main App |
| `Ctrl + W` | Close Template Builder | Template Builder |
| `Ctrl + S` | Save Template | Template Builder |
| `Escape` | Back to Main App (with confirm) | Template Builder |

---

## Accessibility

### Screen Reader Announcements
- "Create or Edit Templates button"
- "Back to Main Application button"
- "Unsaved changes dialog: Save, Discard, or Cancel"

### Keyboard Navigation
- Tab through all buttons
- Enter to activate
- Escape to cancel dialogs

### Visual Indicators
- Button color changes on hover
- Focus rings on keyboard navigation
- Clear dialog prompts

---

## Summary

✅ **Two Ways to Open Template Builder:**
1. Click header button (anytime)
2. Select "Create New Template..." (during workflow)

✅ **Two Ways to Return to Main App:**
1. Click "Back to Main App" button
2. Close window (X button)

✅ **Unsaved Changes Protection:**
- Automatic detection
- Three options: Save, Discard, Cancel
- No accidental data loss

✅ **Seamless Integration:**
- No command line needed
- No app restart required
- Context preserved
- User-friendly workflow

---

**Navigation is now intuitive and foolproof!** 🎉
