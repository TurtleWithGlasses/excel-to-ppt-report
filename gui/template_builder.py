"""
ReportForge - Template Builder Interface
Advanced interface for creating and editing report templates
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QFileDialog, QComboBox, QListWidget, QSplitter,
    QGraphicsView, QGraphicsScene, QFrame, QScrollArea, QCheckBox,
    QSpinBox, QColorDialog, QMessageBox, QDialog, QDialogButtonBox,
    QGroupBox, QFormLayout, QListWidgetItem, QGraphicsTextItem, QGraphicsPixmapItem
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPainter, QPixmap, QIcon
import json
from datetime import datetime
import os


class ComponentWidget(QPushButton):
    """Clickable component widget for component library"""
    component_clicked = pyqtSignal(str)  # Custom signal emitted with component_type
    
    def __init__(self, component_type, icon_text, tooltip, parent=None):
        super().__init__(parent)
        self.component_type = component_type
        self.setToolTip(tooltip)
        self.setup_ui(icon_text)
        # Connect built-in clicked signal to emit our custom signal
        super().clicked.connect(lambda: self.component_clicked.emit(self.component_type))

    def setup_ui(self, icon_text):
        """Setup component widget UI"""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(10, 10, 10, 10)

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
            QPushButton {
                background-color: white;
                border: 2px solid #E5E7EB;
                border-radius: 8px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #F3F4F6;
                border: 2px solid #2563EB;
            }
            QPushButton:pressed {
                background-color: #EFF6FF;
                border: 2px solid #1D4ED8;
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
            'embedded_logo_path': None,
            'title_slide': {
                'title': '',
                'subtitle': '',
                'description': ''
            },
            'table_slide': {
                'title': 'Yönetici Özeti',
                'subtitle': 'Haberlerin Dağılımı',
                'columns': ['Firma', 'Net Etki', 'Erişim', 'Reklam Eşdeğeri'],
                'sort_by': 'Net Etki',
                'ascending': False,
                'group_by': 'Firma',
                'aggregations': {
                    'Toplam': 'count',
                    'Pozitif': 'sum',
                    'Negatif': 'sum',
                    'Erişim': 'sum',
                    'STXCM': 'sum',
                    'Reklam Eşdeğeri': 'sum'
                },
                'note': '',
                'style': {
                    'font_name': 'Calibri',
                    'font_size': 11,
                    'header_color': '#2563EB',
                    'header_text_color': '#FFFFFF',
                    'row_color_1': '#FFFFFF',
                    'row_color_2': '#F9FAFB',
                    'text_color': '#1F2937'
                }
            },
            'chart_slide': {
                'chart_type': 'column',
                'title': '',
                'x_column': 'Firma',
                'y_column': 'Net Etki',
                'calculation': 'sum',
                'sort_by': 'Net Etki',
                'ascending': False,
                'top_n': None,
                'style': {
                    'colors': ['#2563EB', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'],
                    'show_values': True,
                    'grid': True,
                    'legend_position': 'none'
                }
            },
            'colors': {
                'primary': '#2563EB',
                'secondary': '#10B981',
                'accent': '#F59E0B'
            },
            'font_family': 'Segoe UI',
            'slides': []
        }
        self.current_slide_index = -1
        self.selected_component_type = None  # Track which component is being edited
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

        # Title Slide Section - Create but don't show (editing via component button)
        title_slide_group = self._create_title_slide_section()
        title_slide_group.setVisible(False)  # Hide from left panel
        scroll_layout.addWidget(title_slide_group)

        # Table Slide Section - Create but don't show (editing via component button)
        table_slide_group = self._create_table_slide_section()
        table_slide_group.setVisible(False)  # Hide from left panel
        scroll_layout.addWidget(table_slide_group)

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

    def _create_title_slide_section(self):
        """Create title slide configuration section"""
        group = QGroupBox("Title Slide")
        group.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        layout = QFormLayout(group)

        # Title
        self.title_slide_title_input = QLineEdit()
        self.title_slide_title_input.setPlaceholderText("e.g., BSH ve Rakipleri Medya Analizi")
        self.title_slide_title_input.textChanged.connect(self.on_title_slide_changed)
        layout.addRow("Title:", self.title_slide_title_input)

        # Subtitle
        self.title_slide_subtitle_input = QLineEdit()
        self.title_slide_subtitle_input.setPlaceholderText("e.g., {month} {year}")
        self.title_slide_subtitle_input.textChanged.connect(self.on_title_slide_changed)
        layout.addRow("Subtitle:", self.title_slide_subtitle_input)

        # Description
        self.title_slide_description_input = QLineEdit()
        self.title_slide_description_input.setPlaceholderText("e.g., Beyaz Eşya Sektörü - Medya Takip Raporu")
        self.title_slide_description_input.textChanged.connect(self.on_title_slide_changed)
        layout.addRow("Description:", self.title_slide_description_input)

        # Embedded Logo
        embedded_logo_layout = QHBoxLayout()
        self.embedded_logo_path_label = QLabel("No embedded logo selected")
        self.embedded_logo_path_label.setStyleSheet("color: #6B7280;")
        embedded_logo_layout.addWidget(self.embedded_logo_path_label)

        embedded_logo_btn = QPushButton("Browse...")
        embedded_logo_btn.clicked.connect(self.select_embedded_logo)
        embedded_logo_layout.addWidget(embedded_logo_btn)

        layout.addRow("Embedded Logo:", embedded_logo_layout)

        return group

    def _create_table_slide_section(self):
        """Create table slide configuration section"""
        group = QGroupBox("Table Slide")
        group.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        layout = QFormLayout(group)

        # Title
        self.table_slide_title_input = QLineEdit()
        self.table_slide_title_input.setPlaceholderText("e.g., Yönetici Özeti")
        self.table_slide_title_input.textChanged.connect(self.on_table_slide_changed)
        layout.addRow("Title:", self.table_slide_title_input)

        # Subtitle
        self.table_slide_subtitle_input = QLineEdit()
        self.table_slide_subtitle_input.setPlaceholderText("e.g., Haberlerin Dağılımı")
        self.table_slide_subtitle_input.textChanged.connect(self.on_table_slide_changed)
        layout.addRow("Subtitle:", self.table_slide_subtitle_input)

        # Columns (multi-select list)
        columns_label = QLabel("Columns to Display:")
        layout.addRow(columns_label)
        
        self.table_columns_list = QListWidget()
        self.table_columns_list.setMaximumHeight(120)
        self.table_columns_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        # Common columns from Excel file
        common_columns = ['Firma', 'Kurum', 'Toplam', 'Pozitif', 'Negatif', 'Erişim', 
                         'STXCM', 'StxCm', 'Reklam Eşdeğeri', 'Net Etki', 'Medya Kapsam']
        for col in common_columns:
            item = QListWidgetItem(col)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.table_columns_list.addItem(item)
        self.table_columns_list.itemChanged.connect(self.on_table_slide_changed)
        layout.addRow(self.table_columns_list)

        # Sort Column
        self.table_sort_column_combo = QComboBox()
        self.table_sort_column_combo.addItems([''] + common_columns)
        self.table_sort_column_combo.currentTextChanged.connect(self.on_table_slide_changed)
        layout.addRow("Sort By:", self.table_sort_column_combo)

        # Sort Order
        self.table_sort_order_combo = QComboBox()
        self.table_sort_order_combo.addItems(['Descending', 'Ascending'])
        self.table_sort_order_combo.currentTextChanged.connect(self.on_table_slide_changed)
        layout.addRow("Sort Order:", self.table_sort_order_combo)

        # Group By
        self.table_group_by_combo = QComboBox()
        self.table_group_by_combo.addItems([''] + common_columns)
        self.table_group_by_combo.currentTextChanged.connect(self.on_table_slide_changed)
        layout.addRow("Group By:", self.table_group_by_combo)

        # Note/Description
        self.table_slide_note_input = QLineEdit()
        self.table_slide_note_input.setPlaceholderText("e.g., BSH ve markaları toplamında...")
        self.table_slide_note_input.textChanged.connect(self.on_table_slide_changed)
        layout.addRow("Note:", self.table_slide_note_input)

        # Styling Section
        styling_label = QLabel("Table Styling:")
        styling_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        layout.addRow(styling_label)

        # Font Family
        self.table_font_combo = QComboBox()
        self.table_font_combo.addItems(['Calibri', 'Arial', 'Segoe UI', 'Times New Roman', 'Verdana'])
        self.table_font_combo.currentTextChanged.connect(self.on_table_slide_changed)
        layout.addRow("Font Family:", self.table_font_combo)

        # Font Size
        self.table_font_size_spin = QSpinBox()
        self.table_font_size_spin.setMinimum(8)
        self.table_font_size_spin.setMaximum(24)
        self.table_font_size_spin.setValue(11)
        self.table_font_size_spin.valueChanged.connect(self.on_table_slide_changed)
        layout.addRow("Font Size:", self.table_font_size_spin)

        # Header Color
        header_color_layout = QHBoxLayout()
        self.table_header_color_btn = QPushButton()
        self.table_header_color_btn.setFixedSize(40, 30)
        self.table_header_color_btn.setStyleSheet("background-color: #2563EB; border: 1px solid #E5E7EB;")
        self.table_header_color_btn.clicked.connect(lambda: self.pick_table_color('header'))
        header_color_layout.addWidget(self.table_header_color_btn)
        self.table_header_color_label = QLabel("#2563EB")
        header_color_layout.addWidget(self.table_header_color_label)
        layout.addRow("Header Color:", header_color_layout)

        # Row Color 1 (even rows)
        row1_color_layout = QHBoxLayout()
        self.table_row1_color_btn = QPushButton()
        self.table_row1_color_btn.setFixedSize(40, 30)
        self.table_row1_color_btn.setStyleSheet("background-color: #FFFFFF; border: 1px solid #E5E7EB;")
        self.table_row1_color_btn.clicked.connect(lambda: self.pick_table_color('row1'))
        row1_color_layout.addWidget(self.table_row1_color_btn)
        self.table_row1_color_label = QLabel("#FFFFFF")
        row1_color_layout.addWidget(self.table_row1_color_label)
        layout.addRow("Row Color 1:", row1_color_layout)

        # Row Color 2 (odd rows)
        row2_color_layout = QHBoxLayout()
        self.table_row2_color_btn = QPushButton()
        self.table_row2_color_btn.setFixedSize(40, 30)
        self.table_row2_color_btn.setStyleSheet("background-color: #F9FAFB; border: 1px solid #E5E7EB;")
        self.table_row2_color_btn.clicked.connect(lambda: self.pick_table_color('row2'))
        row2_color_layout.addWidget(self.table_row2_color_btn)
        self.table_row2_color_label = QLabel("#F9FAFB")
        row2_color_layout.addWidget(self.table_row2_color_label)
        layout.addRow("Row Color 2:", row2_color_layout)

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
        instructions = QLabel("Click a component to edit:")
        instructions.setFont(QFont("Segoe UI", 9))
        instructions.setStyleSheet("color: #6B7280;")
        layout.addWidget(instructions)

        # Component palette
        components_layout = QHBoxLayout()
        components_layout.setSpacing(10)

        # Title Slide Component
        title_slide_widget = ComponentWidget("Title Slide", "📄", "Title slide with logo and text")
        title_slide_widget.component_clicked.connect(self.show_component_editor)
        components_layout.addWidget(title_slide_widget)

        # Table Component
        table_widget = ComponentWidget("Table", "📊", "Data table for structured information")
        table_widget.component_clicked.connect(self.show_component_editor)
        components_layout.addWidget(table_widget)

        # Chart Component
        chart_widget = ComponentWidget("Chart", "📈", "Visualizations (bar, column, pie, line)")
        chart_widget.component_clicked.connect(self.show_component_editor)
        components_layout.addWidget(chart_widget)

        # Text Component
        text_widget = ComponentWidget("Text", "📝", "Titles, headings, paragraphs")
        text_widget.component_clicked.connect(self.show_component_editor)
        components_layout.addWidget(text_widget)

        # Image Component
        image_widget = ComponentWidget("Image", "🖼️", "Logos, photos, graphics")
        image_widget.component_clicked.connect(self.show_component_editor)
        components_layout.addWidget(image_widget)

        # Summary Component
        summary_widget = ComponentWidget("Summary", "💡", "Auto-generated insights from data")
        summary_widget.component_clicked.connect(self.show_component_editor)
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
        self.config_layout.setContentsMargins(10, 10, 10, 10)

        # Initial placeholder
        self.config_placeholder = QLabel("Select a component to configure")
        self.config_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.config_placeholder.setStyleSheet("color: #9CA3AF; padding: 20px;")
        self.config_layout.addWidget(self.config_placeholder)

        self.config_scroll.setWidget(self.config_widget)
        layout.addWidget(self.config_scroll)

        return panel

    def show_component_editor(self, component_type):
        """Show editing panel for selected component type"""
        self.selected_component_type = component_type
        
        # Clear existing config widgets
        while self.config_layout.count():
            item = self.config_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
            elif item.layout():
                # Clear layout items
                while item.layout().count():
                    layout_item = item.layout().takeAt(0)
                    if layout_item.widget():
                        layout_item.widget().setParent(None)
        
        # Show appropriate editor
        if component_type == "Title Slide":
            self._show_title_slide_editor()
        elif component_type == "Table":
            self._show_table_editor()
        elif component_type == "Chart":
            self._show_chart_editor()
        elif component_type == "Text":
            self._show_text_editor()
        elif component_type == "Image":
            self._show_image_editor()
        elif component_type == "Summary":
            self._show_summary_editor()
        else:
            # Show placeholder if unknown component
            placeholder = QLabel(f"Configuration for {component_type}\n(Coming soon)")
            placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            placeholder.setStyleSheet("color: #9CA3AF; padding: 20px;")
            self.config_layout.addWidget(placeholder)
        
        # Update preview
        self.update_preview()

    def _show_title_slide_editor(self):
        """Show title slide editing panel"""
        title_label = QLabel("Title Slide Configuration")
        title_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.config_layout.addWidget(title_label)

        # Get existing values from template_data
        title_slide_settings = self.template_data.get('title_slide', {})

        # Get existing values from widgets or template_data
        try:
            existing_title = self.title_slide_title_input.text() if hasattr(self, 'title_slide_title_input') and self.title_slide_title_input else ''
            existing_subtitle = self.title_slide_subtitle_input.text() if hasattr(self, 'title_slide_subtitle_input') and self.title_slide_subtitle_input else ''
            existing_description = self.title_slide_description_input.text() if hasattr(self, 'title_slide_description_input') and self.title_slide_description_input else ''
        except RuntimeError:
            # Widgets were deleted, fall back to template_data
            existing_title = title_slide_settings.get('title', '')
            existing_subtitle = title_slide_settings.get('subtitle', '')
            existing_description = title_slide_settings.get('description', '')
        
        # Always create new widgets to avoid deleted widget issues
        self.title_slide_title_input = QLineEdit()
        self.title_slide_title_input.setPlaceholderText("e.g., BSH ve Rakipleri Medya Analizi")
        if existing_title:
            self.title_slide_title_input.setText(existing_title)
        self.title_slide_title_input.textChanged.connect(self.on_title_slide_changed)
        
        self.title_slide_subtitle_input = QLineEdit()
        self.title_slide_subtitle_input.setPlaceholderText("e.g., {month} {year}")
        if existing_subtitle:
            self.title_slide_subtitle_input.setText(existing_subtitle)
        self.title_slide_subtitle_input.textChanged.connect(self.on_title_slide_changed)
        
        self.title_slide_description_input = QLineEdit()
        self.title_slide_description_input.setPlaceholderText("e.g., Beyaz Eşya Sektörü - Medya Takip Raporu")
        if existing_description:
            self.title_slide_description_input.setText(existing_description)
        self.title_slide_description_input.textChanged.connect(self.on_title_slide_changed)
        
        # Embedded logo label - always recreate to avoid deleted widget issues
        existing_logo = title_slide_settings.get('embedded_logo_path', '')
        if existing_logo:
            self.embedded_logo_path_label = QLabel(os.path.basename(existing_logo))
            self.embedded_logo_path_label.setStyleSheet("color: #10B981; font-weight: bold;")
        else:
            self.embedded_logo_path_label = QLabel("No embedded logo selected")
            self.embedded_logo_path_label.setStyleSheet("color: #6B7280;")
        
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        form_layout.addRow("Title:", self.title_slide_title_input)
        form_layout.addRow("Subtitle:", self.title_slide_subtitle_input)
        form_layout.addRow("Description:", self.title_slide_description_input)
        
        # Logo selection
        logo_layout = QHBoxLayout()
        logo_layout.addWidget(self.embedded_logo_path_label)
        embedded_logo_btn = QPushButton("Browse...")
        embedded_logo_btn.clicked.connect(self.select_embedded_logo)
        logo_layout.addWidget(embedded_logo_btn)
        form_layout.addRow("Embedded Logo:", logo_layout)
        
        form_widget = QWidget()
        form_widget.setLayout(form_layout)
        self.config_layout.addWidget(form_widget)
        self.config_layout.addStretch()

    def _show_table_editor(self):
        """Show table editing panel"""
        title_label = QLabel("Table Configuration")
        title_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.config_layout.addWidget(title_label)
        
        # Get existing values from template_data instead of potentially deleted widgets
        table_slide_settings = self.template_data.get('table_slide', {})
        existing_title = table_slide_settings.get('title', '')
        existing_subtitle = table_slide_settings.get('subtitle', '')
        existing_note = table_slide_settings.get('note', '')
        existing_sort_by = table_slide_settings.get('sort_by', '')
        existing_sort_order = table_slide_settings.get('ascending', False)
        existing_group_by = table_slide_settings.get('group_by', '')
        existing_columns = table_slide_settings.get('columns', [])
        
        # Get style settings
        style_settings = table_slide_settings.get('style', {})
        existing_font = style_settings.get('font_name', 'Calibri')
        existing_font_size = style_settings.get('font_size', 11)
        existing_header_color = style_settings.get('header_color', '#2563EB')
        existing_row1_color = style_settings.get('row_color_1', '#FFFFFF')
        existing_row2_color = style_settings.get('row_color_2', '#F9FAFB')
        existing_bg_color = style_settings.get('background_color', '#FFFFFF')
        existing_header_align = style_settings.get('header_alignment', 'Center')
        existing_text_align = style_settings.get('text_alignment', 'Left')
        existing_header_bold = style_settings.get('header_bold', True)
        existing_header_italic = style_settings.get('header_italic', False)
        existing_text_bold = style_settings.get('text_bold', False)
        existing_text_italic = style_settings.get('text_italic', False)
        
        # Always create new widgets to avoid deleted widget issues
        self._initialize_table_inputs()
        
        # Set existing values from template_data
        if existing_title:
            self.table_slide_title_input.setText(existing_title)
        if existing_subtitle:
            self.table_slide_subtitle_input.setText(existing_subtitle)
        if existing_note:
            self.table_slide_note_input.setText(existing_note)
        
        # Set sort column
        if existing_sort_by:
            index = self.table_sort_column_combo.findText(existing_sort_by)
            if index >= 0:
                self.table_sort_column_combo.setCurrentIndex(index)
        
        # Set sort order
        self.table_sort_order_combo.setCurrentIndex(0 if existing_sort_order else 1)
        
        # Set group by
        if existing_group_by:
            index = self.table_group_by_combo.findText(existing_group_by)
            if index >= 0:
                self.table_group_by_combo.setCurrentIndex(index)
        
        # Set columns (check items in list)
        for i in range(self.table_columns_list.count()):
            item = self.table_columns_list.item(i)
            if item and item.text() in existing_columns:
                item.setCheckState(Qt.CheckState.Checked)
        
        # Set font
        font_index = self.table_font_combo.findText(existing_font)
        if font_index >= 0:
            self.table_font_combo.setCurrentIndex(font_index)
        self.table_font_size_spin.setValue(existing_font_size)
        
        # Set colors
        self.table_header_color_btn.setStyleSheet(f"background-color: {existing_header_color}; border: 1px solid #E5E7EB;")
        self.table_header_color_label.setText(existing_header_color)
        self.table_row1_color_btn.setStyleSheet(f"background-color: {existing_row1_color}; border: 1px solid #E5E7EB;")
        self.table_row1_color_label.setText(existing_row1_color)
        self.table_row2_color_btn.setStyleSheet(f"background-color: {existing_row2_color}; border: 1px solid #E5E7EB;")
        self.table_row2_color_label.setText(existing_row2_color)
        self.table_bg_color_btn.setStyleSheet(f"background-color: {existing_bg_color}; border: 1px solid #E5E7EB;")
        self.table_bg_color_label.setText(existing_bg_color)

        # Set alignments
        header_align_index = self.table_header_align_combo.findText(existing_header_align)
        if header_align_index >= 0:
            self.table_header_align_combo.setCurrentIndex(header_align_index)
        text_align_index = self.table_text_align_combo.findText(existing_text_align)
        if text_align_index >= 0:
            self.table_text_align_combo.setCurrentIndex(text_align_index)

        # Set text styles
        self.table_header_bold_check.setChecked(existing_header_bold)
        self.table_header_italic_check.setChecked(existing_header_italic)
        self.table_text_bold_check.setChecked(existing_text_bold)
        self.table_text_italic_check.setChecked(existing_text_italic)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        form_layout.addRow("Title:", self.table_slide_title_input)
        form_layout.addRow("Subtitle:", self.table_slide_subtitle_input)
        
        # Columns
        columns_label = QLabel("Columns to Display:")
        form_layout.addRow(columns_label)
        form_layout.addRow(self.table_columns_list)
        
        form_layout.addRow("Sort By:", self.table_sort_column_combo)
        form_layout.addRow("Sort Order:", self.table_sort_order_combo)
        form_layout.addRow("Group By:", self.table_group_by_combo)
        form_layout.addRow("Note:", self.table_slide_note_input)
        
        # Styling section
        styling_label = QLabel("Table Styling:")
        styling_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        form_layout.addRow(styling_label)
        
        form_layout.addRow("Font Family:", self.table_font_combo)
        form_layout.addRow("Font Size:", self.table_font_size_spin)
        
        # Colors
        header_color_layout = QHBoxLayout()
        header_color_layout.addWidget(self.table_header_color_btn)
        header_color_layout.addWidget(self.table_header_color_label)
        form_layout.addRow("Header Color:", header_color_layout)
        
        row1_color_layout = QHBoxLayout()
        row1_color_layout.addWidget(self.table_row1_color_btn)
        row1_color_layout.addWidget(self.table_row1_color_label)
        form_layout.addRow("Row Color 1:", row1_color_layout)
        
        row2_color_layout = QHBoxLayout()
        row2_color_layout.addWidget(self.table_row2_color_btn)
        row2_color_layout.addWidget(self.table_row2_color_label)
        form_layout.addRow("Row Color 2:", row2_color_layout)

        bg_color_layout = QHBoxLayout()
        bg_color_layout.addWidget(self.table_bg_color_btn)
        bg_color_layout.addWidget(self.table_bg_color_label)
        form_layout.addRow("Background Color:", bg_color_layout)

        # Alignment section
        form_layout.addRow("Header Alignment:", self.table_header_align_combo)
        form_layout.addRow("Text Alignment:", self.table_text_align_combo)

        # Text style section
        style_checkboxes_layout = QVBoxLayout()
        style_checkboxes_layout.addWidget(self.table_header_bold_check)
        style_checkboxes_layout.addWidget(self.table_header_italic_check)
        style_checkboxes_layout.addWidget(self.table_text_bold_check)
        style_checkboxes_layout.addWidget(self.table_text_italic_check)
        form_layout.addRow("Text Style:", style_checkboxes_layout)

        form_widget = QWidget()
        form_widget.setLayout(form_layout)
        self.config_layout.addWidget(form_widget)
        self.config_layout.addStretch()

    def _initialize_table_inputs(self):
        """Initialize table slide input fields - always creates new widgets"""
        # Always create new widgets to avoid deleted widget issues
        self.table_slide_title_input = QLineEdit()
        self.table_slide_title_input.setPlaceholderText("e.g., Yönetici Özeti")
        self.table_slide_title_input.textChanged.connect(self.on_table_slide_changed)
        
        self.table_slide_subtitle_input = QLineEdit()
        self.table_slide_subtitle_input.setPlaceholderText("e.g., Haberlerin Dağılımı")
        self.table_slide_subtitle_input.textChanged.connect(self.on_table_slide_changed)
        
        self.table_columns_list = QListWidget()
        self.table_columns_list.setMaximumHeight(120)
        self.table_columns_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        common_columns = ['Firma', 'Kurum', 'Toplam', 'Pozitif', 'Negatif', 'Erişim', 
                         'STXCM', 'StxCm', 'Reklam Eşdeğeri', 'Net Etki', 'Medya Kapsam']
        for col in common_columns:
            item = QListWidgetItem(col)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.table_columns_list.addItem(item)
        self.table_columns_list.itemChanged.connect(self.on_table_slide_changed)
        
        self.table_sort_column_combo = QComboBox()
        self.table_sort_column_combo.addItems([''] + common_columns)
        self.table_sort_column_combo.currentTextChanged.connect(self.on_table_slide_changed)
        
        self.table_sort_order_combo = QComboBox()
        self.table_sort_order_combo.addItems(['Descending', 'Ascending'])
        self.table_sort_order_combo.currentTextChanged.connect(self.on_table_slide_changed)
        
        self.table_group_by_combo = QComboBox()
        self.table_group_by_combo.addItems([''] + common_columns)
        self.table_group_by_combo.currentTextChanged.connect(self.on_table_slide_changed)
        
        self.table_slide_note_input = QLineEdit()
        self.table_slide_note_input.setPlaceholderText("e.g., BSH ve markaları toplamında...")
        self.table_slide_note_input.textChanged.connect(self.on_table_slide_changed)
        
        self.table_font_combo = QComboBox()
        self.table_font_combo.addItems(['Calibri', 'Arial', 'Segoe UI', 'Times New Roman', 'Verdana'])
        self.table_font_combo.currentTextChanged.connect(self.on_table_slide_changed)
        
        self.table_font_size_spin = QSpinBox()
        self.table_font_size_spin.setMinimum(8)
        self.table_font_size_spin.setMaximum(24)
        self.table_font_size_spin.setValue(11)
        self.table_font_size_spin.valueChanged.connect(self.on_table_slide_changed)
        
        # Color buttons
        self.table_header_color_btn = QPushButton()
        self.table_header_color_btn.setFixedSize(40, 30)
        self.table_header_color_btn.setStyleSheet("background-color: #2563EB; border: 1px solid #E5E7EB;")
        self.table_header_color_btn.clicked.connect(lambda: self.pick_table_color('header'))
        self.table_header_color_label = QLabel("#2563EB")
        
        self.table_row1_color_btn = QPushButton()
        self.table_row1_color_btn.setFixedSize(40, 30)
        self.table_row1_color_btn.setStyleSheet("background-color: #FFFFFF; border: 1px solid #E5E7EB;")
        self.table_row1_color_btn.clicked.connect(lambda: self.pick_table_color('row1'))
        self.table_row1_color_label = QLabel("#FFFFFF")
        
        self.table_row2_color_btn = QPushButton()
        self.table_row2_color_btn.setFixedSize(40, 30)
        self.table_row2_color_btn.setStyleSheet("background-color: #F9FAFB; border: 1px solid #E5E7EB;")
        self.table_row2_color_btn.clicked.connect(lambda: self.pick_table_color('row2'))
        self.table_row2_color_label = QLabel("#F9FAFB")

        # Background color
        self.table_bg_color_btn = QPushButton()
        self.table_bg_color_btn.setFixedSize(40, 30)
        self.table_bg_color_btn.setStyleSheet("background-color: #FFFFFF; border: 1px solid #E5E7EB;")
        self.table_bg_color_btn.clicked.connect(lambda: self.pick_table_color('background'))
        self.table_bg_color_label = QLabel("#FFFFFF")

        # Text alignment
        self.table_text_align_combo = QComboBox()
        self.table_text_align_combo.addItems(['Left', 'Center', 'Right'])
        self.table_text_align_combo.setCurrentText('Left')
        self.table_text_align_combo.currentTextChanged.connect(self.on_table_slide_changed)

        # Header alignment
        self.table_header_align_combo = QComboBox()
        self.table_header_align_combo.addItems(['Left', 'Center', 'Right'])
        self.table_header_align_combo.setCurrentText('Center')
        self.table_header_align_combo.currentTextChanged.connect(self.on_table_slide_changed)

        # Text style checkboxes
        self.table_header_bold_check = QCheckBox("Bold Headers")
        self.table_header_bold_check.setChecked(True)
        self.table_header_bold_check.stateChanged.connect(self.on_table_slide_changed)

        self.table_header_italic_check = QCheckBox("Italic Headers")
        self.table_header_italic_check.setChecked(False)
        self.table_header_italic_check.stateChanged.connect(self.on_table_slide_changed)

        self.table_text_bold_check = QCheckBox("Bold Text")
        self.table_text_bold_check.setChecked(False)
        self.table_text_bold_check.stateChanged.connect(self.on_table_slide_changed)

        self.table_text_italic_check = QCheckBox("Italic Text")
        self.table_text_italic_check.setChecked(False)
        self.table_text_italic_check.stateChanged.connect(self.on_table_slide_changed)

    def _show_chart_editor(self):
        """Show chart editing panel"""
        title_label = QLabel("Chart Configuration")
        title_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.config_layout.addWidget(title_label)
        
        # Get existing values from template_data instead of potentially deleted widgets
        chart_slide_settings = self.template_data.get('chart_slide', {})
        existing_title = chart_slide_settings.get('title', '')
        existing_chart_type = chart_slide_settings.get('chart_type', 'column')
        existing_x_col = chart_slide_settings.get('x_column', 'Firma')
        existing_y_col = chart_slide_settings.get('y_column', 'Net Etki')
        existing_calculation = chart_slide_settings.get('calculation', 'sum')
        existing_sort_by = chart_slide_settings.get('sort_by', '')
        existing_ascending = chart_slide_settings.get('ascending')
        # Handle None case for ascending
        if existing_ascending is None:
            existing_ascending = False
        existing_top_n = chart_slide_settings.get('top_n')
        # Handle None case - convert to 0 (show all), and ensure it's an integer
        if existing_top_n is None or existing_top_n == '':
            existing_top_n = 0
        else:
            existing_top_n = int(existing_top_n)
        
        # Get style settings
        style_settings = chart_slide_settings.get('style', {})
        existing_colors = style_settings.get('colors', ['#2563EB', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'])
        existing_show_values = style_settings.get('show_values')
        if existing_show_values is None:
            existing_show_values = True
        existing_show_grid = style_settings.get('grid')
        if existing_show_grid is None:
            existing_show_grid = True
        existing_legend = style_settings.get('legend_position', 'none')
        
        # Always create new widgets to avoid deleted widget issues
        self._initialize_chart_inputs()
        
        # Set existing values from template_data
        if existing_title:
            self.chart_title_input.setText(existing_title)
        
        # Set chart type
        chart_type_index = self.chart_type_combo.findText(existing_chart_type)
        if chart_type_index >= 0:
            self.chart_type_combo.setCurrentIndex(chart_type_index)
        
        # Set X column
        if existing_x_col:
            index = self.chart_x_column_combo.findText(existing_x_col)
            if index >= 0:
                self.chart_x_column_combo.setCurrentIndex(index)
        
        # Set Y column
        if existing_y_col:
            index = self.chart_y_column_combo.findText(existing_y_col)
            if index >= 0:
                self.chart_y_column_combo.setCurrentIndex(index)
        
        # Set calculation
        calc_index = self.chart_calculation_combo.findText(existing_calculation)
        if calc_index >= 0:
            self.chart_calculation_combo.setCurrentIndex(calc_index)
        
        # Set sort column
        if existing_sort_by:
            sort_index = self.chart_sort_column_combo.findText(existing_sort_by)
            if sort_index >= 0:
                self.chart_sort_column_combo.setCurrentIndex(sort_index)
        
        # Set sort order
        self.chart_sort_order_combo.setCurrentIndex(0 if existing_ascending else 1)
        
        # Set top N
        self.chart_top_n_spin.setValue(existing_top_n)
        
        # Set show values
        self.chart_show_values_check.setChecked(existing_show_values)
        
        # Set show grid
        self.chart_show_grid_check.setChecked(existing_show_grid)
        
        # Set legend position
        legend_index = self.chart_legend_combo.findText(existing_legend)
        if legend_index >= 0:
            self.chart_legend_combo.setCurrentIndex(legend_index)
        
        # Set colors (check items in list)
        for i in range(self.chart_colors_list.count()):
            item = self.chart_colors_list.item(i)
            if item and item.text() in existing_colors:
                item.setCheckState(Qt.CheckState.Checked)
            else:
                item.setCheckState(Qt.CheckState.Unchecked)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        form_layout.addRow("Chart Type:", self.chart_type_combo)
        form_layout.addRow("Chart Title:", self.chart_title_input)
        form_layout.addRow("X-Axis (Categories):", self.chart_x_column_combo)
        form_layout.addRow("Y-Axis (Values):", self.chart_y_column_combo)
        form_layout.addRow("Calculation:", self.chart_calculation_combo)
        form_layout.addRow("Sort By:", self.chart_sort_column_combo)
        form_layout.addRow("Sort Order:", self.chart_sort_order_combo)
        form_layout.addRow("Top N (limit):", self.chart_top_n_spin)
        
        # Styling section
        styling_label = QLabel("Chart Styling:")
        styling_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        form_layout.addRow(styling_label)
        
        form_layout.addRow("Show Values:", self.chart_show_values_check)
        form_layout.addRow("Show Grid:", self.chart_show_grid_check)
        form_layout.addRow("Legend Position:", self.chart_legend_combo)
        
        # Colors
        colors_label = QLabel("Chart Colors:")
        form_layout.addRow(colors_label)
        form_layout.addRow(self.chart_colors_list)
        
        form_widget = QWidget()
        form_widget.setLayout(form_layout)
        self.config_layout.addWidget(form_widget)
        self.config_layout.addStretch()

    def _initialize_chart_inputs(self):
        """Initialize chart input fields if they don't exist"""
        # Chart type
        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems(['column', 'bar', 'pie', 'line', 'stacked_column', 'stacked_bar'])
        self.chart_type_combo.currentTextChanged.connect(self.on_chart_changed)
        
        # Chart title
        self.chart_title_input = QLineEdit()
        self.chart_title_input.setPlaceholderText("e.g., Kurumların Yansıma Sayısı Bazında Karşılaştırılması")
        self.chart_title_input.textChanged.connect(self.on_chart_changed)
        
        # Common columns from Excel file
        common_columns = ['Firma', 'Kurum', 'Toplam', 'Pozitif', 'Negatif', 'Erişim', 
                         'STXCM', 'StxCm', 'Reklam Eşdeğeri', 'Net Etki', 'Medya Kapsam', 
                         'Mecra', 'Medya Tür', 'Algı']
        
        # X column (categories)
        self.chart_x_column_combo = QComboBox()
        self.chart_x_column_combo.addItems(common_columns)
        self.chart_x_column_combo.currentTextChanged.connect(self.on_chart_changed)
        
        # Y column (values)
        self.chart_y_column_combo = QComboBox()
        self.chart_y_column_combo.addItems(common_columns)
        self.chart_y_column_combo.currentTextChanged.connect(self.on_chart_changed)
        
        # Calculation type
        self.chart_calculation_combo = QComboBox()
        self.chart_calculation_combo.addItems(['sum', 'count', 'average', 'mean', 'max', 'min', 'percentage'])
        self.chart_calculation_combo.currentTextChanged.connect(self.on_chart_changed)
        
        # Sort column
        self.chart_sort_column_combo = QComboBox()
        self.chart_sort_column_combo.addItems([''] + common_columns)
        self.chart_sort_column_combo.currentTextChanged.connect(self.on_chart_changed)
        
        # Sort order
        self.chart_sort_order_combo = QComboBox()
        self.chart_sort_order_combo.addItems(['Descending', 'Ascending'])
        self.chart_sort_order_combo.currentTextChanged.connect(self.on_chart_changed)
        
        # Top N
        self.chart_top_n_spin = QSpinBox()
        self.chart_top_n_spin.setMinimum(0)
        self.chart_top_n_spin.setMaximum(100)
        self.chart_top_n_spin.setValue(0)  # 0 means show all
        self.chart_top_n_spin.setSpecialValueText("All")
        self.chart_top_n_spin.valueChanged.connect(self.on_chart_changed)
        
        # Show values checkbox
        self.chart_show_values_check = QCheckBox()
        self.chart_show_values_check.setChecked(True)
        self.chart_show_values_check.stateChanged.connect(self.on_chart_changed)
        
        # Show grid checkbox
        self.chart_show_grid_check = QCheckBox()
        self.chart_show_grid_check.setChecked(True)
        self.chart_show_grid_check.stateChanged.connect(self.on_chart_changed)
        
        # Legend position
        self.chart_legend_combo = QComboBox()
        self.chart_legend_combo.addItems(['none', 'top', 'bottom', 'left', 'right'])
        self.chart_legend_combo.currentTextChanged.connect(self.on_chart_changed)
        
        # Colors list (multi-select)
        self.chart_colors_list = QListWidget()
        self.chart_colors_list.setMaximumHeight(100)
        self.chart_colors_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        default_colors = ['#2563EB', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4', '#EC4899', '#84CC16']
        for color in default_colors:
            item = QListWidgetItem(color)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked)
            self.chart_colors_list.addItem(item)
        self.chart_colors_list.itemChanged.connect(self.on_chart_changed)

    def on_chart_changed(self):
        """Handle chart input changes - update preview if on chart slide"""
        if self.current_slide_index >= 0:
            slide = self.template_data['slides'][self.current_slide_index]
            components = slide.get('components', [])
            has_chart = any(comp.get('type') == 'chart' for comp in components)
            if has_chart or self.selected_component_type == "Chart":
                self.update_preview()

    def _show_text_editor(self):
        """Show text editing panel"""
        label = QLabel("Text Configuration\n(Coming soon)")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: #9CA3AF; padding: 20px;")
        self.config_layout.addWidget(label)

    def _show_image_editor(self):
        """Show image editing panel"""
        label = QLabel("Image Configuration\n(Coming soon)")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: #9CA3AF; padding: 20px;")
        self.config_layout.addWidget(label)

    def _show_summary_editor(self):
        """Show summary editing panel"""
        label = QLabel("Summary Configuration\n(Coming soon)")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: #9CA3AF; padding: 20px;")
        self.config_layout.addWidget(label)

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
            # Update preview if on title slide
            if self.current_slide_index == 0:
                self.update_preview()

    def select_embedded_logo(self):
        """Select embedded logo file (e.g., desiBel logo)"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Embedded Logo",
            "",
            "Image Files (*.png *.jpg *.svg);;All Files (*.*)"
        )
        if file_path:
            self.template_data['embedded_logo_path'] = file_path
            import os
            self.embedded_logo_path_label.setText(os.path.basename(file_path))
            self.embedded_logo_path_label.setStyleSheet("color: #10B981; font-weight: bold;")
            # Update preview if on title slide
            if self.current_slide_index == 0:
                self.update_preview()

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

    def pick_table_color(self, color_type):
        """Pick color for table styling"""
        table_style = self.template_data.get('table_slide', {}).get('style', {})
        
        color_map = {
            'header': ('header_color', '#2563EB'),
            'row1': ('row_color_1', '#FFFFFF'),
            'row2': ('row_color_2', '#F9FAFB'),
            'background': ('background_color', '#FFFFFF')
        }
        
        style_key, default_color = color_map.get(color_type, ('header_color', '#2563EB'))
        current_color_hex = table_style.get(style_key, default_color)
        current_color = QColor(current_color_hex)
        
        color = QColorDialog.getColor(current_color, self, f"Select {color_type.replace('row', 'Row ').title()} Color")

        if color.isValid():
            hex_color = color.name().upper()
            
            # Update template data
            if 'table_slide' not in self.template_data:
                self.template_data['table_slide'] = {}
            if 'style' not in self.template_data['table_slide']:
                self.template_data['table_slide']['style'] = {}
            self.template_data['table_slide']['style'][style_key] = hex_color

            # Update UI
            if color_type == 'header':
                self.table_header_color_btn.setStyleSheet(f"background-color: {hex_color}; border: 1px solid #E5E7EB;")
                self.table_header_color_label.setText(hex_color)
            elif color_type == 'row1':
                self.table_row1_color_btn.setStyleSheet(f"background-color: {hex_color}; border: 1px solid #E5E7EB;")
                self.table_row1_color_label.setText(hex_color)
            elif color_type == 'row2':
                self.table_row2_color_btn.setStyleSheet(f"background-color: {hex_color}; border: 1px solid #E5E7EB;")
                self.table_row2_color_label.setText(hex_color)
            elif color_type == 'background':
                self.table_bg_color_btn.setStyleSheet(f"background-color: {hex_color}; border: 1px solid #E5E7EB;")
                self.table_bg_color_label.setText(hex_color)
            
            # Update preview
            self.on_table_slide_changed()

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

            self.preview_scene.clear()

            # Check if this is the title slide (first slide)
            if self.current_slide_index == 0:
                self._render_title_slide_preview()
            # Check if this is a table slide OR if user has table slide settings configured OR if editing Table component
            elif self._is_table_slide(slide) or (self.current_slide_index > 0 and self._has_table_slide_settings()) or self.selected_component_type == "Table":
                self._render_table_slide_preview(slide)
            # Check if this is a chart slide OR if user has chart settings configured
            elif self._is_chart_slide(slide) or (self.current_slide_index > 0 and self._has_chart_settings()):
                self._render_chart_slide_preview(slide)
            else:
                # For other slides, show component info
                slide_name = slide.get('name', 'Untitled Slide')
                slide_type = slide.get('type', 'N/A')
                slide_layout = slide.get('layout', 'N/A')
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

    def _render_title_slide_preview(self):
        """Render title slide components in preview"""
        # PowerPoint slide dimensions: 10 inches x 7.5 inches
        # Preview scene: 720 x 540 pixels (16:9 aspect ratio)
        # Conversion: 1 inch = 72 pixels (standard DPI)
        INCH_TO_PIXEL = 72

        # Get title slide settings
        title_slide_settings = self.template_data.get('title_slide', {})
        
        # Safely get text from inputs (they might not exist yet)
        try:
            title = self.title_slide_title_input.text() if hasattr(self, 'title_slide_title_input') and self.title_slide_title_input else ''
        except RuntimeError:
            title = ''
        if not title:
            title = title_slide_settings.get('title', '')
        
        try:
            subtitle = self.title_slide_subtitle_input.text() if hasattr(self, 'title_slide_subtitle_input') and self.title_slide_subtitle_input else ''
        except RuntimeError:
            subtitle = ''
        if not subtitle:
            subtitle = title_slide_settings.get('subtitle', '')
        
        try:
            description = self.title_slide_description_input.text() if hasattr(self, 'title_slide_description_input') and self.title_slide_description_input else ''
        except RuntimeError:
            description = ''
        if not description:
            description = title_slide_settings.get('description', '')

        # Get positions and sizes (defaults from template or fallback)
        logo_pos = title_slide_settings.get('logo_position', {'x': 5.0, 'y': 1.0})
        logo_size = title_slide_settings.get('logo_size', {'width': 2.0, 'height': 1.5})
        title_pos = title_slide_settings.get('title_position', {'x': 0.5, 'y': 2.5})
        embedded_logo_pos = title_slide_settings.get('embedded_logo_position', {'x': 0.5, 'y': 6.5})
        embedded_logo_size = title_slide_settings.get('embedded_logo_size', {'width': 1.5, 'height': 0.5})

        # Render main logo
        logo_path = self.template_data.get('logo_path')
        if logo_path:
            logo_pixmap = self._load_image_pixmap(logo_path)
            if logo_pixmap:
                # Scale logo to fit size
                logo_width_px = logo_size['width'] * INCH_TO_PIXEL
                logo_height_px = logo_size['height'] * INCH_TO_PIXEL
                scaled_logo = logo_pixmap.scaled(
                    int(logo_width_px), int(logo_height_px),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                logo_item = QGraphicsPixmapItem(scaled_logo)
                logo_item.setPos(logo_pos['x'] * INCH_TO_PIXEL, logo_pos['y'] * INCH_TO_PIXEL)
                self.preview_scene.addItem(logo_item)

        # Render title text
        if title:
            title_font = QFont("Calibri", 40, QFont.Weight.Bold)
            title_item = self.preview_scene.addText(title, title_font)
            title_item.setDefaultTextColor(QColor("#1F2937"))
            # Center horizontally, position vertically
            title_rect = title_item.boundingRect()
            title_x = (720 - title_rect.width()) / 2  # Center in 720px width
            title_item.setPos(title_x, title_pos['y'] * INCH_TO_PIXEL)

        # Render subtitle text
        if subtitle:
            subtitle_font = QFont("Calibri", 28)
            subtitle_item = self.preview_scene.addText(subtitle, subtitle_font)
            subtitle_item.setDefaultTextColor(QColor("#2563EB"))
            subtitle_rect = subtitle_item.boundingRect()
            subtitle_x = (720 - subtitle_rect.width()) / 2
            subtitle_item.setPos(subtitle_x, (title_pos['y'] + 1.0) * INCH_TO_PIXEL)

        # Render description text
        if description:
            desc_font = QFont("Calibri", 16)
            desc_item = self.preview_scene.addText(description, desc_font)
            desc_item.setDefaultTextColor(QColor("#6B7280"))
            desc_rect = desc_item.boundingRect()
            desc_x = (720 - desc_rect.width()) / 2
            desc_item.setPos(desc_x, (title_pos['y'] + 2.0) * INCH_TO_PIXEL)

        # Render embedded logo
        embedded_logo_path = self.template_data.get('embedded_logo_path')
        if embedded_logo_path:
            embedded_logo_pixmap = self._load_image_pixmap(embedded_logo_path)
            if embedded_logo_pixmap:
                embedded_width_px = embedded_logo_size['width'] * INCH_TO_PIXEL
                embedded_height_px = embedded_logo_size['height'] * INCH_TO_PIXEL
                scaled_embedded = embedded_logo_pixmap.scaled(
                    int(embedded_width_px), int(embedded_height_px),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                embedded_item = QGraphicsPixmapItem(scaled_embedded)
                embedded_item.setPos(embedded_logo_pos['x'] * INCH_TO_PIXEL, embedded_logo_pos['y'] * INCH_TO_PIXEL)
                self.preview_scene.addItem(embedded_item)

    def _load_image_pixmap(self, image_path):
        """Load image as QPixmap, handling both absolute and relative paths"""
        if not image_path:
            return None

        # Try absolute path first
        if os.path.isabs(image_path) and os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                return pixmap

        # Try relative to project root
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        paths_to_try = [
            os.path.join(project_root, image_path),
            os.path.join(project_root, "templates", image_path),
            os.path.join(project_root, "assets", image_path),
        ]

        for path in paths_to_try:
            if os.path.exists(path):
                pixmap = QPixmap(path)
                if not pixmap.isNull():
                    return pixmap

        return None

    def _is_table_slide(self, slide):
        """Check if slide contains a table component"""
        components = slide.get('components', [])
        return any(comp.get('type') == 'table' for comp in components)
    
    def _has_table_slide_settings(self):
        """Check if user has configured table slide settings"""
        # Check if any table slide inputs have values or if columns are selected
        try:
            if hasattr(self, 'table_slide_title_input') and self.table_slide_title_input:
                if self.table_slide_title_input.text():
                    return True
            if hasattr(self, 'table_columns_list') and self.table_columns_list:
                for i in range(self.table_columns_list.count()):
                    item = self.table_columns_list.item(i)
                    if item and item.checkState() == Qt.CheckState.Checked:
                        return True
        except RuntimeError:
            pass
        return False

    def _is_chart_slide(self, slide):
        """Check if slide contains a chart component"""
        components = slide.get('components', [])
        return any(comp.get('type') == 'chart' for comp in components)
    
    def _has_chart_settings(self):
        """Check if user has configured chart settings"""
        try:
            if hasattr(self, 'chart_title_input') and self.chart_title_input:
                if self.chart_title_input.text():
                    return True
            if hasattr(self, 'chart_x_column_combo') and self.chart_x_column_combo:
                if self.chart_x_column_combo.currentText():
                    return True
        except RuntimeError:
            pass
        return False

    def _render_chart_slide_preview(self, slide):
        """Render chart slide components in preview"""
        INCH_TO_PIXEL = 72

        # Get chart settings
        chart_settings = self.template_data.get('chart_slide', {})
        
        # Safely get values from inputs
        try:
            title = self.chart_title_input.text() if hasattr(self, 'chart_title_input') and self.chart_title_input else ''
            x_column = self.chart_x_column_combo.currentText() if hasattr(self, 'chart_x_column_combo') and self.chart_x_column_combo else chart_settings.get('x_column', 'Firma')
            y_column = self.chart_y_column_combo.currentText() if hasattr(self, 'chart_y_column_combo') and self.chart_y_column_combo else chart_settings.get('y_column', 'Net Etki')
        except RuntimeError:
            title = chart_settings.get('title', '')
            x_column = chart_settings.get('x_column', 'Firma')
            y_column = chart_settings.get('y_column', 'Net Etki')
        
        if not title:
            title = chart_settings.get('title', f'{x_column} Bazında {y_column} Karşılaştırması')
        
        # Render title
        if title:
            title_font = QFont("Calibri", 16, QFont.Weight.Bold)
            title_item = self.preview_scene.addText(title, title_font)
            title_item.setDefaultTextColor(QColor("#1F2937"))
            title_item.setPos(0.5 * INCH_TO_PIXEL, 0.3 * INCH_TO_PIXEL)
        
        # Render chart preview (simplified bar chart representation)
        chart_y = 1.0 * INCH_TO_PIXEL
        chart_x = 0.5 * INCH_TO_PIXEL
        chart_width = 9.0 * INCH_TO_PIXEL
        chart_height = 3.5 * INCH_TO_PIXEL
        
        # Chart background
        self.preview_scene.addRect(
            chart_x, chart_y,
            chart_width, chart_height,
            QColor("#FFFFFF"), QColor("#E5E7EB")
        )
        
        # Sample bars (5 bars for preview)
        num_bars = 5
        bar_width = chart_width / (num_bars + 1)
        max_height = chart_height * 0.8
        
        # Get colors from UI or settings
        try:
            if hasattr(self, 'chart_colors_list') and self.chart_colors_list:
                colors = self._get_selected_chart_colors()
            else:
                chart_style = chart_settings.get('style', {})
                colors = chart_style.get('colors', ['#2563EB', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'])
        except RuntimeError:
            chart_style = chart_settings.get('style', {})
            colors = chart_style.get('colors', ['#2563EB', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'])
        
        if not colors:
            colors = ['#2563EB', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6']
        
        for i in range(num_bars):
            bar_x = chart_x + (i + 0.5) * bar_width
            bar_height = max_height * (0.9 - i * 0.15)  # Decreasing heights
            bar_y = chart_y + chart_height - bar_height
            
            # Bar color
            color_index = i % len(colors)
            bar_color = QColor(colors[color_index])
            
            # Draw bar
            self.preview_scene.addRect(
                bar_x - bar_width * 0.3, bar_y,
                bar_width * 0.6, bar_height,
                bar_color, bar_color
            )
            
            # Value label on top
            value_text = str(100 - i * 15)
            value_font = QFont("Calibri", 9)
            value_item = self.preview_scene.addText(value_text, value_font)
            value_item.setDefaultTextColor(QColor("#1F2937"))
            value_rect = value_item.boundingRect()
            value_item.setPos(bar_x - value_rect.width() / 2, bar_y - value_rect.height() - 2)
            
            # Category label below
            category_text = f"Item {i + 1}"
            category_font = QFont("Calibri", 8)
            category_item = self.preview_scene.addText(category_text, category_font)
            category_item.setDefaultTextColor(QColor("#6B7280"))
            category_rect = category_item.boundingRect()
            category_item.setPos(bar_x - category_rect.width() / 2, chart_y + chart_height + 5)

    def _render_table_slide_preview(self, slide):
        """Render table slide components in preview"""
        INCH_TO_PIXEL = 72

        # Get table slide settings
        table_slide_settings = self.template_data.get('table_slide', {})
        table_style = table_slide_settings.get('style', {})
        
        # Safely get text from inputs (they might not exist yet)
        try:
            title = self.table_slide_title_input.text() if hasattr(self, 'table_slide_title_input') and self.table_slide_title_input else ''
        except RuntimeError:
            title = ''
        if not title:
            title = table_slide_settings.get('title', 'Yönetici Özeti')
        
        try:
            subtitle = self.table_slide_subtitle_input.text() if hasattr(self, 'table_slide_subtitle_input') and self.table_slide_subtitle_input else ''
        except RuntimeError:
            subtitle = ''
        if not subtitle:
            subtitle = table_slide_settings.get('subtitle', 'Haberlerin Dağılımı')
        
        try:
            note = self.table_slide_note_input.text() if hasattr(self, 'table_slide_note_input') and self.table_slide_note_input else ''
        except RuntimeError:
            note = ''
        if not note:
            note = table_slide_settings.get('note', '')

        # Get styling settings (safely)
        try:
            font_name = self.table_font_combo.currentText() if hasattr(self, 'table_font_combo') and self.table_font_combo else table_style.get('font_name', 'Calibri')
        except RuntimeError:
            font_name = table_style.get('font_name', 'Calibri')
        
        try:
            font_size = self.table_font_size_spin.value() if hasattr(self, 'table_font_size_spin') and self.table_font_size_spin else table_style.get('font_size', 11)
        except RuntimeError:
            font_size = table_style.get('font_size', 11)
        header_color = QColor(table_style.get('header_color', '#2563EB'))
        header_text_color = QColor(table_style.get('header_text_color', '#FFFFFF'))
        row_color_1 = QColor(table_style.get('row_color_1', '#FFFFFF'))
        row_color_2 = QColor(table_style.get('row_color_2', '#F9FAFB'))
        text_color = QColor(table_style.get('text_color', '#1F2937'))
        bg_color = QColor(table_style.get('background_color', '#FFFFFF'))

        # Get text style settings
        header_bold = table_style.get('header_bold', True)
        header_italic = table_style.get('header_italic', False)
        text_bold = table_style.get('text_bold', False)
        text_italic = table_style.get('text_italic', False)
        header_alignment = table_style.get('header_alignment', 'Center')
        text_alignment = table_style.get('text_alignment', 'Left')

        # Get selected columns
        selected_columns = []
        try:
            if hasattr(self, 'table_columns_list') and self.table_columns_list:
                for i in range(self.table_columns_list.count()):
                    item = self.table_columns_list.item(i)
                    if item and item.checkState() == Qt.CheckState.Checked:
                        selected_columns.append(item.text())
        except RuntimeError:
            pass
        
        if not selected_columns:
            # Use default from settings
            selected_columns = table_slide_settings.get('columns', ['Firma', 'Net Etki', 'Erişim', 'Reklam Eşdeğeri'])

        # Always show at least default columns if none selected
        if not selected_columns:
            selected_columns = ['Firma', 'Net Etki', 'Erişim', 'Reklam Eşdeğeri']

        # Render title
        if title:
            title_font = QFont("Calibri", 32, QFont.Weight.Bold)
            title_item = self.preview_scene.addText(title, title_font)
            title_item.setDefaultTextColor(QColor("#1F2937"))
            title_item.setPos(0.5 * INCH_TO_PIXEL, 0.4 * INCH_TO_PIXEL)

        # Render subtitle
        if subtitle:
            subtitle_font = QFont("Calibri", 16)
            subtitle_item = self.preview_scene.addText(subtitle, subtitle_font)
            subtitle_item.setDefaultTextColor(QColor("#6B7280"))
            subtitle_item.setPos(0.5 * INCH_TO_PIXEL, 1.0 * INCH_TO_PIXEL)

        # Render table preview with proper structure
        table_y = 1.5 * INCH_TO_PIXEL
        table_x = 0.5 * INCH_TO_PIXEL
        table_width = 9.0 * INCH_TO_PIXEL
        num_cols = len(selected_columns)  # Show all selected columns
        col_width = table_width / num_cols if num_cols > 0 else 1.2 * INCH_TO_PIXEL
        row_height = 0.4 * INCH_TO_PIXEL

        # Adjust font size for many columns to fit better
        if num_cols > 7:
            font_size = max(7, font_size - 2)  # Reduce font size for many columns

        # Table background (behind entire table)
        total_height = row_height * 6  # 1 header + 5 data rows
        self.preview_scene.addRect(
            table_x, table_y,
            table_width, total_height,
            bg_color, bg_color
        )

        # Header row background
        self.preview_scene.addRect(
            table_x, table_y,
            table_width, row_height,
            header_color, header_color
        )
        
        # Column headers with borders
        header_font = QFont(font_name, font_size, QFont.Weight.Bold if header_bold else QFont.Weight.Normal)
        header_font.setItalic(header_italic)
        for i, col in enumerate(selected_columns):
            col_x = table_x + i * col_width
            # Cell border
            self.preview_scene.addRect(
                col_x, table_y,
                col_width, row_height,
                QColor("#E5E7EB"), QColor("#E5E7EB")
            )
            # Header text - truncate if too long for cell
            header_text = col
            if num_cols > 7:
                # Truncate long column names when many columns
                max_chars = max(6, int(60 / num_cols))
                if len(col) > max_chars:
                    header_text = col[:max_chars-2] + ".."

            header_item = self.preview_scene.addText(header_text, header_font)
            header_item.setDefaultTextColor(header_text_color)
            header_rect = header_item.boundingRect()
            # Clip text to fit in cell
            if header_rect.width() > col_width - 4:
                header_item.setTextWidth(col_width - 4)
            header_item.setPos(
                col_x + (col_width - min(header_rect.width(), col_width - 4)) / 2,
                table_y + (row_height - header_rect.height()) / 2
            )

        # Data rows (always show at least 5 empty rows)
        sample_rows = 5
        cell_font = QFont(font_name, font_size, QFont.Weight.Bold if text_bold else QFont.Weight.Normal)
        cell_font.setItalic(text_italic)
        for row_idx in range(sample_rows):
            row_y = table_y + row_height + row_idx * row_height
            # Alternate row colors
            row_color = row_color_1 if row_idx % 2 == 0 else row_color_2
            
            # Row background
            self.preview_scene.addRect(
                table_x, row_y,
                table_width, row_height,
                row_color, row_color
            )
            
            # Cell borders and content
            for col_idx in range(num_cols):
                col_x = table_x + col_idx * col_width
                # Cell border
                self.preview_scene.addRect(
                    col_x, row_y,
                    col_width, row_height,
                    QColor("#E5E7EB"), QColor("#E5E7EB")
                )
                
                # Cell text (placeholder or empty)
                if col_idx == 0:
                    cell_text = f"Row {row_idx + 1}" if row_idx < 3 else ""
                    if cell_text:
                        cell_item = self.preview_scene.addText(cell_text, cell_font)
                        cell_item.setDefaultTextColor(text_color)
                        cell_rect = cell_item.boundingRect()
                        cell_item.setPos(
                            col_x + 0.05 * INCH_TO_PIXEL,
                            row_y + (row_height - cell_rect.height()) / 2
                        )

        # Render note if present
        if note:
            note_font = QFont("Calibri", 11)
            note_item = self.preview_scene.addText(f"• {note}", note_font)
            note_item.setDefaultTextColor(QColor("#6B7280"))
            note_item.setPos(0.5 * INCH_TO_PIXEL, 5.5 * INCH_TO_PIXEL)

    def on_title_slide_changed(self):
        """Handle title slide input changes - update preview if on first slide"""
        if self.current_slide_index == 0:
            self.update_preview()

    def _get_selected_table_columns(self):
        """Get list of selected table columns"""
        selected = []
        try:
            if hasattr(self, 'table_columns_list') and self.table_columns_list:
                for i in range(self.table_columns_list.count()):
                    item = self.table_columns_list.item(i)
                    if item and item.checkState() == Qt.CheckState.Checked:
                        selected.append(item.text())
        except RuntimeError:
            pass
        return selected if selected else ['Firma', 'Net Etki', 'Erişim', 'Reklam Eşdeğeri']

    def _get_selected_chart_colors(self):
        """Get list of selected chart colors"""
        selected = []
        try:
            if hasattr(self, 'chart_colors_list') and self.chart_colors_list:
                for i in range(self.chart_colors_list.count()):
                    item = self.chart_colors_list.item(i)
                    if item and item.checkState() == Qt.CheckState.Checked:
                        selected.append(item.text())
        except RuntimeError:
            pass
        return selected if selected else ['#2563EB', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6']

    def on_table_slide_changed(self):
        """Handle table slide input changes - update preview if on table slide"""
        # Save current table styling settings to template_data
        self._save_table_styling_to_template()

        # Update preview if:
        # 1. We're on a table slide (has table component)
        # 2. User has table slide settings configured
        # 3. User is currently editing the Table component
        if self.current_slide_index >= 0:
            slide = self.template_data['slides'][self.current_slide_index]
            components = slide.get('components', [])
            has_table = any(comp.get('type') == 'table' for comp in components)
            has_table_settings = self._has_table_slide_settings()
            is_editing_table = self.selected_component_type == "Table"

            # Update preview if any condition is true
            if has_table or has_table_settings or is_editing_table:
                self.update_preview()

    def _save_table_styling_to_template(self):
        """Save current table styling settings to template_data"""
        if not hasattr(self, 'table_font_combo'):
            return  # Widgets not initialized yet

        try:
            # Ensure table_slide structure exists
            if 'table_slide' not in self.template_data:
                self.template_data['table_slide'] = {}
            if 'style' not in self.template_data['table_slide']:
                self.template_data['table_slide']['style'] = {}

            style = self.template_data['table_slide']['style']

            # Save font settings
            style['font_name'] = self.table_font_combo.currentText()
            style['font_size'] = self.table_font_size_spin.value()

            # Save color settings (already saved by pick_table_color, but ensure they exist)
            if hasattr(self, 'table_header_color_label'):
                style['header_color'] = self.table_header_color_label.text()
            if hasattr(self, 'table_row1_color_label'):
                style['row_color_1'] = self.table_row1_color_label.text()
            if hasattr(self, 'table_row2_color_label'):
                style['row_color_2'] = self.table_row2_color_label.text()
            if hasattr(self, 'table_bg_color_label'):
                style['background_color'] = self.table_bg_color_label.text()

            # Save alignment settings
            if hasattr(self, 'table_header_align_combo'):
                style['header_alignment'] = self.table_header_align_combo.currentText()
            if hasattr(self, 'table_text_align_combo'):
                style['text_alignment'] = self.table_text_align_combo.currentText()

            # Save text style settings
            if hasattr(self, 'table_header_bold_check'):
                style['header_bold'] = self.table_header_bold_check.isChecked()
            if hasattr(self, 'table_header_italic_check'):
                style['header_italic'] = self.table_header_italic_check.isChecked()
            if hasattr(self, 'table_text_bold_check'):
                style['text_bold'] = self.table_text_bold_check.isChecked()
            if hasattr(self, 'table_text_italic_check'):
                style['text_italic'] = self.table_text_italic_check.isChecked()

        except (RuntimeError, AttributeError):
            # Widgets might have been deleted
            pass

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
                    "logo_path": self.template_data.get('logo_path'),
                    "embedded_logo_path": self.template_data.get('embedded_logo_path'),
                    "title_slide": {
                        "title": self.title_slide_title_input.text(),
                        "subtitle": self.title_slide_subtitle_input.text(),
                        "description": self.title_slide_description_input.text(),
                        "logo_position": {"x": 5.0, "y": 1.0},
                        "logo_size": {"width": 2.0, "height": 1.5},
                        "title_position": {"x": 0.5, "y": 2.5},
                        "embedded_logo_position": {"x": 0.5, "y": 6.5},
                        "embedded_logo_size": {"width": 1.5, "height": 0.5}
                    },
                    "table_slide": {
                        "title": self.table_slide_title_input.text() if hasattr(self, 'table_slide_title_input') and self.table_slide_title_input else '',
                        "subtitle": self.table_slide_subtitle_input.text() if hasattr(self, 'table_slide_subtitle_input') and self.table_slide_subtitle_input else '',
                        "columns": self._get_selected_table_columns(),
                        "sort_by": self.table_sort_column_combo.currentText() or None,
                        "ascending": self.table_sort_order_combo.currentText() == "Ascending",
                        "group_by": self.table_group_by_combo.currentText() or None,
                        "note": self.table_slide_note_input.text(),
                        "style": {
                            "font_name": self.table_font_combo.currentText() if hasattr(self, 'table_font_combo') else "Calibri",
                            "font_size": self.table_font_size_spin.value() if hasattr(self, 'table_font_size_spin') else 11,
                            "header_color": self.template_data.get('table_slide', {}).get('style', {}).get('header_color', '#2563EB'),
                            "header_text_color": self.template_data.get('table_slide', {}).get('style', {}).get('header_text_color', '#FFFFFF'),
                            "row_color_1": self.template_data.get('table_slide', {}).get('style', {}).get('row_color_1', '#FFFFFF'),
                            "row_color_2": self.template_data.get('table_slide', {}).get('style', {}).get('row_color_2', '#F9FAFB'),
                            "text_color": self.template_data.get('table_slide', {}).get('style', {}).get('text_color', '#1F2937')
                        }
                    },
                    "chart_slide": {
                        "chart_type": self.chart_type_combo.currentText() if hasattr(self, 'chart_type_combo') and self.chart_type_combo else "column",
                        "title": self.chart_title_input.text() if hasattr(self, 'chart_title_input') and self.chart_title_input else '',
                        "x_column": self.chart_x_column_combo.currentText() if hasattr(self, 'chart_x_column_combo') and self.chart_x_column_combo else "Firma",
                        "y_column": self.chart_y_column_combo.currentText() if hasattr(self, 'chart_y_column_combo') and self.chart_y_column_combo else "Net Etki",
                        "calculation": self.chart_calculation_combo.currentText() if hasattr(self, 'chart_calculation_combo') and self.chart_calculation_combo else "sum",
                        "sort_by": self.chart_sort_column_combo.currentText() if hasattr(self, 'chart_sort_column_combo') and self.chart_sort_column_combo and self.chart_sort_column_combo.currentText() else None,
                        "ascending": self.chart_sort_order_combo.currentText() == "Ascending" if hasattr(self, 'chart_sort_order_combo') and self.chart_sort_order_combo else False,
                        "top_n": self.chart_top_n_spin.value() if hasattr(self, 'chart_top_n_spin') and self.chart_top_n_spin and self.chart_top_n_spin.value() > 0 else None,
                        "style": {
                            "colors": self._get_selected_chart_colors(),
                            "show_values": self.chart_show_values_check.isChecked() if hasattr(self, 'chart_show_values_check') and self.chart_show_values_check else True,
                            "grid": self.chart_show_grid_check.isChecked() if hasattr(self, 'chart_show_grid_check') and self.chart_show_grid_check else True,
                            "legend_position": self.chart_legend_combo.currentText() if hasattr(self, 'chart_legend_combo') and self.chart_legend_combo else "none"
                        }
                    },
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
                    settings = loaded_data['settings']
                    title_slide = settings.get('title_slide', {})
                    table_slide = settings.get('table_slide', {})
                    chart_slide = settings.get('chart_slide', {})
                    
                    self.template_data = {
                        'name': loaded_data['metadata'].get('name', ''),
                        'industry': loaded_data['metadata'].get('industry', ''),
                        'logo_path': settings.get('logo_path'),
                        'embedded_logo_path': settings.get('embedded_logo_path'),
                        'title_slide': {
                            'title': title_slide.get('title', ''),
                            'subtitle': title_slide.get('subtitle', ''),
                            'description': title_slide.get('description', ''),
                            'logo_position': title_slide.get('logo_position', {'x': 5.0, 'y': 1.0}),
                            'logo_size': title_slide.get('logo_size', {'width': 2.0, 'height': 1.5}),
                            'title_position': title_slide.get('title_position', {'x': 0.5, 'y': 2.5}),
                            'embedded_logo_position': title_slide.get('embedded_logo_position', {'x': 0.5, 'y': 6.5}),
                            'embedded_logo_size': title_slide.get('embedded_logo_size', {'width': 1.5, 'height': 0.5})
                        },
                        'table_slide': {
                            'title': table_slide.get('title', 'Yönetici Özeti'),
                            'subtitle': table_slide.get('subtitle', 'Haberlerin Dağılımı'),
                            'columns': table_slide.get('columns', ['Firma', 'Net Etki', 'Erişim', 'Reklam Eşdeğeri']),
                            'sort_by': table_slide.get('sort_by'),
                            'ascending': table_slide.get('ascending', False),
                            'group_by': table_slide.get('group_by'),
                            'note': table_slide.get('note', ''),
                            'style': table_slide.get('style', {
                                'font_name': 'Calibri',
                                'font_size': 11,
                                'header_color': '#2563EB',
                                'header_text_color': '#FFFFFF',
                                'row_color_1': '#FFFFFF',
                                'row_color_2': '#F9FAFB',
                                'text_color': '#1F2937'
                            })
                        },
                        'chart_slide': {
                            'chart_type': chart_slide.get('chart_type', 'column'),
                            'title': chart_slide.get('title', ''),
                            'x_column': chart_slide.get('x_column', 'Firma'),
                            'y_column': chart_slide.get('y_column', 'Net Etki'),
                            'calculation': chart_slide.get('calculation', 'sum'),
                            'sort_by': chart_slide.get('sort_by'),
                            'ascending': chart_slide.get('ascending', False),
                            'top_n': chart_slide.get('top_n'),
                            'style': chart_slide.get('style', {
                                'colors': ['#2563EB', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'],
                                'show_values': True,
                                'grid': True,
                                'legend_position': 'none'
                            })
                        },
                        'colors': {
                            'primary': settings.get('color_scheme', {}).get('primary', '#2563EB'),
                            'secondary': settings.get('color_scheme', {}).get('secondary', '#10B981'),
                            'accent': settings.get('color_scheme', {}).get('accent', '#F59E0B')
                        },
                        'font_family': settings.get('default_font', 'Segoe UI'),
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

                # Update logo paths
                logo_path = self.template_data.get('logo_path')
                if logo_path:
                    import os
                    self.logo_path_label.setText(os.path.basename(logo_path))
                    self.logo_path_label.setStyleSheet("color: #10B981; font-weight: bold;")
                
                embedded_logo_path = self.template_data.get('embedded_logo_path')
                if embedded_logo_path:
                    import os
                    self.embedded_logo_path_label.setText(os.path.basename(embedded_logo_path))
                    self.embedded_logo_path_label.setStyleSheet("color: #10B981; font-weight: bold;")

                # Update title slide settings
                title_slide = self.template_data.get('title_slide', {})
                self.title_slide_title_input.setText(title_slide.get('title', ''))
                self.title_slide_subtitle_input.setText(title_slide.get('subtitle', ''))
                self.title_slide_description_input.setText(title_slide.get('description', ''))

                # Update table slide settings
                table_slide = self.template_data.get('table_slide', {})
                self.table_slide_title_input.setText(table_slide.get('title', 'Yönetici Özeti'))
                self.table_slide_subtitle_input.setText(table_slide.get('subtitle', 'Haberlerin Dağılımı'))
                self.table_slide_note_input.setText(table_slide.get('note', ''))
                
                # Set selected columns
                selected_columns = table_slide.get('columns', [])
                for i in range(self.table_columns_list.count()):
                    item = self.table_columns_list.item(i)
                    if item.text() in selected_columns:
                        item.setCheckState(Qt.CheckState.Checked)
                    else:
                        item.setCheckState(Qt.CheckState.Unchecked)
                
                # Set sort column
                sort_by = table_slide.get('sort_by')
                if sort_by:
                    index = self.table_sort_column_combo.findText(sort_by)
                    if index >= 0:
                        self.table_sort_column_combo.setCurrentIndex(index)
                
                # Set sort order
                ascending = table_slide.get('ascending', False)
                self.table_sort_order_combo.setCurrentIndex(1 if ascending else 0)
                
                # Set group by
                group_by = table_slide.get('group_by')
                if group_by:
                    index = self.table_group_by_combo.findText(group_by)
                    if index >= 0:
                        self.table_group_by_combo.setCurrentIndex(index)
                
                # Load styling settings
                table_style = table_slide.get('style', {})
                if hasattr(self, 'table_font_combo'):
                    font_name = table_style.get('font_name', 'Calibri')
                    index = self.table_font_combo.findText(font_name)
                    if index >= 0:
                        self.table_font_combo.setCurrentIndex(index)
                
                if hasattr(self, 'table_font_size_spin'):
                    self.table_font_size_spin.setValue(table_style.get('font_size', 11))
                
                # Update color buttons
                header_color = table_style.get('header_color', '#2563EB')
                if hasattr(self, 'table_header_color_btn'):
                    self.table_header_color_btn.setStyleSheet(f"background-color: {header_color}; border: 1px solid #E5E7EB;")
                    self.table_header_color_label.setText(header_color)
                
                row1_color = table_style.get('row_color_1', '#FFFFFF')
                if hasattr(self, 'table_row1_color_btn'):
                    self.table_row1_color_btn.setStyleSheet(f"background-color: {row1_color}; border: 1px solid #E5E7EB;")
                    self.table_row1_color_label.setText(row1_color)
                
                row2_color = table_style.get('row_color_2', '#F9FAFB')
                if hasattr(self, 'table_row2_color_btn'):
                    self.table_row2_color_btn.setStyleSheet(f"background-color: {row2_color}; border: 1px solid #E5E7EB;")
                    self.table_row2_color_label.setText(row2_color)
                
                # Update chart slide settings
                chart_slide = self.template_data.get('chart_slide', {})
                if hasattr(self, 'chart_title_input'):
                    self.chart_title_input.setText(chart_slide.get('title', ''))
                if hasattr(self, 'chart_type_combo'):
                    chart_type = chart_slide.get('chart_type', 'column')
                    index = self.chart_type_combo.findText(chart_type)
                    if index >= 0:
                        self.chart_type_combo.setCurrentIndex(index)
                if hasattr(self, 'chart_x_column_combo'):
                    x_column = chart_slide.get('x_column', 'Firma')
                    index = self.chart_x_column_combo.findText(x_column)
                    if index >= 0:
                        self.chart_x_column_combo.setCurrentIndex(index)
                if hasattr(self, 'chart_y_column_combo'):
                    y_column = chart_slide.get('y_column', 'Net Etki')
                    index = self.chart_y_column_combo.findText(y_column)
                    if index >= 0:
                        self.chart_y_column_combo.setCurrentIndex(index)
                if hasattr(self, 'chart_calculation_combo'):
                    calculation = chart_slide.get('calculation', 'sum')
                    index = self.chart_calculation_combo.findText(calculation)
                    if index >= 0:
                        self.chart_calculation_combo.setCurrentIndex(index)
                if hasattr(self, 'chart_sort_column_combo'):
                    sort_by = chart_slide.get('sort_by')
                    if sort_by:
                        index = self.chart_sort_column_combo.findText(sort_by)
                        if index >= 0:
                            self.chart_sort_column_combo.setCurrentIndex(index)
                if hasattr(self, 'chart_sort_order_combo'):
                    ascending = chart_slide.get('ascending', False)
                    self.chart_sort_order_combo.setCurrentIndex(1 if ascending else 0)
                if hasattr(self, 'chart_top_n_spin'):
                    top_n = chart_slide.get('top_n')
                    # Handle None case - convert to 0 (show all)
                    self.chart_top_n_spin.setValue(top_n if top_n is not None else 0)
                if hasattr(self, 'chart_show_values_check'):
                    chart_style = chart_slide.get('style', {})
                    self.chart_show_values_check.setChecked(chart_style.get('show_values', True))
                if hasattr(self, 'chart_show_grid_check'):
                    chart_style = chart_slide.get('style', {})
                    self.chart_show_grid_check.setChecked(chart_style.get('grid', True))
                if hasattr(self, 'chart_legend_combo'):
                    chart_style = chart_slide.get('style', {})
                    legend_pos = chart_style.get('legend_position', 'none')
                    index = self.chart_legend_combo.findText(legend_pos)
                    if index >= 0:
                        self.chart_legend_combo.setCurrentIndex(index)
                if hasattr(self, 'chart_colors_list'):
                    chart_style = chart_slide.get('style', {})
                    selected_colors = chart_style.get('colors', ['#2563EB', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'])
                    for i in range(self.chart_colors_list.count()):
                        item = self.chart_colors_list.item(i)
                        if item.text() in selected_colors:
                            item.setCheckState(Qt.CheckState.Checked)
                        else:
                            item.setCheckState(Qt.CheckState.Unchecked)

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
                            'embedded_logo_path': None,
                            'title_slide': {
                                'title': '',
                                'subtitle': '',
                                'description': ''
                            },
                            'colors': {
                                'primary': '#2563EB',
                                'secondary': '#10B981',
                                'accent': '#F59E0B'
                            },
                            'font_family': 'Segoe UI',
                            'slides': []
                        }
                        # Clear UI fields
                        self.template_name_input.clear()
                        self.logo_path_label.setText("No logo selected")
                        self.logo_path_label.setStyleSheet("color: #6B7280;")
                        self.embedded_logo_path_label.setText("No embedded logo selected")
                        self.embedded_logo_path_label.setStyleSheet("color: #6B7280;")
                        self.title_slide_title_input.clear()
                        self.title_slide_subtitle_input.clear()
                        self.title_slide_description_input.clear()
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
