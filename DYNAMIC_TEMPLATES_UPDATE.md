# Dynamic Template Loading & Delete Functionality

## Overview
Implemented dynamic template discovery and deletion to make the Report Generator automatically detect templates created in the Template Builder.

## Problem Solved

### Before:
- ❌ Main App had hardcoded list of 3 templates (BSH, Sanofi, SOCAR)
- ❌ Templates created in Template Builder didn't appear in Main App
- ❌ Had to manually edit code to add new templates
- ❌ No way to delete templates from Template Builder

### After:
- ✅ Main App automatically scans `templates/configs/` directory
- ✅ All templates appear in dropdown immediately (after restart or refresh)
- ✅ Templates created in Template Builder show up automatically
- ✅ Can delete templates from Template Builder
- ✅ Template list refreshes when returning from Template Builder

## Features Implemented

### 1. Dynamic Template Loading
**Location:** [gui/main_window.py:715-761](gui/main_window.py#L715-L761)

**Functionality:**
- Scans `templates/configs/` directory for all `.json` files
- Reads each template to extract display name from metadata
- Supports both PPTGenerator format and Template Builder format
- Creates directory automatically if it doesn't exist
- Handles errors gracefully with fallback to filename

**Code:**
```python
def load_templates(self):
    """Load all templates from templates/configs/ directory."""
    template_map = {}
    templates_dir = os.path.join(os.getcwd(), "templates", "configs")
    os.makedirs(templates_dir, exist_ok=True)

    for filename in os.listdir(templates_dir):
        if filename.endswith('.json'):
            # Read template metadata
            with open(file_path, 'r', encoding='utf-8') as f:
                template_data = json.load(f)

            # Extract display name
            if 'metadata' in template_data:
                display_name = template_data['metadata'].get('name', filename[:-5])
            else:
                display_name = template_data.get('name', filename[:-5])

            template_map[display_name] = relative_path

    return template_map
```

### 2. Template Refresh
**Location:** [gui/main_window.py:763-785](gui/main_window.py#L763-L785)

**Functionality:**
- Automatically called when Template Builder window closes
- Reloads all templates from directory
- Updates dropdown with new templates
- Preserves user's current selection if template still exists

**Integration:**
```python
# In open_template_builder():
self.template_builder_window.destroyed.connect(self.refresh_templates)
```

### 3. Delete Template
**Location:** [gui/template_builder.py:945-1014](gui/template_builder.py#L945-L1014)

**Functionality:**
- Browse and select template to delete from `templates/configs/`
- Shows template name and filename for confirmation
- Requires explicit user confirmation
- Deletes file from disk
- Clears UI if deleted template was currently loaded

**UI:**
- Red "Delete Template" button in left panel
- File browser dialog to select template
- Confirmation dialog with template details
- Success/error messages

**Code:**
```python
def delete_template(self):
    """Delete an existing template from templates/configs/"""
    # Browse for template
    file_path, _ = QFileDialog.getOpenFileName(...)

    # Get template name for confirmation
    template_name = extract_name_from_json(file_path)

    # Confirm deletion
    reply = QMessageBox.question(
        self, "Delete Template",
        f"Are you sure you want to delete '{template_name}'?\n"
        "This action cannot be undone!",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )

    if reply == QMessageBox.StandardButton.Yes:
        os.remove(file_path)
        # Clear UI if deleted template was loaded
```

## User Workflow

### Creating and Using a New Template:

1. **Open Template Builder** from Main App
2. **Create Template:**
   - Enter template name (e.g., "My Custom Report")
   - Select industry
   - Choose colors and fonts
   - Add slides
3. **Save Template** → Saves to `templates/configs/My_Custom_Report_Template.json`
4. **Return to Main App** → Template list automatically refreshes
5. **Select Your Template** from dropdown → It's now available!

### Deleting a Template:

1. **Open Template Builder**
2. **Click "Delete Template"** (red button)
3. **Browse** to template file
4. **Confirm deletion** → Template removed from disk
5. **Return to Main App** → Template no longer in dropdown

## Technical Details

### Template Discovery Algorithm:

1. Scan `templates/configs/` directory
2. For each `.json` file:
   - Read file contents
   - Detect format (PPTGenerator vs Template Builder)
   - Extract display name from metadata or name field
   - Map display name → file path
3. Sort templates alphabetically
4. Populate dropdown

### Format Support:

**PPTGenerator Format:**
```json
{
  "metadata": {
    "name": "Display Name Here"
  }
}
```

**Template Builder Format:**
```json
{
  "name": "Display Name Here"
}
```

Both formats are auto-detected and supported.

### Error Handling:

- Missing directory → Creates automatically
- Corrupted JSON → Uses filename as fallback
- Missing metadata → Uses filename as fallback
- Delete errors → Shows error dialog
- Empty directory → Returns empty map (no crash)

## Files Modified

1. **[gui/main_window.py](gui/main_window.py)**
   - Replaced hardcoded template map with `load_templates()` call
   - Added `load_templates()` method (lines 715-761)
   - Implemented `refresh_templates()` method (lines 763-785)
   - Connected Template Builder close event to refresh

2. **[gui/template_builder.py](gui/template_builder.py)**
   - Added "Delete Template" button (lines 377-392)
   - Implemented `delete_template()` method (lines 945-1014)
   - Styled delete button in red for visibility

## Benefits

### For Users:
- ✅ No manual configuration needed
- ✅ Templates appear automatically
- ✅ Easy template management
- ✅ Safe deletion with confirmation
- ✅ Seamless workflow

### For Developers:
- ✅ No hardcoded template lists
- ✅ Extensible architecture
- ✅ Easy to add new templates
- ✅ Automatic template discovery
- ✅ Clean separation of concerns

## Testing

### Test Scenarios:

1. **Create New Template:**
   - Open Template Builder
   - Create "Test Template"
   - Save to `templates/configs/`
   - Close Template Builder
   - ✅ Verify "Test Template" appears in Main App dropdown

2. **Delete Template:**
   - Open Template Builder
   - Click "Delete Template"
   - Select "Test Template"
   - Confirm deletion
   - ✅ Verify file deleted from disk
   - Return to Main App
   - ✅ Verify template no longer in dropdown

3. **Multiple Templates:**
   - Create 5 different templates
   - ✅ Verify all appear in dropdown
   - ✅ Verify sorted alphabetically
   - Delete 2 templates
   - ✅ Verify only 3 remain

4. **Empty Directory:**
   - Delete all templates
   - ✅ Verify app doesn't crash
   - ✅ Verify dropdown is empty (or shows "Create New Template...")

## Known Limitations

1. **Requires Restart for External Changes:**
   - If template files are added/deleted outside the app, requires app restart
   - Workaround: Use Template Builder for all template management

2. **No Undo for Deletion:**
   - Once deleted, template is permanently removed
   - Workaround: Keep backups of important templates

3. **No Template Versioning:**
   - Overwriting a template loses previous version
   - Future: Add version control or backup system

## Future Enhancements

### Planned Features:
- 📋 Template list with preview thumbnails
- 🔍 Search/filter templates by industry
- 📁 Template categories/folders
- 💾 Automatic template backups
- 🔄 Template import/export (bulk operations)
- ⭐ Favorite/star templates
- 📊 Template usage statistics

## Summary

The dynamic template loading system makes ReportForge significantly more user-friendly:

**Before:** Manual code editing required to add templates
**After:** Automatic discovery and management

**Before:** No way to remove templates
**After:** Safe deletion with confirmation

**Before:** Hardcoded 3 templates only
**After:** Unlimited templates, auto-discovered

This brings ReportForge one step closer to being a true production-ready application that non-technical users can fully utilize.

---

**Status:** ✅ Complete
**Last Updated:** 2025-11-30
**Author:** Claude (Sonnet 4.5)
