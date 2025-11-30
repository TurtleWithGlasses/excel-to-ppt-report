import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from template_manager import TemplateManager
from main import generate_report_from_template, generate_report_direct
import os


class PPTReportGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ReportForge - PPT Report Generator")
        self.root.geometry("900x700")

        # Initialize template manager
        self.template_manager = TemplateManager()
        self.selected_file = None
        self.selected_template = None
        self.generated_report_path = None

        # Main container
        main_container = ttk.Frame(root)
        main_container.pack(fill='both', expand=True, padx=10, pady=10)

        # Left panel (controls)
        self.frame1 = ttk.LabelFrame(main_container, text="Report Configuration", padding=10)
        self.frame1.pack(side="left", fill="y", padx=(0, 10))

        # Right panel (preview)
        self.frame2 = ttk.LabelFrame(main_container, text="Preview & Output", padding=10)
        self.frame2.pack(side="left", fill="both", expand=True)

        # Setup UI components
        self.create_template_selector()
        self.create_brand_selector()
        self.create_file_selector()
        self.create_report_name_entry()
        self.create_generate_button()
        self.create_save_button()
        self.create_template_management_buttons()
        self.create_report_preview()
    
    def create_template_selector(self):
        """Dropdown for selecting template"""
        ttk.Label(self.frame1, text="Select Template:", font=('Arial', 10, 'bold')).pack(pady=(5, 2))
        
        # Template selection frame
        template_frame = ttk.Frame(self.frame1)
        template_frame.pack(fill='x', padx=5, pady=5)
        
        self.template_combobox = ttk.Combobox(template_frame, state="readonly", width=25)
        self.template_combobox.pack(side='top', fill='x')
        self.template_combobox.bind('<<ComboboxSelected>>', self.on_template_selected)
        
        # Refresh templates button
        ttk.Button(
            template_frame,
            text="↻ Refresh",
            command=self.refresh_templates,
            width=10
        ).pack(side='top', pady=(2, 0))
        
        # Template info display
        self.template_info_label = ttk.Label(
            self.frame1,
            text="No template selected",
            wraplength=250,
            justify='left',
            foreground='gray'
        )
        self.template_info_label.pack(pady=5)
        
        # Load templates initially
        self.refresh_templates()
    
    def create_brand_selector(self):
        """Combobox for selecting brand (for backward compatibility)"""
        ttk.Separator(self.frame1, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(self.frame1, text="Or Quick Select Brand:").pack(pady=(5, 2))
        
        self.brand_combobox = ttk.Combobox(self.frame1, values=["BSH"], state="readonly", width=25)
        self.brand_combobox.pack(pady=5, padx=5)

    def create_file_selector(self):
        """Button and label for file selection"""
        ttk.Separator(self.frame1, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(self.frame1, text="Excel Data File:", font=('Arial', 10, 'bold')).pack(pady=(5, 2))
        
        ttk.Button(
            self.frame1,
            text="📁 Choose Excel File",
            command=self.on_choose_file
        ).pack(pady=5, padx=5, fill='x')

        self.selected_file_label = ttk.Label(
            self.frame1,
            text="No file selected",
            foreground="gray",
            wraplength=250
        )
        self.selected_file_label.pack(pady=5)

    def refresh_templates(self):
        """Refresh the list of available templates"""
        templates = self.template_manager.list_templates()
        
        template_names = ["[No Template - Direct Mode]"] + [
            f"{tmpl['name']} ({tmpl['client']})" for tmpl in templates
        ]
        
        self.template_combobox['values'] = template_names
        
        if template_names:
            self.template_combobox.current(0)
        
        # Store template data for easy access
        self.templates_data = {
            f"{tmpl['name']} ({tmpl['client']})": tmpl for tmpl in templates
        }
    
    def on_template_selected(self, event):
        """Handle template selection"""
        selected = self.template_combobox.get()
        
        if selected == "[No Template - Direct Mode]":
            self.selected_template = None
            self.template_info_label.config(
                text="Direct mode: Manually select brand and Excel file",
                foreground='gray'
            )
            return
        
        if selected in self.templates_data:
            template_data = self.templates_data[selected]
            self.selected_template = template_data['filepath']
            
            info_text = f"Client: {template_data['client']}\n"
            info_text += f"Description: {template_data.get('description', 'N/A')}"
            
            self.template_info_label.config(text=info_text, foreground='black')
    
    def on_choose_file(self):
        """Open file dialog to choose Excel file"""
        file_path = filedialog.askopenfilename(
            title="Select Excel Data File",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if file_path:
            self.selected_file = file_path
            filename = os.path.basename(file_path)
            self.selected_file_label.config(text=f"✓ {filename}", foreground='green')

    def create_report_name_entry(self):
        """Entry for report name"""
        ttk.Separator(self.frame1, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(self.frame1, text="Report Name (Optional):").pack(pady=(5, 2))

        self.report_name_entry = ttk.Entry(self.frame1, width=28)
        self.report_name_entry.pack(pady=5, padx=5)

    def create_generate_button(self):
        """Button to generate report"""
        ttk.Separator(self.frame1, orient='horizontal').pack(fill='x', pady=10)
        
        self.generate_button = ttk.Button(
            self.frame1,
            text="🚀 Generate Report",
            command=self.on_generate_report,
            style='Accent.TButton'
        )
        self.generate_button.pack(pady=10, padx=5, fill='x')

    def on_generate_report(self):
        """Logic to generate the report"""
        # Validate inputs
        if not self.selected_file:
            messagebox.showerror("Error", "Please select an Excel file.")
            return
        
        if not os.path.exists(self.selected_file):
            messagebox.showerror("Error", "Selected Excel file does not exist.")
            return
        
        # Disable generate button during processing
        self.generate_button.config(state='disabled', text='⏳ Generating...')
        self.root.update()
        
        try:
            # Determine output path
            report_name = self.report_name_entry.get().strip()
            if not report_name:
                report_name = "Generated_Report"
            
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"{report_name}.pptx")
            
            # Generate report based on mode
            if self.selected_template:
                # Template-based generation
                self.update_preview(f"Generating report using template...\nData: {self.selected_file}")
                result_path = generate_report_from_template(
                    self.selected_template,
                    self.selected_file,
                    output_path
                )
            else:
                # Direct mode generation
                brand = self.brand_combobox.get()
                if not brand:
                    messagebox.showerror("Error", "Please select a brand or template.")
                    return
                
                # Use default paths for direct mode
                ppt_template_path = f"templates/{brand} Template.pptx"
                if not os.path.exists(ppt_template_path):
                    ppt_template_path = "templates/BSH Kasım Ayı Aylık Medya Yansıma Raporu 24.pptx"
                
                sheet_name = brand  # Assume sheet name matches brand
                
                self.update_preview(f"Generating report (direct mode)...\nBrand: {brand}\nData: {self.selected_file}")
                result_path = generate_report_direct(
                    self.selected_file,
                    ppt_template_path,
                    sheet_name,
                    output_path
                )
            
            if result_path:
                self.generated_report_path = result_path
                self.save_button.config(state='normal')
                
                success_msg = f"✓ Report generated successfully!\n\nSaved to:\n{result_path}"
                messagebox.showinfo("Success", success_msg)
                
                self.update_preview(
                    f"Report Generated Successfully!\n\n"
                    f"Output: {result_path}\n"
                    f"Source: {self.selected_file}\n"
                    f"Template: {self.selected_template or 'Direct Mode'}\n\n"
                    f"You can now save this report to a different location."
                )
            else:
                messagebox.showerror("Error", "Report generation failed. Check console for details.")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
            self.update_preview(f"Error during generation:\n{str(e)}")
        
        finally:
            # Re-enable generate button
            self.generate_button.config(state='normal', text='🚀 Generate Report')

    def create_save_button(self):
        """Button to save PPT file in your computer"""
        self.save_button = ttk.Button(
            self.frame1,
            text="💾 Save Report As...",
            command=self.on_save_report,
            state='disabled'
        )
        self.save_button.pack(pady=5, padx=5, fill='x')
    
    def create_template_management_buttons(self):
        """Buttons for template management"""
        ttk.Separator(self.frame1, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(self.frame1, text="Template Management:", font=('Arial', 9)).pack(pady=(5, 2))
        
        btn_frame = ttk.Frame(self.frame1)
        btn_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(
            btn_frame,
            text="➕ Create Template",
            command=self.open_template_builder
        ).pack(fill='x', pady=2)
        
        ttk.Button(
            btn_frame,
            text="✏️ Edit Template",
            command=self.edit_selected_template
        ).pack(fill='x', pady=2)
        
        ttk.Button(
            btn_frame,
            text="🗑️ Delete Template",
            command=self.delete_selected_template
        ).pack(fill='x', pady=2)
    
    def on_save_report(self):
        """Logic to save the report to a different location"""
        if not self.generated_report_path or not os.path.exists(self.generated_report_path):
            messagebox.showerror("Error", "No report available to save. Please generate a report first.")
            return
        
        save_path = filedialog.asksaveasfilename(
            title="Save Report As",
            defaultextension=".pptx",
            filetypes=[("PowerPoint files", "*.pptx"), ("All files", "*.*")],
            initialfile="report.pptx"
        )
        
        if save_path:
            try:
                # Copy the generated report to the new location
                import shutil
                shutil.copy2(self.generated_report_path, save_path)
                messagebox.showinfo("Success", f"Report saved to:\n{save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save report:\n{str(e)}")
    
    def open_template_builder(self):
        """Open the template builder window"""
        try:
            from template_builder_gui import TemplateBuilderGUI
            builder_window = tk.Toplevel(self.root)
            TemplateBuilderGUI(builder_window)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open template builder:\n{str(e)}")
    
    def edit_selected_template(self):
        """Edit the currently selected template"""
        if not self.selected_template:
            messagebox.showwarning("No Template", "Please select a template to edit.")
            return
        
        # TODO: Implement template editing
        messagebox.showinfo("Coming Soon", "Template editing will be implemented soon.")
    
    def delete_selected_template(self):
        """Delete the currently selected template"""
        if not self.selected_template:
            messagebox.showwarning("No Template", "Please select a template to delete.")
            return
        
        # Get template info
        selected = self.template_combobox.get()
        if selected in self.templates_data:
            template_data = self.templates_data[selected]
            
            # Confirm deletion
            confirm = messagebox.askyesno(
                "Confirm Deletion",
                f"Are you sure you want to delete template:\n\n{template_data['name']} ({template_data['client']})\n\nThis cannot be undone."
            )
            
            if confirm:
                try:
                    success = self.template_manager.delete_template(template_data['template_id'])
                    if success:
                        messagebox.showinfo("Success", "Template deleted successfully.")
                        self.refresh_templates()
                    else:
                        messagebox.showerror("Error", "Failed to delete template.")
                except Exception as e:
                    messagebox.showerror("Error", f"Error deleting template:\n{str(e)}")
            
    def create_report_preview(self):
        """Area to preview the report."""
        self.preview_text = tk.Text(
            self.frame2,
            height=35,
            width=60,
            state="disabled",
            wrap=tk.WORD,
            font=('Consolas', 9)
        )
        self.preview_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Initial message
        self.update_preview(
            "Welcome to ReportForge!\n\n"
            "Steps to generate a report:\n"
            "1. Select a template or use direct mode\n"
            "2. Choose your Excel data file\n"
            "3. (Optional) Enter a custom report name\n"
            "4. Click 'Generate Report'\n\n"
            "You can also create custom templates using the Template Builder."
        )
    
    def update_preview(self, content):
        """Update the preview area with content."""
        self.preview_text.config(state="normal")
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(tk.END, content)
        self.preview_text.config(state="disabled")


def main():
    root = tk.Tk()
    
    # Set theme (optional - requires ttkthemes package)
    try:
        style = ttk.Style()
        style.theme_use('clam')  # Try: vista, xpnative, clam, alt, default
    except:
        pass
    
    app = PPTReportGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()