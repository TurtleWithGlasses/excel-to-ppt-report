# Unfinished Components & Features

**Last Updated:** 2025-12-01

## Overview

This document identifies incomplete features and components in the ReportForge system that need to be finished.

---

## 🔴 High Priority - Component Features

### 1. Template Brand Colors Integration ⚠️ **INCOMPLETE**

**Location:** `components/chart_component.py` (line 477)

**Current Status:**
- ChartComponent has hardcoded brand colors when `colors='brand'` is set
- Templates have `color_scheme` in settings but components can't access it

**Issue:**
```python
# Current code (line 477):
if self.colors == 'brand':
    # Use template brand colors (TODO: get from template)
    return ['#2563EB', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899']
```

**Template Structure:**
```json
{
  "settings": {
    "color_scheme": {
      "primary": "#2563EB",
      "secondary": "#10B981",
      "accent": "#F59E0B",
      "negative": "#EF4444",
      "neutral": "#6B7280"
    }
  }
}
```

**What Needs to be Done:**
1. Pass template reference to components during rendering
2. Update ChartComponent to extract colors from template settings
3. Update other components (TableComponent, SummaryComponent) to use template colors
4. Add fallback to default colors if template doesn't have color_scheme

**Estimated Time:** 2-3 hours

**Files to Modify:**
- `components/chart_component.py`
- `components/table_component.py`
- `components/summary_component.py`
- `core/ppt_generator.py` (pass template to components)

---

### 2. Template Logo Path Support ⚠️ **INCOMPLETE**

**Location:** `components/image_component.py` (line 130-135)

**Current Status:**
- ImageComponent supports `type: 'template_logo'` but can't access template logo path
- Templates don't have logo_path in their structure yet

**Issue:**
```python
# Current code (line 130-135):
if self.image_type == 'template_logo':
    # Logo path should come from template data
    if data and isinstance(data, dict) and 'template_logo' in data:
        return data['template_logo']
```

**What Needs to be Done:**
1. Add `logo_path` to template settings structure
2. Pass template reference to ImageComponent
3. Extract logo_path from template settings
4. Update template JSON files to include logo_path

**Estimated Time:** 1-2 hours

**Files to Modify:**
- `components/image_component.py`
- `core/ppt_generator.py`
- `templates/configs/*.json` (add logo_path to settings)

---

### 3. ImageComponent Advanced Styling ⚠️ **PARTIALLY INCOMPLETE**

**Location:** `components/image_component.py` (line 137-155)

**Current Status:**
- ImageComponent accepts styling config (opacity, border, corner_radius) but doesn't implement them
- Marked as "not implemented in basic python-pptx"

**Issue:**
```python
# Current code (line 147-155):
# Opacity (transparency)
if self.opacity < 100:
    # Note: This requires accessing the underlying XML
    # Not implemented in basic python-pptx
    pass

# Border and corner radius would require direct XML manipulation
# Beyond scope of basic implementation
pass
```

**What Needs to be Done:**
1. Implement opacity using python-pptx XML manipulation
2. Implement border styling via XML
3. Implement corner radius (rounded rectangles) via XML
4. Add error handling for XML manipulation failures

**Estimated Time:** 4-6 hours (requires XML knowledge)

**Files to Modify:**
- `components/image_component.py`

**Note:** This requires knowledge of PowerPoint XML structure and python-pptx's XML API.

---

## 🟡 Medium Priority - Code Cleanup

### 4. Remove Debug Statements

**Location:** `components/chart_component.py` (multiple lines)

**Current Status:**
- Debug print statements left in production code
- Should be removed or converted to proper logging

**Lines to Remove/Update:**
- Line 222: `print(f"[DEBUG] Raw dimensions: {raw_width}x{raw_height} inches")`
- Line 226: `print(f"[DEBUG] Clamping width from {raw_width} to 20.0")`
- Line 232: `print(f"[DEBUG] Clamping height from {raw_height} to 15.0")`
- Line 240: `print(f"[DEBUG] Final dimensions: ...")`
- Line 249: `print(f"[DEBUG] Scaled DPI from {old_dpi} to {dpi}")`
- Line 302: `print(f"[DEBUG] Scaling DPI from {dpi} to {new_dpi}...")`
- Line 320: `print(f"[DEBUG] Resized image to {new_width}x{new_height}px")`

**What Needs to be Done:**
1. Remove debug print statements OR
2. Convert to proper logging using Python `logging` module
3. Add log level configuration

**Estimated Time:** 30 minutes

**Files to Modify:**
- `components/chart_component.py`

---

## 🟢 Low Priority - Future Enhancements

### 5. Component Editor UI ⚠️ **NOT STARTED**

**Location:** `gui/template_builder.py`

**Current Status:**
- Template Builder can create/edit templates
- Cannot visually add/edit components
- Components must be added manually via JSON

**What Needs to be Done:**
1. Create component selector panel
2. Add visual slide canvas (representing 16:9 slide)
3. Implement drag-and-drop component placement
4. Create property editor panel for component configuration
5. Add component preview rendering
6. Save component data to template JSON

**Estimated Time:** 8-12 hours

**Files to Create/Modify:**
- `gui/component_editor.py` (new file)
- `gui/template_builder.py` (integrate component editor)

**Note:** This is a major feature and is listed as next priority in PROJECT_STATUS.md

---

## 📋 Summary

### Quick Wins (Can be done in 1-2 hours each):
1. ✅ **Template Brand Colors Integration** - High value, low effort
2. ✅ **Template Logo Path Support** - High value, low effort
3. ✅ **Remove Debug Statements** - Cleanup, 30 minutes

### Medium Effort (4-6 hours):
4. ⚠️ **ImageComponent Advanced Styling** - Requires XML knowledge

### Major Features (8-12 hours):
5. 🚧 **Component Editor UI** - Major feature, requires GUI work

---

## Recommended Work Order

1. **Start with Template Brand Colors** (2-3 hours)
   - High impact, relatively easy
   - Makes templates more consistent
   - Used by multiple components

2. **Template Logo Path Support** (1-2 hours)
   - Quick to implement
   - Useful for branded reports

3. **Remove Debug Statements** (30 minutes)
   - Quick cleanup
   - Improves code quality

4. **ImageComponent Styling** (4-6 hours)
   - If needed for production
   - Requires XML manipulation knowledge

5. **Component Editor UI** (8-12 hours)
   - Major feature
   - Makes template creation user-friendly
   - Should be done after core features are stable

---

## Implementation Notes

### Template Brand Colors Integration

**Approach:**
1. Modify `PPTGenerator._render_component()` to pass template reference
2. Update `BaseComponent.__init__()` to accept optional template parameter
3. Add method to extract colors from template settings
4. Update ChartComponent, TableComponent, SummaryComponent to use template colors

**Example:**
```python
# In ppt_generator.py
def _render_component(self, slide, component_config: Dict[str, Any]) -> None:
    # Get template for brand colors
    template = self.template_manager.current_template
    
    # Create component with template reference
    component = self.component_factory.create_component(
        component_config, 
        template=template  # Pass template
    )
```

### Template Logo Path

**Approach:**
1. Add `logo_path` to template settings structure
2. Pass template to ImageComponent
3. Extract logo_path from template.settings.logo_path

**Template Structure:**
```json
{
  "settings": {
    "logo_path": "assets/company_logo.png",
    "color_scheme": {...}
  }
}
```

---

## Testing Checklist

After implementing each feature:

- [ ] Test with BSH template
- [ ] Test with Sanofi template
- [ ] Test with SOCAR template
- [ ] Verify colors are applied correctly
- [ ] Verify logo paths work
- [ ] Test with missing color_scheme (fallback)
- [ ] Test with missing logo_path (placeholder)
- [ ] Run all existing tests
- [ ] Generate sample reports

---

## Questions to Consider

1. **Should brand colors be required in templates?** (Currently optional)
2. **Should we support multiple logo types?** (header, footer, watermark)
3. **Should ImageComponent styling be a priority?** (May not be needed for MVP)
4. **When should Component Editor be built?** (After core features are stable)

---

**Status:** Ready for implementation! 🚀












