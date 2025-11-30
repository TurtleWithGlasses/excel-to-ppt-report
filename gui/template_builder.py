"""
ReportForge - Template Builder Interface
Advanced interface for creating and editing report templates
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QFileDialog, QComboBox, QListWidget, QSplitter,
    QGraphicsView, QGraphicsScene, QFrame, QScrollArea, QCheckBox,
    QSpinBox, QColorDialog, QMessageBox, QDialog, QDialogButtonBox,
    QGroupBox, QFormLayout, QListWidgetItem
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPainter, QPixmap, QIcon
import json
from datetime import datetime


class ComponentWidget(QWidget):
    """Draggable component widget for component library"""
    def __init__(self, component_type, icon_text, tooltip):
        super().__init__()
        self.component_type = component_type
        self.setToolTip(tooltip)
        self.setup_ui(icon_text)

    def setup_ui(self, icon_text):
        """Setup component widget UI"""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Icon (emoji or text)
        icon_label = QLabel(icon_text)
        icon_label.setFont(QFont("Segoe UI", 24))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)

        # Type label
        type_label = QLabel(self.component_type)
        type_label.setFont(QFont("Segoe UI", 9))
        type_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(type_label)

        self.setFixedSize(100, 100)
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 2px solid #E5E7EB;
                border-radius: 8px;
            }
            QWidget:hover {
                background-color: #F3F4F6;
                border: 2px solid #2563EB;
            }
        """)


class TemplateBuilder(QMainWindow):
    """Template Builder - Create and edit report templates"""

    def __init__(self):
        super().__init__()
        self.template_data = {
            'name': '',
            'industry': '',
            'logo_path': None,
            'colors': {
                'primary': '#2563EB',
                'secondary': '#10B981',
                'accent': '#F59E0B'
            },
            'font_family': 'Segoe UI',
            'slides': []
        }
        self.current_slide_index = -1
        self.init_ui()

    def init_ui(self):
        """Initialize user interface"""
        # Start in full-screen mode
        self.showMaximized()
        self.setMinimumSize(1200, 700)

        # Create central widget with splitter
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Add header
        self._create_header(main_layout)

        # Create horizontal layout for 3-panel splitter
        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(0, 0, 0, 0)

        # Create 3-panel splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left panel: Template Settings
        left_panel = self._create_left_panel()
        splitter.addWidget(left_panel)

        # Center panel: Slide Preview
        center_panel = self._create_center_panel()
        splitter.addWidget(center_panel)

        # Right panel: Components Library
        right_panel = self._create_right_panel()
        splitter.addWidget(right_panel)

        # Set initial sizes (30%, 40%, 30%)
        splitter.setSizes([420, 560, 420])

        h_layout.addWidget(splitter)
        main_layout.addLayout(h_layout)

    def _create_header(self, layout):
        """Create header with title and navigation buttons"""
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: #1F2937; padding: 10px;")
        header_frame.setFixedHeight(60)

        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 10, 20, 10)

        # Title
        title = QLabel("🛠️ ReportForge - Template Builder")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        header_layout.addWidget(title)

        header_layout.addStretch()

        # Back to Main App button
        back_btn = QPushButton("← Back to Main App")
        back_btn.setFont(QFont("Segoe UI", 11))
        back_btn.setFixedHeight(35)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
        """)
        back_btn.clicked.connect(self.back_to_main_app)
        header_layout.addWidget(back_btn)

        layout.addWidget(header_frame)

    def _create_left_panel(self):
        """Create left panel with template settings"""
        panel = QFrame()
        panel.setStyleSheet("background-color: #F9FAFB;")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Title
        title = QLabel("TEMPLATE SETTINGS")
        title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        layout.addWidget(title)

        # Scroll area for settings
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Template Info Section
        info_group = self._create_template_info_section()
        scroll_layout.addWidget(info_group)

        # Brand Colors Section
        colors_group = self._create_brand_colors_section()
        scroll_layout.addWidget(colors_group)

        # Typography Section
        typography_group = self._create_typography_section()
        scroll_layout.addWidget(typography_group)

        # Slide Structure Section
        slides_group = self._create_slide_structure_section()
        scroll_layout.addWidget(slides_group)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        # Action Buttons
        self._create_action_buttons(layout)

        return panel

    def _create_template_info_section(self):
        """Create template information section"""
        group = QGroupBox("Template Info")
        group.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        layout = QFormLayout(group)

        # Template Name
        self.template_name_input = QLineEdit()
        self.template_name_input.setPlaceholderText("e.g., BSH Monthly Media Report")
        layout.addRow("Template Name:", self.template_name_input)

        # Industry
        self.industry_combo = QComboBox()
        self.industry_combo.addItems([
            "Fashion & Retail",
            "Pharmaceutical",
            "Energy & Utilities",
            "Banking & Finance",
            "Technology",
            "FMCG",
            "Custom / Other"
        ])
        layout.addRow("Industry:", self.industry_combo)

        # Logo
        logo_layout = QHBoxLayout()
        self.logo_path_label = QLabel("No logo selected")
        self.logo_path_label.setStyleSheet("color: #6B7280;")
        logo_layout.addWidget(self.logo_path_label)

        logo_btn = QPushButton("Browse...")
        logo_btn.clicked.connect(self.select_logo)
        logo_layout.addWidget(logo_btn)

        layout.addRow("Logo:", logo_layout)

        return group

    def _create_brand_colors_section(self):
        """Create brand colors section"""
        group = QGroupBox("Brand Colors")
        group.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        layout = QFormLayout(group)

        # Primary Color
        primary_layout = QHBoxLayout()
        self.primary_color_btn = QPushButton("■")
        self.primary_color_btn.setFixedSize(40, 30)
        self.primary_color_btn.setStyleSheet(f"background-color: {self.template_data['colors']['primary']};")
        self.primary_color_btn.clicked.connect(lambda: self.pick_color('primary'))
        primary_layout.addWidget(self.primary_color_btn)

        self.primary_color_label = QLabel(self.template_data['colors']['primary'])
        primary_layout.addWidget(self.primary_color_label)
        primary_layout.addStretch()

        layout.addRow("Primary:", primary_layout)

        # Secondary Color
        secondary_layout = QHBoxLayout()
        self.secondary_color_btn = QPushButton("■")
        self.secondary_color_btn.setFixedSize(40, 30)
        self.secondary_color_btn.setStyleSheet(f"background-color: {self.template_data['colors']['secondary']};")
        self.secondary_color_btn.clicked.connect(lambda: self.pick_color('secondary'))
        secondary_layout.addWidget(self.secondary_color_btn)

        self.secondary_color_label = QLabel(self.template_data['colors']['secondary'])
        secondary_layout.addWidget(self.secondary_color_label)
        secondary_layout.addStretch()

        layout.addRow("Secondary:", secondary_layout)

        # Accent Color
        accent_layout = QHBoxLayout()
        self.accent_color_btn = QPushButton("■")
        self.accent_color_btn.setFixedSize(40, 30)
        self.accent_color_btn.setStyleSheet(f"background-color: {self.template_data['colors']['accent']};")
        self.accent_color_btn.clicked.connect(lambda: self.pick_color('accent'))
        accent_layout.addWidget(self.accent_color_btn)

        self.accent_color_label = QLabel(self.template_data['colors']['accent'])
        accent_layout.addWidget(self.accent_color_label)
        accent_layout.addStretch()

        layout.addRow("Accent:", accent_layout)

        return group

    def _create_typography_section(self):
        """Create typography section"""
        group = QGroupBox("Typography")
        group.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        layout = QFormLayout(group)

        # Font Family
        self.font_combo = QComboBox()
        self.font_combo.addItems([
            "Segoe UI",
            "Calibri",
            "Arial",
            "Times New Roman",
            "Helvetica"
        ])
        layout.addRow("Font Family:", self.font_combo)

        return group

    def _create_slide_structure_section(self):
        """Create slide structure section"""
        group = QGroupBox("Slide Structure")
        group.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        layout = QVBoxLayout(group)

        # Slide list
        self.slide_list = QListWidget()
        self.slide_list.setMaximumHeight(200)
        self.slide_list.currentRowChanged.connect(self.slide_selected)
        layout.addWidget(self.slide_list)

        # Slide management buttons
        btn_layout = QHBoxLayout()

        add_slide_btn = QPushButton("+ Add Slide")
        add_slide_btn.clicked.connect(self.add_slide)
        btn_layout.addWidget(add_slide_btn)

        remove_slide_btn = QPushButton("- Remove")
        remove_slide_btn.clicked.connect(self.remove_slide)
        btn_layout.addWidget(remove_slide_btn)

        layout.addLayout(btn_layout)

        # Reorder buttons
        reorder_layout = QHBoxLayout()
        move_up_btn = QPushButton("↑")
        move_up_btn.setFixedWidth(40)
        move_up_btn.clicked.connect(self.move_slide_up)
        reorder_layout.addWidget(move_up_btn)

        move_down_btn = QPushButton("↓")
        move_down_btn.setFixedWidth(40)
        move_down_btn.clicked.connect(self.move_slide_down)
        reorder_layout.addWidget(move_down_btn)

        reorder_layout.addStretch()
        layout.addLayout(reorder_layout)

        return group

    def _create_action_buttons(self, layout):
        """Create action buttons"""
        layout.addWidget(self._create_separator())

        save_btn = QPushButton("Save Template")
        save_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
        """)
        save_btn.clicked.connect(self.save_template)
        layout.addWidget(save_btn)

        load_btn = QPushButton("Load Template")
        load_btn.setFont(QFont("Segoe UI", 10))
        load_btn.clicked.connect(self.load_template)
        layout.addWidget(load_btn)

        export_btn = QPushButton("Export as JSON")
        export_btn.setFont(QFont("Segoe UI", 10))
        export_btn.clicked.connect(self.export_template)
        layout.addWidget(export_btn)

    def _create_center_panel(self):
        """Create center panel with slide preview"""
        panel = QFrame()
        panel.setStyleSheet("background-color: white;")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(15, 15, 15, 15)

        # Title
        title = QLabel("SLIDE PREVIEW")
        title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Preview canvas
        self.preview_view = QGraphicsView()
        self.preview_scene = QGraphicsScene()
        self.preview_view.setScene(self.preview_scene)
        self.preview_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.preview_view.setStyleSheet("""
            QGraphicsView {
                border: 2px solid #E5E7EB;
                border-radius: 8px;
                background-color: #F9FAFB;
            }
        """)

        # Set scene size (PowerPoint slide dimensions)
        self.preview_scene.setSceneRect(0, 0, 720, 540)
        self.show_preview_placeholder()

        layout.addWidget(self.preview_view)

        # Slide counter and navigation
        nav_layout = QHBoxLayout()

        self.slide_counter_label = QLabel("Slide ... of ...")
        self.slide_counter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nav_layout.addWidget(self.slide_counter_label)

        prev_btn = QPushButton("◄ Previous")
        prev_btn.clicked.connect(self.previous_slide_preview)
        nav_layout.addWidget(prev_btn)

        next_btn = QPushButton("Next ►")
        next_btn.clicked.connect(self.next_slide_preview)
        nav_layout.addWidget(next_btn)

        layout.addLayout(nav_layout)

        return panel

    def _create_right_panel(self):
        """Create right panel with components library"""
        panel = QFrame()
        panel.setStyleSheet("background-color: #F9FAFB;")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(15, 15, 15, 15)

        # Title
        title = QLabel("COMPONENTS LIBRARY")
        title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        layout.addWidget(title)

        # Instructions
        instructions = QLabel("Drag components to add to slide:")
        instructions.setFont(QFont("Segoe UI", 9))
        instructions.setStyleSheet("color: #6B7280;")
        layout.addWidget(instructions)

        # Component palette
        components_layout = QHBoxLayout()
        components_layout.setSpacing(10)

        # Table Component
        table_widget = ComponentWidget("Table", "📊", "Data table for structured information")
        components_layout.addWidget(table_widget)

        # Chart Component
        chart_widget = ComponentWidget("Chart", "📈", "Visualizations (bar, column, pie, line)")
        components_layout.addWidget(chart_widget)

        # Text Component
        text_widget = ComponentWidget("Text", "📝", "Titles, headings, paragraphs")
        components_layout.addWidget(text_widget)

        # Image Component
        image_widget = ComponentWidget("Image", "🖼️", "Logos, photos, graphics")
        components_layout.addWidget(image_widget)

        # Summary Component
        summary_widget = ComponentWidget("Summary", "💡", "Auto-generated insights from data")
        components_layout.addWidget(summary_widget)

        layout.addLayout(components_layout)

        layout.addWidget(self._create_separator())

        # Component configuration area
        config_label = QLabel("SELECTED COMPONENT")
        config_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        layout.addWidget(config_label)

        # Scroll area for component configuration
        self.config_scroll = QScrollArea()
        self.config_scroll.setWidgetResizable(True)
        self.config_scroll.setFrameShape(QFrame.Shape.NoFrame)

        self.config_widget = QWidget()
        self.config_layout = QVBoxLayout(self.config_widget)

        placeholder = QLabel("Select a component to configure")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("color: #9CA3AF; padding: 20px;")
        self.config_layout.addWidget(placeholder)

        self.config_scroll.setWidget(self.config_widget)
        layout.addWidget(self.config_scroll)

        return panel

    def _create_separator(self):
        """Create horizontal separator"""
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("background-color: #E5E7EB;")
        return line

    def show_preview_placeholder(self):
        """Show placeholder in preview"""
        self.preview_scene.clear()
        text = self.preview_scene.addText(
            "Select a slide to preview\n\nOr add a new slide to get started",
            QFont("Segoe UI", 14)
        )
        text.setDefaultTextColor(QColor("#9CA3AF"))
        text_rect = text.boundingRect()
        text.setPos(360 - text_rect.width()/2, 270 - text_rect.height()/2)

    # Template Settings Methods
    def select_logo(self):
        """Select logo file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Logo",
            "",
            "Image Files (*.png *.jpg *.svg);;All Files (*.*)"
        )
        if file_path:
            self.template_data['logo_path'] = file_path
            import os
            self.logo_path_label.setText(os.path.basename(file_path))
            self.logo_path_label.setStyleSheet("color: #10B981; font-weight: bold;")

    def pick_color(self, color_type):
        """Pick color for template"""
        current_color = QColor(self.template_data['colors'][color_type])
        color = QColorDialog.getColor(current_color, self, f"Select {color_type.title()} Color")

        if color.isValid():
            hex_color = color.name()
            self.template_data['colors'][color_type] = hex_color

            # Update button and label
            if color_type == 'primary':
                self.primary_color_btn.setStyleSheet(f"background-color: {hex_color};")
                self.primary_color_label.setText(hex_color)
            elif color_type == 'secondary':
                self.secondary_color_btn.setStyleSheet(f"background-color: {hex_color};")
                self.secondary_color_label.setText(hex_color)
            elif color_type == 'accent':
                self.accent_color_btn.setStyleSheet(f"background-color: {hex_color};")
                self.accent_color_label.setText(hex_color)

    # Slide Management Methods
    def add_slide(self):
        """Add new slide"""
        # Create dialog for slide type selection
        dialog = QDialog(self)
        dialog.setWindowTitle("Add New Slide")
        dialog.setMinimumWidth(400)

        layout = QVBoxLayout(dialog)

        label = QLabel("Slide Type:")
        label.setFont(QFont("Segoe UI", 11))
        layout.addWidget(label)

        type_combo = QComboBox()
        type_combo.addItems([
            "Blank Slide",
            "Title Slide",
            "Table Slide",
            "Chart Slide",
            "Mixed Content (Table + Chart)",
            "Summary/Insights Slide"
        ])
        layout.addWidget(type_combo)

        name_label = QLabel("Slide Name:")
        layout.addWidget(name_label)

        name_input = QLineEdit()
        name_input.setPlaceholderText("e.g., Executive Summary")
        layout.addWidget(name_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            slide_type = type_combo.currentText()
            slide_name = name_input.text() or f"Slide {len(self.template_data['slides']) + 1}"

            slide_data = {
                'name': slide_name,
                'type': slide_type,
                'components': []
            }

            self.template_data['slides'].append(slide_data)
            self.slide_list.addItem(f"{len(self.template_data['slides'])}. {slide_name}")

    def remove_slide(self):
        """Remove selected slide"""
        current_row = self.slide_list.currentRow()
        if current_row >= 0:
            reply = QMessageBox.question(
                self,
                "Remove Slide",
                f"Remove slide: {self.template_data['slides'][current_row]['name']}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                del self.template_data['slides'][current_row]
                self.slide_list.takeItem(current_row)
                self.update_slide_numbers()

    def move_slide_up(self):
        """Move slide up in order"""
        current_row = self.slide_list.currentRow()
        if current_row > 0:
            # Swap in data
            self.template_data['slides'][current_row], self.template_data['slides'][current_row - 1] = \
                self.template_data['slides'][current_row - 1], self.template_data['slides'][current_row]

            # Swap in list
            item = self.slide_list.takeItem(current_row)
            self.slide_list.insertItem(current_row - 1, item)
            self.slide_list.setCurrentRow(current_row - 1)
            self.update_slide_numbers()

    def move_slide_down(self):
        """Move slide down in order"""
        current_row = self.slide_list.currentRow()
        if current_row >= 0 and current_row < self.slide_list.count() - 1:
            # Swap in data
            self.template_data['slides'][current_row], self.template_data['slides'][current_row + 1] = \
                self.template_data['slides'][current_row + 1], self.template_data['slides'][current_row]

            # Swap in list
            item = self.slide_list.takeItem(current_row)
            self.slide_list.insertItem(current_row + 1, item)
            self.slide_list.setCurrentRow(current_row + 1)
            self.update_slide_numbers()

    def update_slide_numbers(self):
        """Update slide numbers in list"""
        for i in range(self.slide_list.count()):
            item = self.slide_list.item(i)
            slide_name = self.template_data['slides'][i]['name']
            item.setText(f"{i + 1}. {slide_name}")

    def slide_selected(self, index):
        """Handle slide selection"""
        if 0 <= index < len(self.template_data['slides']):
            self.current_slide_index = index
            self.update_preview()

    def update_preview(self):
        """Update slide preview"""
        if self.current_slide_index >= 0:
            slide = self.template_data['slides'][self.current_slide_index]
            self.slide_counter_label.setText(
                f"Slide {self.current_slide_index + 1} of {len(self.template_data['slides'])}"
            )

            # TODO: Render actual slide with components
            self.preview_scene.clear()
            text = self.preview_scene.addText(
                f"{slide['name']}\nType: {slide['type']}\n\n"
                f"Components: {len(slide['components'])}",
                QFont("Segoe UI", 14)
            )
            text_rect = text.boundingRect()
            text.setPos(360 - text_rect.width()/2, 270 - text_rect.height()/2)

    def previous_slide_preview(self):
        """Navigate to previous slide"""
        if self.current_slide_index > 0:
            self.slide_list.setCurrentRow(self.current_slide_index - 1)

    def next_slide_preview(self):
        """Navigate to next slide"""
        if self.current_slide_index < len(self.template_data['slides']) - 1:
            self.slide_list.setCurrentRow(self.current_slide_index + 1)

    # Template Actions
    def save_template(self):
        """Save template to JSON file"""
        # Update template data from UI
        self.template_data['name'] = self.template_name_input.text()
        self.template_data['industry'] = self.industry_combo.currentText()
        self.template_data['font_family'] = self.font_combo.currentText()

        if not self.template_data['name']:
            QMessageBox.warning(self, "No Template Name", "Please enter a template name!")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Template",
            f"{self.template_data['name']}.json",
            "JSON Files (*.json)"
        )

        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.template_data, f, indent=2, ensure_ascii=False)

            QMessageBox.information(
                self,
                "Template Saved",
                f"Template saved successfully to:\n{file_path}"
            )

    def load_template(self):
        """Load template from JSON file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Template",
            "",
            "JSON Files (*.json);;All Files (*.*)"
        )

        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.template_data = json.load(f)

            # Update UI from loaded data
            self.template_name_input.setText(self.template_data.get('name', ''))
            self.industry_combo.setCurrentText(self.template_data.get('industry', ''))

            # Update colors
            for color_type in ['primary', 'secondary', 'accent']:
                color = self.template_data['colors'].get(color_type, '#000000')
                if color_type == 'primary':
                    self.primary_color_btn.setStyleSheet(f"background-color: {color};")
                    self.primary_color_label.setText(color)
                elif color_type == 'secondary':
                    self.secondary_color_btn.setStyleSheet(f"background-color: {color};")
                    self.secondary_color_label.setText(color)
                elif color_type == 'accent':
                    self.accent_color_btn.setStyleSheet(f"background-color: {color};")
                    self.accent_color_label.setText(color)

            # Update font
            self.font_combo.setCurrentText(self.template_data.get('font_family', 'Segoe UI'))

            # Load slides
            self.slide_list.clear()
            for i, slide in enumerate(self.template_data.get('slides', [])):
                self.slide_list.addItem(f"{i + 1}. {slide['name']}")

            QMessageBox.information(
                self,
                "Template Loaded",
                f"Template loaded successfully:\n{self.template_data['name']}"
            )

    def export_template(self):
        """Export template as JSON"""
        self.save_template()  # Same as save for now

    def back_to_main_app(self):
        """Return to Main App"""
        # Check if there are unsaved changes
        if self.template_data['slides']:
            reply = QMessageBox.question(
                self,
                "Unsaved Changes",
                "Do you want to save your template before returning to Main App?",
                QMessageBox.StandardButton.Save |
                QMessageBox.StandardButton.Discard |
                QMessageBox.StandardButton.Cancel
            )

            if reply == QMessageBox.StandardButton.Save:
                self.save_template()
                self.close()
            elif reply == QMessageBox.StandardButton.Discard:
                self.close()
            # If Cancel, do nothing
        else:
            self.close()
