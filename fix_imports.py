# Скрипт для удаления неиспользуемых импортов
import os

files_to_fix = {
    'src/utils.py': ['import os'],
    'src/views.py': ['import json', 'from typing import Optional'],
    'tests/test_services.py': ['from datetime import datetime', 'import pytest'],
    'tests/test_views.py': ['from datetime import datetime', 'from unittest.mock import MagicMock']
}

for filepath, imports_to_remove in files_to_fix.items():
    if os.path.exists(filepath):
        print(f'Fixing {filepath}')
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        new_lines = []
        for line in lines:
            if not any(line.strip().startswith(imp) for imp in imports_to_remove):
                new_lines.append(line)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f'Removed imports from {filepath}')
    else:
        print(f'File not found: {filepath}')
