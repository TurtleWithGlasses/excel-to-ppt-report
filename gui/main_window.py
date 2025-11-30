"""
ReportForge - Main Application Window (Report Generator)
Simple 4-step workflow: Import Data → Select Template → Prepare Report → Download
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QFileDialog, QComboBox, QProgressBar,
    QGraphicsView, QGraphicsScene, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt, QRectF, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor, QPixmap, QPainter
import os
from datetime import datetime

# Import core PPTGenerator
try:
    from core import PPTGenerator
    CORE_AVAILABLE = True
except ImportError:
    CORE_AVAILABLE = False
    print("Warning: Core engine not available. Using simulation mode.")


class ReportGeneratorThread(QThread):
    """Background thread for report generation"""
    progress = pyqtSignal(int, str)  # (percentage, message)
    finished = pyqtSignal(bool, str, str)  # (success, message, output_path)

    def __init__(self, excel_path, template_path, output_path, variables):
        super().__init__()
        self.excel_path = excel_path
        self.template_path = template_path
        self.output_path = output_path
        self.variables = variables

    def run(self):
        """Generate report in background"""
        try:
            if CORE_AVAILABLE:
                # Use actual PPTGenerator
                self.progress.emit(10, "Initializing generator...")
                generator = PPTGenerator()

                self.progress.emit(20, "Loading template...")
                generator.load_template(self.template_path)

                self.progress.emit(40, "Loading data...")
                generator.load_data(self.excel_path)

                self.progress.emit(60, "Setting variables...")
                generator.set_variables(self.variables)

                self.progress.emit(80, "Generating PowerPoint...")
                output = generator.generate(self.output_path)

                self.progress.emit(100, "Complete!")
                self.finished.emit(True, "Report generated successfully!", output)
            else:
                # Simulation mode
                for i in range(1, 101, 10):
                    self.progress.emit(i, f"Generating slides... {i}% complete")
                    self.msleep(200)

                self.finished.emit(True, "Report generated (simulation mode)!", self.output_path)

        except Exception as e:
            import traceback
            error_msg = f"Error: {str(e)}\n\n{traceback.format_exc()}"
            self.finished.emit(False, error_msg, "")


class StepButton(QPushButton):
    """Custom button for workflow steps"""
    def __init__(self, step_number, title, description):
        super().__init__()
        self.step_number = step_number
        self.title = title
        self.description = description
        self.completed = False
        self.setup_ui()

    def setup_ui(self):
        """Setup button appearance"""
        self.setFixedHeight(100)
        self.setMinimumWidth(200)
        self.setText(f"{self.step_number}. {self.title}\n{self.description}")
        self.setFont(QFont("Segoe UI", 10))
        self.update_style()

    def mark_completed(self):
        """Mark step as completed"""
        self.completed = True
        self.update_style()

    def mark_active(self):
        """Mark step as active"""
        self.update_style(active=True)

    def update_style(self, active=False):
        """Update button style based on state"""
        if self.completed:
            # Green for completed
            style = """
                QPushButton {
                    background-color: #10B981;
                    color: white;
                    border: 2px solid #059669;
                    border-radius: 8px;
                    padding: 10px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #059669;
                }
            """
        elif active:
            # Blue for active
            style = """
                QPushButton {
                    background-color: #2563EB;
                    color: white;
                    border: 2px solid #1D4ED8;
                    border-radius: 8px;
                    padding: 10px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #1D4ED8;
                }
            """
        else:
            # Gray for pending
            style = """
                QPushButton {
                    background-color: #F9FAFB;
                    color: #6B7280;
                    border: 2px solid #E5E7EB;
                    border-radius: 8px;
                    padding: 10px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #F3F4F6;
                }
            """
        self.setStyleSheet(style)


class MainWindow(QMainWindow):
    """Main Application Window - Report Generator"""

    def __init__(self):
        super().__init__()
        self.excel_path = None
        self.template_name = None
        self.template_path = None
        self.generated_slides = []
        self.current_slide_index = 0

        # Map template names to file paths
        self.template_map = {
            "BSH Monthly Media Report": "templates/configs/BSH_Template.json",
            "Sanofi Pharma Media Report": "templates/configs/Sanofi_Template.json",
            "SOCAR Energy Sector Template": "templates/configs/SOCAR_Template.json"
        }

        self.init_ui()

    def init_ui(self):
        """Initialize user interface"""
        # Start in full-screen mode
        self.showMaximized()
        self.setMinimumSize(1024, 768)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Add header with Template Builder button
        self._create_header(main_layout)

        # Add components
        self._create_progress_steps(main_layout)
        self._create_separator(main_layout)
        self._create_report_name_field(main_layout)
        self._create_slide_preview(main_layout)
        self._create_slide_controls(main_layout)

    def _create_header(self, layout):
        """Create header with app title and Template Builder button"""
        header_layout = QHBoxLayout()

        # App title
        title = QLabel("📊 ReportForge - Report Generator")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #1F2937;")
        header_layout.addWidget(title)

        header_layout.addStretch()

        # Template Builder button
        template_builder_btn = QPushButton("🛠️ Create/Edit Templates")
        template_builder_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        template_builder_btn.setFixedHeight(40)
        template_builder_btn.setStyleSheet("""
            QPushButton {
                background-color: #F59E0B;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #D97706;
            }
        """)
        template_builder_btn.clicked.connect(self.open_template_builder)
        header_layout.addWidget(template_builder_btn)

        layout.addLayout(header_layout)

    def _create_progress_steps(self, layout):
        """Create 4-step progress workflow"""
        steps_layout = QHBoxLayout()
        steps_layout.setSpacing(10)

        # Step 1: Import Data
        self.step1_btn = StepButton(1, "Import Data", "Users will import\nexcel files")
        self.step1_btn.clicked.connect(self.import_data)
        steps_layout.addWidget(self.step1_btn)

        # Arrow
        arrow1 = QLabel("→")
        arrow1.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        arrow1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        steps_layout.addWidget(arrow1)

        # Step 2: Select Template
        self.step2_btn = StepButton(2, "Select Template", "Users will select\ntemplate")
        self.step2_btn.clicked.connect(self.select_template)
        steps_layout.addWidget(self.step2_btn)

        # Arrow
        arrow2 = QLabel("→")
        arrow2.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        arrow2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        steps_layout.addWidget(arrow2)

        # Step 3: Prepare Report
        self.step3_btn = StepButton(3, "Prepare Report", "Report will be prepared\nby excel importation")
        self.step3_btn.clicked.connect(self.prepare_report)
        steps_layout.addWidget(self.step3_btn)

        # Arrow
        arrow3 = QLabel("→")
        arrow3.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        arrow3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        steps_layout.addWidget(arrow3)

        # Step 4: Download Report
        self.step4_btn = StepButton(4, "Download Report", "Report will be downloaded\non local file")
        self.step4_btn.clicked.connect(self.download_report)
        steps_layout.addWidget(self.step4_btn)

        layout.addLayout(steps_layout)

        # Progress bar (hidden initially)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(True)
        layout.addWidget(self.progress_bar)

    def _create_separator(self, layout):
        """Create horizontal separator line"""
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("background-color: #E5E7EB;")
        layout.addWidget(line)

    def _create_report_name_field(self, layout):
        """Create report name input field"""
        name_layout = QHBoxLayout()

        label = QLabel("Report name:")
        label.setFont(QFont("Segoe UI", 11))
        name_layout.addWidget(label)

        self.report_name_input = QLineEdit()
        self.report_name_input.setPlaceholderText("Enter report name...")
        self.report_name_input.setText(f"Report_{datetime.now().strftime('%Y%m%d')}")
        self.report_name_input.setFont(QFont("Segoe UI", 11))
        self.report_name_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #E5E7EB;
                border-radius: 4px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #2563EB;
            }
        """)
        name_layout.addWidget(self.report_name_input)

        layout.addLayout(name_layout)

    def _create_slide_preview(self, layout):
        """Create slide preview area"""
        # Preview container
        preview_frame = QFrame()
        preview_frame.setFrameShape(QFrame.Shape.Box)
        preview_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #E5E7EB;
                border-radius: 8px;
            }
        """)
        preview_layout = QVBoxLayout(preview_frame)

        # Slide counter
        self.slide_counter = QLabel("Slide ... of ...")
        self.slide_counter.setFont(QFont("Segoe UI", 10))
        self.slide_counter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_layout.addWidget(self.slide_counter)

        # Graphics view for slide preview
        self.slide_view = QGraphicsView()
        self.slide_scene = QGraphicsScene()
        self.slide_view.setScene(self.slide_scene)
        self.slide_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.slide_view.setStyleSheet("border: none; background-color: #F9FAFB;")

        # Show placeholder message
        self.show_placeholder_message()

        preview_layout.addWidget(self.slide_view)
        layout.addWidget(preview_frame)

    def _create_slide_controls(self, layout):
        """Create slide navigation and editing controls"""
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)

        # Previous button
        self.prev_btn = QPushButton("◄ Previous")
        self.prev_btn.setFont(QFont("Segoe UI", 10))
        self.prev_btn.setEnabled(False)
        self.prev_btn.clicked.connect(self.previous_slide)
        self.prev_btn.setStyleSheet(self._get_button_style())
        controls_layout.addWidget(self.prev_btn)

        # Edit Slide button
        self.edit_btn = QPushButton("Edit Slide")
        self.edit_btn.setFont(QFont("Segoe UI", 10))
        self.edit_btn.setEnabled(False)
        self.edit_btn.clicked.connect(self.edit_slide)
        self.edit_btn.setStyleSheet(self._get_button_style())
        controls_layout.addWidget(self.edit_btn)

        # Delete Slide button
        self.delete_btn = QPushButton("Delete Slide")
        self.delete_btn.setFont(QFont("Segoe UI", 10))
        self.delete_btn.setEnabled(False)
        self.delete_btn.clicked.connect(self.delete_slide)
        self.delete_btn.setStyleSheet(self._get_button_style("#EF4444", "#DC2626"))
        controls_layout.addWidget(self.delete_btn)

        # Add Slide button
        self.add_btn = QPushButton("Add Slide")
        self.add_btn.setFont(QFont("Segoe UI", 10))
        self.add_btn.setEnabled(False)
        self.add_btn.clicked.connect(self.add_slide)
        self.add_btn.setStyleSheet(self._get_button_style("#10B981", "#059669"))
        controls_layout.addWidget(self.add_btn)

        # Next button
        self.next_btn = QPushButton("Next ►")
        self.next_btn.setFont(QFont("Segoe UI", 10))
        self.next_btn.setEnabled(False)
        self.next_btn.clicked.connect(self.next_slide)
        self.next_btn.setStyleSheet(self._get_button_style())
        controls_layout.addWidget(self.next_btn)

        layout.addLayout(controls_layout)

    def _get_button_style(self, bg_color="#2563EB", hover_color="#1D4ED8"):
        """Get button stylesheet"""
        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:disabled {{
                background-color: #D1D5DB;
                color: #9CA3AF;
            }}
        """

    def show_placeholder_message(self):
        """Show placeholder message in slide preview"""
        self.slide_scene.clear()
        text = self.slide_scene.addText(
            "After the report is prepared,\nthe slides will be shown here\n"
            "page by page. The user will be\nable to edit the pages too.",
            QFont("Segoe UI", 14)
        )
        text.setDefaultTextColor(QColor("#EF4444"))
        text_rect = text.boundingRect()
        text.setPos(-text_rect.width()/2, -text_rect.height()/2)

    # Step 1: Import Data
    def import_data(self):
        """Import Excel file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Excel File",
            "",
            "Excel Files (*.xlsx *.xls);;All Files (*.*)"
        )

        if file_path:
            self.excel_path = file_path
            self.step1_btn.mark_completed()
            self.step2_btn.mark_active()
            QMessageBox.information(
                self,
                "File Imported",
                f"Successfully imported:\n{os.path.basename(file_path)}"
            )

    # Step 2: Select Template
    def select_template(self):
        """Select report template"""
        if not self.excel_path:
            QMessageBox.warning(self, "No Data", "Please import Excel file first!")
            return

        # Create template selection dialog
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox

        dialog = QDialog(self)
        dialog.setWindowTitle("Select Template")
        dialog.setMinimumWidth(400)

        layout = QVBoxLayout(dialog)

        label = QLabel("Choose a template:")
        label.setFont(QFont("Segoe UI", 11))
        layout.addWidget(label)

        template_combo = QComboBox()
        template_combo.setFont(QFont("Segoe UI", 10))
        template_combo.addItems([
            "--- Fashion & Retail ---",
            "BSH Monthly Media Report",
            "LC Waikiki Monthly Report",
            "--- Pharmaceutical ---",
            "Sanofi Pharma Media Report",
            "--- Energy Sector ---",
            "SOCAR Energy Sector Template",
            "--- Financial ---",
            "Financial Quarterly Report",
            "--- Custom ---",
            "Create New Template..."
        ])
        layout.addWidget(template_combo)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.template_name = template_combo.currentText()
            if self.template_name == "Create New Template...":
                # Open Template Builder
                reply = QMessageBox.question(
                    self,
                    "Template Builder",
                    "Open Template Builder to create a new template?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.Yes:
                    self.open_template_builder()
            elif self.template_name.startswith("---"):
                # Category header, ignore
                QMessageBox.information(self, "Category", "Please select an actual template, not a category header.")
                return
            else:
                # Map template name to path
                self.template_path = self.template_map.get(self.template_name)

                if not self.template_path or not os.path.exists(self.template_path):
                    QMessageBox.warning(
                        self,
                        "Template Not Found",
                        f"Template file not found for:\n{self.template_name}\n\nPlease select a valid template."
                    )
                    return

                self.step2_btn.mark_completed()
                self.step3_btn.mark_active()
                QMessageBox.information(
                    self,
                    "Template Selected",
                    f"Selected template:\n{self.template_name}\n\nPath: {self.template_path}"
                )

    # Step 3: Prepare Report
    def prepare_report(self):
        """Generate PowerPoint report"""
        if not self.excel_path or not self.template_path:
            QMessageBox.warning(
                self,
                "Missing Information",
                "Please complete Steps 1 and 2 first!"
            )
            return

        report_name = self.report_name_input.text()
        if not report_name:
            QMessageBox.warning(self, "No Report Name", "Please enter a report name!")
            return

        # Create output directory if it doesn't exist
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        # Generate output path
        output_path = os.path.join(output_dir, f"{report_name}.pptx")

        # Prepare variables for text substitution
        from datetime import datetime
        now = datetime.now()
        variables = {
            'month': now.strftime('%B'),  # Full month name
            'year': now.strftime('%Y'),
            'date': now.strftime('%Y-%m-%d'),
            'report_name': report_name
        }

        # Show progress bar
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        # Start generation thread
        self.generator_thread = ReportGeneratorThread(
            self.excel_path,
            self.template_path,
            output_path,
            variables
        )
        self.generator_thread.progress.connect(self.update_progress)
        self.generator_thread.finished.connect(self.generation_finished)
        self.generator_thread.start()

    def update_progress(self, percentage, message):
        """Update progress bar"""
        self.progress_bar.setValue(percentage)
        self.progress_bar.setFormat(message)

    def generation_finished(self, success, message, output_path):
        """Handle report generation completion"""
        self.progress_bar.setVisible(False)

        if success:
            # Store the output path
            self.output_path = output_path

            # Simulate generated slides (for preview - in real implementation, could load from PPTX)
            self.generated_slides = [f"Slide {i}" for i in range(1, 56)]
            self.current_slide_index = 0

            # Update UI
            self.step3_btn.mark_completed()
            self.step4_btn.mark_active()
            self.show_slide(0)
            self.enable_slide_controls(True)

            # Show success message with file location
            QMessageBox.information(
                self,
                "Success",
                f"{message}\n\nFile saved to:\n{output_path}"
            )
        else:
            QMessageBox.critical(self, "Error", message)

    def show_slide(self, index):
        """Display slide at given index"""
        if 0 <= index < len(self.generated_slides):
            self.current_slide_index = index
            self.slide_counter.setText(
                f"Slide {index + 1} of {len(self.generated_slides)}"
            )

            # TODO: Render actual slide content
            self.slide_scene.clear()
            text = self.slide_scene.addText(
                f"{self.generated_slides[index]}\n\n"
                f"[Preview of slide content will appear here]",
                QFont("Segoe UI", 16)
            )
            text_rect = text.boundingRect()
            text.setPos(-text_rect.width()/2, -text_rect.height()/2)

            # Update navigation buttons
            self.prev_btn.setEnabled(index > 0)
            self.next_btn.setEnabled(index < len(self.generated_slides) - 1)

    def enable_slide_controls(self, enabled):
        """Enable/disable slide control buttons"""
        self.edit_btn.setEnabled(enabled)
        self.delete_btn.setEnabled(enabled)
        self.add_btn.setEnabled(enabled)

    def previous_slide(self):
        """Navigate to previous slide"""
        self.show_slide(self.current_slide_index - 1)

    def next_slide(self):
        """Navigate to next slide"""
        self.show_slide(self.current_slide_index + 1)

    def edit_slide(self):
        """Edit current slide"""
        QMessageBox.information(
            self,
            "Edit Slide",
            f"Editing slide {self.current_slide_index + 1}\n\n"
            "Slide editing functionality will be implemented here."
        )

    def delete_slide(self):
        """Delete current slide"""
        reply = QMessageBox.question(
            self,
            "Delete Slide",
            f"Are you sure you want to delete slide {self.current_slide_index + 1}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            del self.generated_slides[self.current_slide_index]
            if self.current_slide_index >= len(self.generated_slides):
                self.current_slide_index = len(self.generated_slides) - 1
            if self.generated_slides:
                self.show_slide(self.current_slide_index)
            else:
                self.show_placeholder_message()
                self.enable_slide_controls(False)

    def add_slide(self):
        """Add new slide after current"""
        QMessageBox.information(
            self,
            "Add Slide",
            "Add new slide functionality will be implemented here.\n\n"
            "User can choose from blank slide, table slide, chart slide, etc."
        )

    # Step 4: Download Report
    def download_report(self):
        """Download generated PowerPoint report"""
        if not self.generated_slides:
            QMessageBox.warning(
                self,
                "No Report",
                "Please generate report first (Step 3)!"
            )
            return

        report_name = self.report_name_input.text()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PowerPoint Report",
            f"{report_name}.pptx",
            "PowerPoint Files (*.pptx)"
        )

        if file_path:
            # TODO: Save actual PowerPoint file
            QMessageBox.information(
                self,
                "Download Complete",
                f"Report saved successfully to:\n{file_path}\n\n"
                f"Total slides: {len(self.generated_slides)}"
            )
            self.step4_btn.mark_completed()

    # Template Builder Integration
    def open_template_builder(self):
        """Open Template Builder window"""
        from gui.template_builder import TemplateBuilder

        # Create and show Template Builder window
        self.template_builder_window = TemplateBuilder()
        self.template_builder_window.setWindowTitle("ReportForge - Template Builder")
        self.template_builder_window.show()

        # Optional: Connect signal to refresh templates when builder closes
        self.template_builder_window.destroyed.connect(self.refresh_templates)

    def refresh_templates(self):
        """Refresh template list after Template Builder closes"""
        # TODO: Reload template list from templates/configs/ directory
        pass
