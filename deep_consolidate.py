#!/usr/bin/env python3
"""
Deep consolidation script that recursively includes ALL code from imported modules
"""

import ast
import os
import re
from typing import Set, Dict, List, Tuple

class DependencyResolver:
    def __init__(self, base_path='.'):
        self.base_path = base_path
        self.processed_modules = set()
        self.module_contents = {}
        self.all_stdlib_imports = set()
        
    def find_module_file(self, module_name: str) -> str:
        """Find the file path for a given module"""
        if not module_name:
            return None
            
        parts = module_name.split('.')
        
        # Try as a .py file
        py_file = os.path.join(self.base_path, *parts) + '.py'
        if os.path.exists(py_file):
            return py_file
        
        # Try as a package __init__.py
        init_file = os.path.join(self.base_path, *parts, '__init__.py')
        if os.path.exists(init_file):
            return init_file
        
        return None
    
    def read_file(self, file_path: str) -> str:
        """Read file content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Warning: Could not read {file_path}: {e}")
            return ""
    
    def extract_imports(self, content: str) -> List[Tuple[str, str, str]]:
        """Extract imports from source code"""
        try:
            tree = ast.parse(content)
        except:
            return []
        
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports.append(('from', module, alias.name))
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(('import', alias.name, None))
        
        return imports
    
    def is_local_module(self, module_name: str) -> bool:
        """Check if module is local (not stdlib)"""
        if not module_name:
            return False
        
        # Check if it's a local module
        local_prefixes = ['toolbox', 'crazy_functions', 'request_llms', 'themes']
        for prefix in local_prefixes:
            if module_name.startswith(prefix):
                return True
        
        # Check if file exists
        return self.find_module_file(module_name) is not None
    
    def process_module(self, module_name: str, depth=0):
        """Recursively process a module and all its dependencies"""
        if not module_name or module_name in self.processed_modules:
            return
        
        indent = "  " * depth
        print(f"{indent}Processing: {module_name}")
        
        # Mark as processed first to avoid infinite recursion
        self.processed_modules.add(module_name)
        
        # Find module file
        module_file = self.find_module_file(module_name)
        if not module_file:
            print(f"{indent}  -> File not found")
            return
        
        # Read content
        content = self.read_file(module_file)
        if not content:
            print(f"{indent}  -> Empty or unreadable")
            return
        
        # Store content
        self.module_contents[module_name] = {
            'file': module_file,
            'content': content
        }
        
        # Extract and process imports
        imports = self.extract_imports(content)
        for imp_type, imp_module, imp_name in imports:
            if self.is_local_module(imp_module):
                # Recursively process local imports
                self.process_module(imp_module, depth + 1)
            else:
                # Track stdlib imports
                if imp_type == 'import':
                    self.all_stdlib_imports.add(f"import {imp_module}")
                else:
                    self.all_stdlib_imports.add(f"from {imp_module} import {imp_name}")
    
    def remove_imports_from_code(self, content: str) -> str:
        """Remove import statements from code"""
        lines = content.splitlines()
        result = []
        skip_until_blank = False
        
        for line in lines:
            stripped = line.strip()
            
            # Skip import lines
            if stripped.startswith('import ') or stripped.startswith('from '):
                skip_until_blank = True
                continue
            
            # Skip blank lines after imports
            if skip_until_blank:
                if not stripped:
                    continue
                else:
                    skip_until_blank = False
            
            result.append(line)
        
        return '\n'.join(result)
    
    def build_standalone_file(self, main_file: str, output_file: str):
        """Build a standalone file with all dependencies"""
        print(f"\n{'='*70}")
        print(f"Building standalone version of: {main_file}")
        print(f"{'='*70}\n")
        
        # Read main file
        main_content = self.read_file(main_file)
        if not main_content:
            print(f"Error: Could not read {main_file}")
            return
        
        # Process main file and dependencies
        main_module = main_file.replace('.py', '').replace('/', '.')
        self.process_module(main_module)
        
        # Also process direct imports from main file
        imports = self.extract_imports(main_content)
        for imp_type, imp_module, imp_name in imports:
            if self.is_local_module(imp_module):
                self.process_module(imp_module)
        
        print(f"\n{'='*70}")
        print(f"Processed {len(self.processed_modules)} modules")
        print(f"{'='*70}\n")
        
        # Build output
        output = []
        
        # Header
        output.append('#!/usr/bin/env python3')
        output.append('"""')
        output.append('CONSOLIDATED STANDALONE VERSION')
        output.append(f'Original file: {main_file}')
        output.append('')
        output.append('ALL dependencies have been recursively inlined.')
        output.append('This file is completely self-contained and requires no external modules')
        output.append('except for Python standard library.')
        output.append('')
        output.append('Auto-generated by deep_consolidate.py')
        output.append('"""')
        output.append('')
        
        # Standard library imports
        output.append('#' + '='*70)
        output.append('# STANDARD LIBRARY IMPORTS')
        output.append('#' + '='*70)
        output.append('')
        
        for imp in sorted(self.all_stdlib_imports):
            output.append(imp)
        
        output.append('')
        output.append('')
        
        # Inlined module contents
        output.append('#' + '='*70)
        output.append('# INLINED LOCAL DEPENDENCIES')
        output.append('#' + '='*70)
        output.append('')
        
        # Sort modules by dependency order (simple heuristic: reverse order of discovery)
        for module_name in list(self.processed_modules)[::-1]:
            if module_name == main_module:
                continue
                
            module_info = self.module_contents.get(module_name)
            if not module_info:
                continue
            
            output.append('')
            output.append('#' + '-'*70)
            output.append(f'# MODULE: {module_name}')
            output.append(f'# SOURCE: {module_info["file"]}')
            output.append('#' + '-'*70)
            output.append('')
            
            # Remove imports from module code
            clean_content = self.remove_imports_from_code(module_info['content'])
            output.append(clean_content)
            output.append('')
        
        # Main file content
        output.append('')
        output.append('#' + '='*70)
        output.append('# MAIN CODE')
        output.append(f'# SOURCE: {main_file}')
        output.append('#' + '='*70)
        output.append('')
        
        clean_main = self.remove_imports_from_code(main_content)
        output.append(clean_main)
        
        # Write output
        output_content = '\n'.join(output)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output_content)
        
        print(f"\n{'='*70}")
        print(f"✅ SUCCESS!")
        print(f"{'='*70}")
        print(f"Output file: {output_file}")
        print(f"Total lines: {len(output)}")
        print(f"File size: {len(output_content)} bytes")
        print(f"Modules included: {len(self.processed_modules)}")
        print(f"{'='*70}\n")

if __name__ == "__main__":
    resolver = DependencyResolver(base_path='.')
    resolver.build_standalone_file(
        main_file='crazy_functions/Dynamic_Function_Generate.py',
        output_file='Dynamic_Function_Generate_STANDALONE.py'
    )

