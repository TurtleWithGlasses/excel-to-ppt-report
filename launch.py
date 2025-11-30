"""
ReportForge Launcher - Ensures fresh code loading
"""
import sys
import os
import shutil

# Disable bytecode caching BEFORE any imports
sys.dont_write_bytecode = True

# Clear existing cache
print("Clearing Python cache...")
cache_dirs = []
for root, dirs, files in os.walk('.'):
    if '__pycache__' in dirs:
        cache_path = os.path.join(root, '__pycache__')
        cache_dirs.append(cache_path)

for cache_dir in cache_dirs:
    try:
        shutil.rmtree(cache_dir)
        print(f"Deleted: {cache_dir}")
    except Exception as e:
        print(f"Could not delete {cache_dir}: {e}")

print("Cache cleared! Starting application...\n")

# Now import and run main
from main import main
main()
