"""
Quick script to make code compatible with both PyQt6 and PySide6
Run this once to update all imports
"""

import os
import re

files_to_update = [
    'main.py',
    'gui/main_window.py',
    'gui/template_builder.py'
]

pyqt6_imports = '''from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QFileDialog, QComboBox, QProgressBar,
    QGraphicsView, QGraphicsScene, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPainter, QPen, QPainterPath'''

compatible_imports = '''try:
    from PyQt6.QtWidgets import (
        QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
        QLabel, QLineEdit, QFileDialog, QComboBox, QProgressBar,
        QGraphicsView, QGraphicsScene, QMessageBox, QFrame
    )
    from PyQt6.QtCore import Qt, QThread, pyqtSignal
    from PyQt6.QtGui import QFont, QColor, QPainter, QPen, QPainterPath
except ImportError:
    from PySide6.QtWidgets import (
        QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
        QLabel, QLineEdit, QFileDialog, QComboBox, QProgressBar,
        QGraphicsView, QGraphicsScene, QMessageBox, QFrame
    )
    from PySide6.QtCore import Qt, QThread, Signal as pyqtSignal
    from PySide6.QtGui import QFont, QColor, QPainter, QPen, QPainterPath'''

main_py_old = '''from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt'''

main_py_new = '''try:
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import Qt
except ImportError:
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import Qt'''

def update_file(filepath, old_text, new_text):
    """Update imports in a file"""
    if not os.path.exists(filepath):
        print(f"⚠️  {filepath} not found, skipping...")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if old_text in content:
        new_content = content.replace(old_text, new_text)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ Updated {filepath}")
        return True
    else:
        print(f"ℹ️  {filepath} - no changes needed")
        return False

print("=" * 60)
print("Qt Imports Compatibility Fixer")
print("=" * 60)
print("\nMaking your code compatible with both PyQt6 and PySide6...\n")

# Update main.py
update_file('main.py', main_py_old, main_py_new)

# Update GUI files
for gui_file in ['gui/main_window.py', 'gui/template_builder.py']:
    # Try to update PyQt6 imports
    update_file(gui_file, pyqt6_imports, compatible_imports)

print("\n" + "=" * 60)
print("✨ Done! Now install PySide6:")
print("   pip install PySide6==6.6.1")
print("\nThen run: python main.py")
print("=" * 60)
