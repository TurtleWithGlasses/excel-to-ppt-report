"""
ReportForge - Main Application Entry Point
Universal PowerPoint Report Generation System

Usage:
    python main.py              # Launch Main App (Report Generator)
    python main.py --builder    # Launch Template Builder
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from gui.main_window import MainWindow
from gui.template_builder import TemplateBuilder


def main():
    """Main application entry point"""
    # Create Qt Application
    app = QApplication(sys.argv)
    app.setApplicationName("ReportForge")
    app.setOrganizationName("ReportForge")

    # Set application-wide style
    app.setStyle('Fusion')

    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == '--builder':
        # Launch Template Builder
        window = TemplateBuilder()
        window.setWindowTitle("ReportForge - Template Builder")
    else:
        # Launch Main App (Report Generator)
        window = MainWindow()
        window.setWindowTitle("ReportForge - Report Generator")

    # Show window in full-screen mode
    window.showMaximized()

    # Start event loop
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
