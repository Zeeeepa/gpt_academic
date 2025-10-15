#!/usr/bin/env python3
"""
Script to consolidate Dynamic_Function_Generate.py with all its dependencies
"""

import ast
import os
from pathlib import Path
from typing import Set, Dict, List

def extract_imports(file_path: str) -> List[tuple]:
    """Extract all imports from a Python file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            tree = ast.parse(f.read())
        except:
            return []
    
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module
            for alias in node.names:
                imports.append(('from', module, alias.name))
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(('import', alias.name, None))
    
    return imports

def find_module_file(module_name: str, base_path: str = '.') -> str:
    """Find the file path for a given module"""
    # Convert module name to file path
    parts = module_name.split('.')
    
    # Try as a .py file
    py_file = os.path.join(base_path, *parts) + '.py'
    if os.path.exists(py_file):
        return py_file
    
    # Try as a package __init__.py
    init_file = os.path.join(base_path, *parts, '__init__.py')
    if os.path.exists(init_file):
        return init_file
    
    return None

def read_file_content(file_path: str) -> str:
    """Read file content with proper encoding"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return ""

def get_function_or_class_code(file_path: str, name: str) -> str:
    """Extract specific function or class from a file"""
    content = read_file_content(file_path)
    if not content:
        return ""
    
    try:
        tree = ast.parse(content)
        lines = content.splitlines()
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                if node.name == name:
                    # Get the source code for this node
                    start_line = node.lineno - 1
                    end_line = node.end_lineno
                    return '\n'.join(lines[start_line:end_line])
    except:
        pass
    
    return ""

def consolidate_file(main_file: str, output_file: str):
    """Consolidate a Python file with all its local dependencies"""
    
    print(f"Consolidating {main_file}...")
    
    # Read main file
    main_content = read_file_content(main_file)
    if not main_content:
        print(f"Error: Could not read {main_file}")
        return
    
    # Extract imports
    imports = extract_imports(main_file)
    print(f"Found {len(imports)} imports")
    
    # Separate stdlib and local imports
    local_modules = {}
    stdlib_imports = []
    
    for imp_type, module, name in imports:
        if module and ('toolbox' in module or 'crazy_functions' in module):
            # This is a local import
            module_file = find_module_file(module)
            if module_file:
                print(f"  Found local module: {module} -> {module_file}")
                if name:
                    # Import specific item
                    code = get_function_or_class_code(module_file, name)
                    if code:
                        local_modules[name] = code
                    else:
                        # If can't extract, include whole file
                        local_modules[module] = read_file_content(module_file)
                else:
                    # Import whole module
                    local_modules[module] = read_file_content(module_file)
            else:
                print(f"  Warning: Could not find file for {module}")
        else:
            # Standard library import
            stdlib_imports.append((imp_type, module, name))
    
    # Build consolidated file
    output = []
    
    # Header
    output.append('"""')
    output.append('CONSOLIDATED STANDALONE VERSION OF Dynamic_Function_Generate.py')
    output.append('All dependencies have been inlined.')
    output.append('Generated automatically.')
    output.append('"""')
    output.append('')
    
    # Standard library imports
    output.append('# ===== STANDARD LIBRARY IMPORTS =====')
    seen_imports = set()
    for imp_type, module, name in stdlib_imports:
        if imp_type == 'import':
            imp_str = f'import {module}'
        else:
            imp_str = f'from {module} import {name}'
        
        if imp_str not in seen_imports:
            output.append(imp_str)
            seen_imports.add(imp_str)
    output.append('')
    
    # Inlined local code
    output.append('# ===== INLINED LOCAL DEPENDENCIES =====')
    for name, code in local_modules.items():
        output.append(f'\n# ----- From {name} -----')
        output.append(code)
        output.append('')
    
    # Main file content (with imports removed)
    output.append('# ===== MAIN CODE =====')
    
    # Parse main content and remove import statements
    try:
        tree = ast.parse(main_content)
        lines = main_content.splitlines()
        
        # Find lines with imports to skip
        import_lines = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                import_lines.update(range(node.lineno - 1, node.end_lineno))
        
        # Add non-import lines
        for i, line in enumerate(lines):
            if i not in import_lines:
                output.append(line)
    except:
        # If parsing fails, just include everything after imports
        in_imports = True
        for line in main_content.splitlines():
            if in_imports and not line.startswith(('import ', 'from ')) and line.strip() and not line.strip().startswith('#'):
                in_imports = False
            if not in_imports:
                output.append(line)
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))
    
    print(f"\nConsolidated file written to: {output_file}")
    print(f"Total lines: {len(output)}")

if __name__ == "__main__":
    consolidate_file(
        'crazy_functions/Dynamic_Function_Generate.py',
        'Dynamic_Function_Generate_STANDALONE.py'
    )

