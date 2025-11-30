"""
Template Builder GUI
Visual interface for creating and editing report templates
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
from template_manager import TemplateManager


class TemplateBuilderGUI:
    """GUI for building and editing report templates"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("ReportForge - Template Builder")
        self.root.geometry("1000x700")
        
        self.template_manager = TemplateManager()
        self.current_template = None
        self.current_slide_config = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the main UI layout"""
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Tab 1: Template Info
        self.info_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.info_tab, text="Template Info")
        self.create_info_tab()
        
        # Tab 2: Data Mapping
        self.mapping_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.mapping_tab, text="Data Mapping")
        self.create_mapping_tab()
        
        # Tab 3: Slides Configuration
        self.slides_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.slides_tab, text="Slides")
        self.create_slides_tab()
        
        # Tab 4: Processing Rules
        self.rules_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.rules_tab, text="Processing Rules")
        self.create_rules_tab()
        
        # Bottom buttons
        self.create_bottom_buttons()
    
    def create_info_tab(self):
        """Create template info tab"""
        frame = ttk.LabelFrame(self.info_tab, text="Template Information", padding=10)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Template Name
        ttk.Label(frame, text="Template Name:").grid(row=0, column=0, sticky='w', pady=5)
        self.name_entry = ttk.Entry(frame, width=40)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        # Client Name
        ttk.Label(frame, text="Client/Brand:").grid(row=1, column=0, sticky='w', pady=5)
        self.client_entry = ttk.Entry(frame, width=40)
        self.client_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        
        # Description
        ttk.Label(frame, text="Description:").grid(row=2, column=0, sticky='nw', pady=5)
        self.description_text = tk.Text(frame, height=4, width=40)
        self.description_text.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        
        # PowerPoint Template
        ttk.Label(frame, text="PPT Template:").grid(row=3, column=0, sticky='w', pady=5)
        
        ppt_frame = ttk.Frame(frame)
        ppt_frame.grid(row=3, column=1, sticky='ew', padx=5, pady=5)
        
        self.ppt_path_entry = ttk.Entry(ppt_frame, width=30)
        self.ppt_path_entry.pack(side='left', fill='x', expand=True)
        
        ttk.Button(ppt_frame, text="Browse", command=self.browse_ppt_template).pack(side='left', padx=5)
        
        frame.columnconfigure(1, weight=1)
    
    def create_mapping_tab(self):
        """Create data mapping tab"""
        frame = ttk.LabelFrame(self.mapping_tab, text="Excel Data Mapping", padding=10)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Sheet Name
        ttk.Label(frame, text="Sheet Name:").grid(row=0, column=0, sticky='w', pady=5)
        self.sheet_name_entry = ttk.Entry(frame, width=30)
        self.sheet_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        # Column Mappings
        ttk.Label(frame, text="Column Mappings:", font=('Arial', 10, 'bold')).grid(
            row=1, column=0, columnspan=2, sticky='w', pady=(15, 5)
        )
        
        # Column mapping list
        mapping_frame = ttk.Frame(frame)
        mapping_frame.grid(row=2, column=0, columnspan=2, sticky='nsew', pady=5)
        
        # Create treeview for column mappings
        columns = ('Excel Column', 'Internal Name', 'Data Type')
        self.mapping_tree = ttk.Treeview(mapping_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.mapping_tree.heading(col, text=col)
            self.mapping_tree.column(col, width=150)
        
        self.mapping_tree.pack(side='left', fill='both', expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(mapping_frame, orient='vertical', command=self.mapping_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.mapping_tree.configure(yscrollcommand=scrollbar.set)
        
        # Buttons for managing mappings
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Add Mapping", command=self.add_column_mapping).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Remove Mapping", command=self.remove_column_mapping).pack(side='left', padx=5)
        
        frame.rowconfigure(2, weight=1)
        frame.columnconfigure(1, weight=1)
    
    def create_slides_tab(self):
        """Create slides configuration tab"""
        # Left side: Slides list
        left_frame = ttk.LabelFrame(self.slides_tab, text="Slides", padding=10)
        left_frame.pack(side='left', fill='both', expand=False, padx=(10, 5), pady=10)
        
        self.slides_listbox = tk.Listbox(left_frame, width=30, height=20)
        self.slides_listbox.pack(fill='both', expand=True)
        self.slides_listbox.bind('<<ListboxSelect>>', self.on_slide_select)
        
        # Slide management buttons
        slide_btn_frame = ttk.Frame(left_frame)
        slide_btn_frame.pack(fill='x', pady=(5, 0))
        
        ttk.Button(slide_btn_frame, text="Add Slide", command=self.add_slide).pack(fill='x', pady=2)
        ttk.Button(slide_btn_frame, text="Remove Slide", command=self.remove_slide).pack(fill='x', pady=2)
        ttk.Button(slide_btn_frame, text="Move Up", command=self.move_slide_up).pack(fill='x', pady=2)
        ttk.Button(slide_btn_frame, text="Move Down", command=self.move_slide_down).pack(fill='x', pady=2)
        
        # Right side: Slide configuration
        right_frame = ttk.LabelFrame(self.slides_tab, text="Slide Configuration", padding=10)
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 10), pady=10)
        
        # Slide Title
        ttk.Label(right_frame, text="Slide Title:").grid(row=0, column=0, sticky='w', pady=5)
        self.slide_title_entry = ttk.Entry(right_frame, width=40)
        self.slide_title_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        # Slide Type
        ttk.Label(right_frame, text="Slide Type:").grid(row=1, column=0, sticky='w', pady=5)
        self.slide_type_combo = ttk.Combobox(
            right_frame,
            values=["table", "chart", "text", "mixed"],
            state='readonly',
            width=37
        )
        self.slide_type_combo.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        # Components section
        ttk.Label(right_frame, text="Components:", font=('Arial', 10, 'bold')).grid(
            row=2, column=0, columnspan=2, sticky='w', pady=(15, 5)
        )
        
        # Components list
        components_frame = ttk.Frame(right_frame)
        components_frame.grid(row=3, column=0, columnspan=2, sticky='nsew', pady=5)
        
        self.components_listbox = tk.Listbox(components_frame, height=8)
        self.components_listbox.pack(side='left', fill='both', expand=True)
        
        comp_scroll = ttk.Scrollbar(components_frame, orient='vertical', command=self.components_listbox.yview)
        comp_scroll.pack(side='right', fill='y')
        self.components_listbox.configure(yscrollcommand=comp_scroll.set)
        
        # Component buttons
        comp_btn_frame = ttk.Frame(right_frame)
        comp_btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(comp_btn_frame, text="Add Table", command=self.add_table_component).pack(side='left', padx=5)
        ttk.Button(comp_btn_frame, text="Add Chart", command=self.add_chart_component).pack(side='left', padx=5)
        ttk.Button(comp_btn_frame, text="Add Text", command=self.add_text_component).pack(side='left', padx=5)
        ttk.Button(comp_btn_frame, text="Remove", command=self.remove_component).pack(side='left', padx=5)
        
        right_frame.rowconfigure(3, weight=1)
        right_frame.columnconfigure(1, weight=1)
    
    def create_rules_tab(self):
        """Create processing rules tab"""
        frame = ttk.LabelFrame(self.rules_tab, text="Data Processing Rules", padding=10)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Sort By
        ttk.Label(frame, text="Sort By Column:").grid(row=0, column=0, sticky='w', pady=5)
        self.sort_column_entry = ttk.Entry(frame, width=30)
        self.sort_column_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        # Sort Order
        ttk.Label(frame, text="Sort Order:").grid(row=1, column=0, sticky='w', pady=5)
        self.sort_order_combo = ttk.Combobox(
            frame,
            values=["ascending", "descending"],
            state='readonly',
            width=27
        )
        self.sort_order_combo.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.sort_order_combo.set("descending")
        
        # Number Format
        ttk.Label(frame, text="Decimal Places:").grid(row=2, column=0, sticky='w', pady=5)
        self.decimal_places_spin = ttk.Spinbox(frame, from_=0, to=4, width=28)
        self.decimal_places_spin.set(2)
        self.decimal_places_spin.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        
        # Thousands separator
        self.thousands_sep_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            frame,
            text="Use thousands separator (1,000)",
            variable=self.thousands_sep_var
        ).grid(row=3, column=0, columnspan=2, sticky='w', pady=5, padx=5)
        
        # Currency Symbol
        ttk.Label(frame, text="Currency Symbol:").grid(row=4, column=0, sticky='w', pady=5)
        self.currency_entry = ttk.Entry(frame, width=30)
        self.currency_entry.insert(0, "₺")
        self.currency_entry.grid(row=4, column=1, padx=5, pady=5, sticky='w')
    
    def create_bottom_buttons(self):
        """Create bottom action buttons"""
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(button_frame, text="New Template", command=self.new_template).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Load Template", command=self.load_template).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Save Template", command=self.save_template).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Save As...", command=self.save_template_as).pack(side='left', padx=5)
        
        ttk.Separator(button_frame, orient='vertical').pack(side='left', fill='y', padx=10)
        
        ttk.Button(button_frame, text="Preview JSON", command=self.preview_json).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Validate", command=self.validate_template).pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="Close", command=self.root.quit).pack(side='right', padx=5)
    
    # Event handlers
    def browse_ppt_template(self):
        """Browse for PowerPoint template file"""
        filepath = filedialog.askopenfilename(
            title="Select PowerPoint Template",
            filetypes=[("PowerPoint files", "*.pptx"), ("All files", "*.*")]
        )
        if filepath:
            self.ppt_path_entry.delete(0, tk.END)
            self.ppt_path_entry.insert(0, filepath)
    
    def add_column_mapping(self):
        """Add a new column mapping"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Column Mapping")
        dialog.geometry("400x200")
        
        ttk.Label(dialog, text="Excel Column Name:").grid(row=0, column=0, sticky='w', padx=10, pady=5)
        excel_col_entry = ttk.Entry(dialog, width=30)
        excel_col_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Internal Name:").grid(row=1, column=0, sticky='w', padx=10, pady=5)
        internal_name_entry = ttk.Entry(dialog, width=30)
        internal_name_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Data Type:").grid(row=2, column=0, sticky='w', padx=10, pady=5)
        data_type_combo = ttk.Combobox(
            dialog,
            values=["text", "number", "currency", "percentage", "date"],
            state='readonly',
            width=27
        )
        data_type_combo.set("text")
        data_type_combo.grid(row=2, column=1, padx=10, pady=5)
        
        def on_add():
            excel_col = excel_col_entry.get().strip()
            internal_name = internal_name_entry.get().strip()
            data_type = data_type_combo.get()
            
            if excel_col and internal_name:
                self.mapping_tree.insert('', 'end', values=(excel_col, internal_name, data_type))
                dialog.destroy()
            else:
                messagebox.showwarning("Invalid Input", "Please fill all fields")
        
        ttk.Button(dialog, text="Add", command=on_add).grid(row=3, column=0, columnspan=2, pady=20)
    
    def remove_column_mapping(self):
        """Remove selected column mapping"""
        selected = self.mapping_tree.selection()
        if selected:
            self.mapping_tree.delete(selected)
    
    def add_slide(self):
        """Add a new slide to the template"""
        slide_num = self.slides_listbox.size() + 1
        self.slides_listbox.insert(tk.END, f"Slide {slide_num}: New Slide")
    
    def remove_slide(self):
        """Remove selected slide"""
        selected = self.slides_listbox.curselection()
        if selected:
            self.slides_listbox.delete(selected)
    
    def move_slide_up(self):
        """Move selected slide up"""
        selected = self.slides_listbox.curselection()
        if selected and selected[0] > 0:
            idx = selected[0]
            text = self.slides_listbox.get(idx)
            self.slides_listbox.delete(idx)
            self.slides_listbox.insert(idx - 1, text)
            self.slides_listbox.selection_set(idx - 1)
    
    def move_slide_down(self):
        """Move selected slide down"""
        selected = self.slides_listbox.curselection()
        if selected and selected[0] < self.slides_listbox.size() - 1:
            idx = selected[0]
            text = self.slides_listbox.get(idx)
            self.slides_listbox.delete(idx)
            self.slides_listbox.insert(idx + 1, text)
            self.slides_listbox.selection_set(idx + 1)
    
    def on_slide_select(self, event):
        """Handle slide selection"""
        pass
    
    def add_table_component(self):
        """Add table component to current slide"""
        self.components_listbox.insert(tk.END, "Table Component")
    
    def add_chart_component(self):
        """Add chart component to current slide"""
        self.components_listbox.insert(tk.END, "Chart Component")
    
    def add_text_component(self):
        """Add text component to current slide"""
        self.components_listbox.insert(tk.END, "Text Component")
    
    def remove_component(self):
        """Remove selected component"""
        selected = self.components_listbox.curselection()
        if selected:
            self.components_listbox.delete(selected)
    
    def new_template(self):
        """Create a new template"""
        self.current_template = self.template_manager.create_template(
            name="New Template",
            client="",
            description=""
        )
        self.clear_form()
        messagebox.showinfo("Success", "New template created")
    
    def load_template(self):
        """Load an existing template"""
        filepath = filedialog.askopenfilename(
            title="Load Template",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialdir=self.template_manager.templates_dir
        )
        
        if filepath:
            template = self.template_manager.load_template(filepath)
            if template:
                self.current_template = template
                self.populate_form(template)
                messagebox.showinfo("Success", f"Template '{template['name']}' loaded")
    
    def save_template(self):
        """Save current template"""
        if not self.current_template:
            self.save_template_as()
            return
        
        self.update_template_from_form()
        
        is_valid, errors = self.template_manager.validate_template(self.current_template)
        if not is_valid:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return
        
        filepath = self.template_manager.save_template(self.current_template)
        messagebox.showinfo("Success", f"Template saved:\n{filepath}")
    
    def save_template_as(self):
        """Save template with new name"""
        self.update_template_from_form()
        
        filepath = filedialog.asksaveasfilename(
            title="Save Template As",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialdir=self.template_manager.templates_dir
        )
        
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.current_template, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Success", f"Template saved:\n{filepath}")
    
    def preview_json(self):
        """Preview template as JSON"""
        if not self.current_template:
            messagebox.showwarning("No Template", "Please create or load a template first")
            return
        
        self.update_template_from_form()
        
        # Create preview window
        preview_window = tk.Toplevel(self.root)
        preview_window.title("Template JSON Preview")
        preview_window.geometry("600x500")
        
        text_widget = scrolledtext.ScrolledText(preview_window, wrap=tk.WORD)
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)
        
        json_str = json.dumps(self.current_template, indent=2, ensure_ascii=False)
        text_widget.insert('1.0', json_str)
        text_widget.config(state='disabled')
    
    def validate_template(self):
        """Validate current template"""
        if not self.current_template:
            messagebox.showwarning("No Template", "Please create or load a template first")
            return
        
        self.update_template_from_form()
        
        is_valid, errors = self.template_manager.validate_template(self.current_template)
        
        if is_valid:
            messagebox.showinfo("Validation", "Template is valid! ✓")
        else:
            messagebox.showerror("Validation Errors", "\n".join(errors))
    
    def clear_form(self):
        """Clear all form fields"""
        self.name_entry.delete(0, tk.END)
        self.client_entry.delete(0, tk.END)
        self.description_text.delete('1.0', tk.END)
        self.ppt_path_entry.delete(0, tk.END)
        self.sheet_name_entry.delete(0, tk.END)
        
        for item in self.mapping_tree.get_children():
            self.mapping_tree.delete(item)
        
        self.slides_listbox.delete(0, tk.END)
        self.components_listbox.delete(0, tk.END)
    
    def populate_form(self, template):
        """Populate form with template data"""
        self.clear_form()
        
        self.name_entry.insert(0, template.get('name', ''))
        self.client_entry.insert(0, template.get('client', ''))
        self.description_text.insert('1.0', template.get('description', ''))
        self.ppt_path_entry.insert(0, template.get('ppt_template_path', ''))
        
        # Data mapping
        data_mapping = template.get('data_mapping', {})
        self.sheet_name_entry.insert(0, data_mapping.get('sheet_name', ''))
        
        for excel_col, internal_name in data_mapping.get('columns', {}).items():
            self.mapping_tree.insert('', 'end', values=(excel_col, internal_name, 'text'))
        
        # Slides
        for i, slide in enumerate(template.get('slides', [])):
            slide_title = slide.get('title', f'Slide {i+1}')
            self.slides_listbox.insert(tk.END, f"Slide {i+1}: {slide_title}")
        
        # Processing rules
        rules = template.get('processing_rules', {})
        self.sort_column_entry.insert(0, rules.get('sort_by', ''))
        self.sort_order_combo.set(rules.get('sort_order', 'descending'))
    
    def update_template_from_form(self):
        """Update template object from form fields"""
        if not self.current_template:
            self.current_template = self.template_manager.create_template("", "", "")
        
        self.current_template['name'] = self.name_entry.get()
        self.current_template['client'] = self.client_entry.get()
        self.current_template['description'] = self.description_text.get('1.0', tk.END).strip()
        self.current_template['ppt_template_path'] = self.ppt_path_entry.get()
        
        # Data mapping
        self.current_template['data_mapping']['sheet_name'] = self.sheet_name_entry.get()
        
        columns = {}
        for item in self.mapping_tree.get_children():
            values = self.mapping_tree.item(item)['values']
            columns[values[0]] = values[1]
        self.current_template['data_mapping']['columns'] = columns
        
        # Processing rules
        self.current_template['processing_rules']['sort_by'] = self.sort_column_entry.get()
        self.current_template['processing_rules']['sort_order'] = self.sort_order_combo.get()
        
        # Formatting
        self.current_template['formatting']['number_format']['decimal_places'] = int(
            self.decimal_places_spin.get()
        )
        self.current_template['formatting']['number_format']['use_thousands_separator'] = (
            self.thousands_sep_var.get()
        )
        self.current_template['formatting']['currency_symbol'] = self.currency_entry.get()


def main():
    root = tk.Tk()
    app = TemplateBuilderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()






