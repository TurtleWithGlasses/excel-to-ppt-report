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

        # Slide list with inline editing
        self.slide_list = QListWidget()
        self.slide_list.setMaximumHeight(200)
        self.slide_list.currentRowChanged.connect(self.slide_selected)
        self.slide_list.itemChanged.connect(self.slide_renamed)
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

        delete_btn = QPushButton("Delete Template")
        delete_btn.setFont(QFont("Segoe UI", 10))
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #DC2626;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #B91C1C;
            }
        """)
        delete_btn.clicked.connect(self.delete_template)
        layout.addWidget(delete_btn)

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

            # Add item with editable flag
            item = QListWidgetItem(f"{len(self.template_data['slides'])}. {slide_name}")
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.slide_list.addItem(item)

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
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)

    def slide_renamed(self, item):
        """Handle slide rename (double-click to edit)"""
        # Get the row index
        row = self.slide_list.row(item)
        if 0 <= row < len(self.template_data['slides']):
            # Extract new name from "1. New Name" format
            new_text = item.text()
            # Remove number prefix "1. " to get just the name
            if '. ' in new_text:
                new_name = new_text.split('. ', 1)[1]
            else:
                new_name = new_text

            # Update template data
            self.template_data['slides'][row]['name'] = new_name

            # Update the item text to ensure proper formatting
            item.setText(f"{row + 1}. {new_name}")

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

            # Build preview text (handle both Template Builder and PPTGenerator formats)
            slide_name = slide.get('name', 'Untitled Slide')
            slide_type = slide.get('type', 'N/A')  # Type only exists in Template Builder format
            slide_layout = slide.get('layout', 'N/A')  # Layout exists in PPTGenerator format
            num_components = len(slide.get('components', []))

            preview_text = f"{slide_name}\n"
            if slide_type != 'N/A':
                preview_text += f"Type: {slide_type}\n"
            if slide_layout != 'N/A':
                preview_text += f"Layout: {slide_layout}\n"
            preview_text += f"\nComponents: {num_components}"

            text = self.preview_scene.addText(preview_text, QFont("Segoe UI", 14))
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
    def validate_template(self):
        """
        Validate template before saving.
        Returns (is_valid, error_message)
        """
        # Check template name
        template_name = self.template_name_input.text().strip()
        if not template_name:
            return False, "Template name is required."

        # Check slides
        if not self.template_data['slides']:
            return False, "At least one slide is required."

        # Validate each slide
        for i, slide in enumerate(self.template_data['slides']):
            slide_num = i + 1

            # Check slide name
            if not slide.get('name'):
                return False, f"Slide {slide_num} is missing a name."

            # Check components
            if not slide.get('components'):
                # Warning but not error - blank slides are allowed
                continue

            # Validate each component
            for j, component in enumerate(slide['components']):
                comp_num = j + 1

                # Check component type
                if 'type' not in component:
                    return False, f"Slide {slide_num}, Component {comp_num}: Missing type."

                # Check position
                if 'position' not in component:
                    return False, f"Slide {slide_num}, Component {comp_num}: Missing position."

                # Check size
                if 'size' not in component:
                    return False, f"Slide {slide_num}, Component {comp_num}: Missing size."

                # Type-specific validation
                comp_type = component['type']

                if comp_type == 'text':
                    if 'content' not in component:
                        return False, f"Slide {slide_num}, Text Component {comp_num}: Missing content."

                elif comp_type == 'table':
                    if 'data_source' not in component or 'sheet_name' not in component.get('data_source', {}):
                        return False, f"Slide {slide_num}, Table Component {comp_num}: Missing data source configuration."

                elif comp_type == 'chart':
                    if 'data_source' not in component:
                        return False, f"Slide {slide_num}, Chart Component {comp_num}: Missing data source."
                    if 'chart_type' not in component:
                        return False, f"Slide {slide_num}, Chart Component {comp_num}: Missing chart type."

        return True, "Template is valid."

    def save_template(self):
        """Save template to JSON file in PPTGenerator format"""
        # Update template data from UI
        template_name = self.template_name_input.text()
        industry = self.industry_combo.currentText()
        font_family = self.font_combo.currentText()

        # Validate template before saving
        is_valid, message = self.validate_template()
        if not is_valid:
            QMessageBox.warning(
                self,
                "Validation Error",
                f"Template validation failed:\n\n{message}\n\nPlease fix the issue and try again."
            )
            return

        # Default save location: templates/configs/
        import os
        default_dir = os.path.join(os.getcwd(), "templates", "configs")
        os.makedirs(default_dir, exist_ok=True)
        default_filename = os.path.join(default_dir, f"{template_name.replace(' ', '_')}_Template.json")

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Template",
            default_filename,
            "JSON Files (*.json)"
        )

        if file_path:
            # Convert to PPTGenerator format
            ppt_template = {
                "metadata": {
                    "name": template_name,
                    "description": f"{industry} report template",
                    "industry": industry,
                    "author": "ReportForge Template Builder",
                    "version": "1.0",
                    "created_date": datetime.now().strftime("%Y-%m-%d"),
                    "modified_date": datetime.now().strftime("%Y-%m-%d")
                },
                "settings": {
                    "page_size": "16:9",
                    "default_font": font_family,
                    "default_font_size": 11,
                    "color_scheme": {
                        "primary": self.template_data['colors']['primary'],
                        "secondary": self.template_data['colors']['secondary'],
                        "accent": self.template_data['colors']['accent'],
                        "negative": "#EF4444",
                        "neutral": "#6B7280",
                        "text": "#1F2937",
                        "background": "#FFFFFF"
                    }
                },
                "slides": self.template_data['slides']
            }

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(ppt_template, f, indent=2, ensure_ascii=False)

            QMessageBox.information(
                self,
                "Template Saved",
                f"Template saved successfully to:\n{file_path}\n\n"
                f"Slides: {len(self.template_data['slides'])}\n"
                f"Format: PPTGenerator JSON"
            )

    def load_template(self):
        """Load template from JSON file (supports PPTGenerator format)"""
        import os
        default_dir = os.path.join(os.getcwd(), "templates", "configs")

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Template",
            default_dir if os.path.exists(default_dir) else "",
            "JSON Files (*.json);;All Files (*.*)"
        )

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)

                # Detect format: PPTGenerator format has "metadata" and "settings" keys
                if 'metadata' in loaded_data and 'settings' in loaded_data:
                    # PPTGenerator format - convert to internal format
                    self.template_data = {
                        'name': loaded_data['metadata'].get('name', ''),
                        'industry': loaded_data['metadata'].get('industry', ''),
                        'logo_path': None,
                        'colors': {
                            'primary': loaded_data['settings']['color_scheme'].get('primary', '#2563EB'),
                            'secondary': loaded_data['settings']['color_scheme'].get('secondary', '#10B981'),
                            'accent': loaded_data['settings']['color_scheme'].get('accent', '#F59E0B')
                        },
                        'font_family': loaded_data['settings'].get('default_font', 'Segoe UI'),
                        'slides': loaded_data.get('slides', [])
                    }
                else:
                    # Simple format (old Template Builder format)
                    self.template_data = loaded_data

                # Update UI from loaded data
                self.template_name_input.setText(self.template_data.get('name', ''))

                # Set industry if it exists in combo box
                industry = self.template_data.get('industry', '')
                index = self.industry_combo.findText(industry)
                if index >= 0:
                    self.industry_combo.setCurrentIndex(index)
                else:
                    self.industry_combo.setCurrentText(industry)

                # Update colors
                colors = self.template_data.get('colors', {})
                for color_type in ['primary', 'secondary', 'accent']:
                    color = colors.get(color_type, '#000000')
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
                font_family = self.template_data.get('font_family', 'Segoe UI')
                index = self.font_combo.findText(font_family)
                if index >= 0:
                    self.font_combo.setCurrentIndex(index)

                # Load slides
                self.slide_list.clear()
                for i, slide in enumerate(self.template_data.get('slides', [])):
                    item = QListWidgetItem(f"{i + 1}. {slide['name']}")
                    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                    self.slide_list.addItem(item)

                # Select first slide if available
                if self.slide_list.count() > 0:
                    self.slide_list.setCurrentRow(0)

                QMessageBox.information(
                    self,
                    "Template Loaded",
                    f"Template loaded successfully!\n\n"
                    f"Name: {self.template_data['name']}\n"
                    f"Industry: {self.template_data.get('industry', 'N/A')}\n"
                    f"Slides: {len(self.template_data.get('slides', []))}"
                )

            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Load Error",
                    f"Failed to load template:\n{str(e)}"
                )

    def delete_template(self):
        """Delete an existing template from templates/configs/"""
        import os

        default_dir = os.path.join(os.getcwd(), "templates", "configs")

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Template to Delete",
            default_dir if os.path.exists(default_dir) else "",
            "JSON Files (*.json);;All Files (*.*)"
        )

        if file_path:
            # Get template name for confirmation
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)

                if 'metadata' in loaded_data:
                    template_name = loaded_data['metadata'].get('name', os.path.basename(file_path))
                else:
                    template_name = loaded_data.get('name', os.path.basename(file_path))
            except Exception:
                template_name = os.path.basename(file_path)

            # Confirm deletion
            reply = QMessageBox.question(
                self,
                "Delete Template",
                f"Are you sure you want to delete this template?\n\n"
                f"Template: {template_name}\n"
                f"File: {os.path.basename(file_path)}\n\n"
                f"This action cannot be undone!",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                try:
                    os.remove(file_path)
                    QMessageBox.information(
                        self,
                        "Template Deleted",
                        f"Template '{template_name}' has been deleted successfully."
                    )

                    # If the deleted template was currently loaded, clear the UI
                    if self.template_data.get('name') == template_name:
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
                        self.template_name_input.clear()
                        self.slide_list.clear()

                except Exception as e:
                    QMessageBox.critical(
                        self,
                        "Delete Error",
                        f"Failed to delete template:\n{str(e)}"
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
