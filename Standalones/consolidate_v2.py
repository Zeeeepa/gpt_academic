#!/usr/bin/env python3
"""
Standalone Code Consolidation Tool
Creates a single standalone Python file with all dependencies included.

NO EXTERNAL DEPENDENCIES REQUIRED - Uses only Python standard library (ast, os, sys, etc.)
"""

import argparse
import ast
import fnmatch
import json
import logging
import os
import re
import sys
from collections import defaultdict, deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


@dataclass
class ModuleInfo:
    """Information about a Python module"""
    path: str  # Relative path from root
    module_id: str  # Dot-separated module identifier (e.g., "foo.bar.baz")
    imports: List[Tuple[str, List[str]]] = field(default_factory=list)  # (module, names)
    dependencies: Set[str] = field(default_factory=set)  # Module IDs this depends on
    external_imports: Set[str] = field(default_factory=set)  # External package names
    ast_tree: Optional[ast.Module] = None  # Parsed AST
    code: str = ""  # Source code
    symbols: Set[str] = field(default_factory=set)  # Defined symbols (functions, classes)
    
    def __hash__(self):
        return hash(self.module_id)


class StandaloneConsolidator:
    """
    Standalone consolidation tool using only Python standard library.
    
    Features:
    - Two-pass dependency analysis
    - Complete transitive dependency resolution
    - Import deduplication
    - Topological module ordering
    - External package detection
    """
    
    def __init__(self, root_path: str):
        self.root_path = os.path.abspath(root_path)
        self.modules: Dict[str, ModuleInfo] = {}  # module_id -> ModuleInfo
        self.external_packages: Set[str] = set()
        self.stats = {
            'total_files': 0,
            'parsed_files': 0,
            'included_modules': 0,
            'external_packages': 0,
            'parse_errors': 0
        }
        
    def consolidate(self, entry_point: str, output_path: str, mode: str = "complete") -> None:
        """Main consolidation workflow"""
        logger.info(f"=== Standalone Consolidation ===")
        logger.info(f"Root: {self.root_path}")
        logger.info(f"Entry: {entry_point}")
        logger.info(f"Mode: {mode}")
        
        # Phase 1 & 2: Parse and analyze (two-pass)
        logger.info("\n[Phase 1] Discovering Python files...")
        self._discover_python_files()
        logger.info(f"Found {self.stats['total_files']} Python files")
        
        logger.info("\n[Phase 2] Parsing and analyzing dependencies (two-pass)...")
        self._analyze_dependencies()
        logger.info(f"Successfully parsed {self.stats['parsed_files']}/{self.stats['total_files']} files")
        
        # Phase 3: Resolve entry point and collect
        logger.info("\n[Phase 3] Resolving dependencies...")
        entry_module_id = self._resolve_entry_point(entry_point)
        if not entry_module_id:
            raise ValueError(f"Entry point {entry_point} not found")
        
        if mode == "complete":
            # Include ALL local modules
            included = set(self.modules.keys())
        else:
            # Include only reachable from entry
            included = self._collect_transitive_dependencies(entry_module_id)
        
        self.stats['included_modules'] = len(included)
        logger.info(f"Including {self.stats['included_modules']} modules")
        
        # Phase 4: Topological sort
        logger.info("\n[Phase 4] Ordering modules...")
        ordered = self._topological_sort(included)
        logger.info(f"Ordered {len(ordered)} modules")
        
        # Phase 5: Generate output
        logger.info("\n[Phase 5] Generating consolidated code...")
        output = self._generate_output(ordered)
        
        # Phase 6: Write
        logger.info(f"\n[Phase 6] Writing to {output_path}...")
        self._write_output(output_path, output)
        
        # Validate
        logger.info("\nValidating output...")
        if self._validate_syntax(output):
            logger.info("✓ Syntax validation passed")
        else:
            logger.warning("⚠ Syntax validation failed")
        
        # Summary
        logger.info("\n" + "="*70)
        logger.info("Summary:")
        logger.info(f"  Errors: {self.stats['parse_errors']}")
        logger.info(f"  Warnings: {len(self.external_packages)}")
        logger.info(f"  Skipped files: {self.stats['total_files'] - self.stats['parsed_files']}")
        logger.info(f"Detailed report saved to: {output_path.replace('.py', '_report.json')}")
        logger.info("="*70)
        
    def _discover_python_files(self) -> None:
        """Discover all Python files in the project"""
        for root, dirs, files in os.walk(self.root_path):
            # Skip common exclude patterns
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'node_modules', 'venv', '.venv']]
            
            for file in files:
                if file.endswith('.py'):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, self.root_path)
                    module_id = self._path_to_module_id(rel_path)
                    
                    # Read source
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            code = f.read()
                        
                        module = ModuleInfo(
                            path=rel_path,
                            module_id=module_id,
                            code=code
                        )
                        self.modules[module_id] = module
                        self.stats['total_files'] += 1
                        
                    except Exception as e:
                        logger.debug(f"Could not read {rel_path}: {e}")
                        
    def _analyze_dependencies(self) -> None:
        """Two-pass dependency analysis"""
        # Pass 1: Parse AST and register all modules
        logger.info("  Pass 1: Parsing AST for all modules...")
        for module_id, module in list(self.modules.items()):
            try:
                module.ast_tree = ast.parse(module.code)
                self._extract_symbols(module)
                self.stats['parsed_files'] += 1
            except SyntaxError as e:
                logger.debug(f"Syntax error in {module.path}: {e}")
                self.stats['parse_errors'] += 1
                # Keep module but mark as unparseable
                
        # Pass 2: Extract dependencies when ALL modules are known
        logger.info("  Pass 2: Extracting dependencies...")
        for module_id, module in self.modules.items():
            if module.ast_tree:
                self._extract_dependencies(module)
                
    def _extract_symbols(self, module: ModuleInfo) -> None:
        """Extract defined symbols (functions, classes) from module"""
        if not module.ast_tree:
            return
            
        for node in ast.walk(module.ast_tree):
            if isinstance(node, ast.FunctionDef):
                module.symbols.add(node.name)
            elif isinstance(node, ast.ClassDef):
                module.symbols.add(node.name)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        module.symbols.add(target.id)
                        
    def _extract_dependencies(self, module: ModuleInfo) -> None:
        """Extract import dependencies from module"""
        if not module.ast_tree:
            return
            
        for node in ast.walk(module.ast_tree):
            if isinstance(node, ast.Import):
                # import foo, bar
                for alias in node.names:
                    name = alias.name
                    dep_module_id = self._resolve_import(name, module)
                    if dep_module_id:
                        module.dependencies.add(dep_module_id)
                        module.imports.append((None, [name]))
                    else:
                        module.external_imports.add(name.split('.')[0])
                        self.external_packages.add(name.split('.')[0])
                        
            elif isinstance(node, ast.ImportFrom):
                # from foo import bar, baz
                if node.module:
                    dep_module_id = self._resolve_import(node.module, module)
                    if dep_module_id:
                        module.dependencies.add(dep_module_id)
                        names = [alias.name for alias in node.names]
                        module.imports.append((node.module, names))
                    else:
                        module.external_imports.add(node.module.split('.')[0])
                        self.external_packages.add(node.module.split('.')[0])
                        
    def _resolve_import(self, import_name: str, from_module: ModuleInfo) -> Optional[str]:
        """Resolve an import to a local module ID"""
        # Try exact match
        if import_name in self.modules:
            return import_name
            
        # Try with .__init__
        init_id = f"{import_name}.__init__"
        if init_id in self.modules:
            return init_id
            
        # Try relative to current module's package
        parts = from_module.module_id.split('.')
        for i in range(len(parts), 0, -1):
            candidate = '.'.join(parts[:i] + [import_name])
            if candidate in self.modules:
                return candidate
                
        # Try as submodule
        for module_id in self.modules:
            if module_id.startswith(import_name + '.'):
                return module_id
            if module_id.endswith('.' + import_name):
                return module_id
                
        return None
        
    def _path_to_module_id(self, rel_path: str) -> str:
        """Convert file path to module ID"""
        # Remove .py extension
        if rel_path.endswith('.py'):
            rel_path = rel_path[:-3]
        # Convert path separators to dots
        module_id = rel_path.replace(os.sep, '.').replace('/', '.')
        # Handle __init__.py
        if module_id.endswith('.__init__'):
            module_id = module_id[:-9]
        return module_id
        
    def _resolve_entry_point(self, entry_point: str) -> Optional[str]:
        """Find the module ID for the entry point"""
        entry_abs = os.path.abspath(os.path.join(self.root_path, entry_point))
        for module_id, module in self.modules.items():
            module_abs = os.path.abspath(os.path.join(self.root_path, module.path))
            if module_abs == entry_abs:
                return module_id
        return None
        
    def _collect_transitive_dependencies(self, entry_module_id: str) -> Set[str]:
        """Collect all transitive dependencies using BFS"""
        visited = set()
        queue = deque([entry_module_id])
        
        while queue:
            current_id = queue.popleft()
            if current_id in visited:
                continue
            visited.add(current_id)
            
            if current_id in self.modules:
                module = self.modules[current_id]
                for dep_id in module.dependencies:
                    if dep_id not in visited:
                        queue.append(dep_id)
                        
        return visited
        
    def _topological_sort(self, module_ids: Set[str]) -> List[str]:
        """Sort modules in dependency order (dependencies first)"""
        # Build graph
        graph = defaultdict(list)
        in_degree = defaultdict(int)
        
        for module_id in module_ids:
            if module_id not in in_degree:
                in_degree[module_id] = 0
            if module_id in self.modules:
                module = self.modules[module_id]
                for dep_id in module.dependencies:
                    if dep_id in module_ids:
                        graph[dep_id].append(module_id)
                        in_degree[module_id] += 1
                        
        # Kahn's algorithm
        queue = deque([m for m in module_ids if in_degree[m] == 0])
        result = []
        
        while queue:
            current = queue.popleft()
            result.append(current)
            for neighbor in graph[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
                    
        # Handle cycles
        if len(result) < len(module_ids):
            remaining = module_ids - set(result)
            logger.warning(f"Circular dependencies detected for {len(remaining)} modules")
            result.extend(remaining)
            
        return result
        
    def _generate_output(self, ordered_modules: List[str]) -> str:
        """Generate the consolidated output"""
        parts = []
        
        # Header
        parts.append('"""')
        parts.append('Consolidated Standalone Python File')
        parts.append('Generated by Standalone Consolidation Tool')
        parts.append('')
        parts.append(f'Total modules: {len(ordered_modules)}')
        parts.append(f'External packages: {len(self.external_packages)}')
        parts.append('')
        if self.external_packages:
            parts.append('Required external packages:')
            for pkg in sorted(self.external_packages):
                parts.append(f'  - {pkg}')
            parts.append('')
            parts.append('Install with:')
            parts.append(f'  pip install {" ".join(sorted(self.external_packages))}')
        parts.append('"""')
        parts.append('')
        
        # External imports
        if self.external_packages:
            parts.append('# ===== EXTERNAL IMPORTS =====')
            external_imports = set()
            for module_id in ordered_modules:
                if module_id in self.modules:
                    module = self.modules[module_id]
                    for ext in module.external_imports:
                        external_imports.add(f"import {ext}")
            parts.extend(sorted(external_imports))
            parts.append('')
            
        # Module code
        parts.append('# ===== MODULE CODE =====')
        parts.append('')
        
        for module_id in ordered_modules:
            if module_id in self.modules:
                module = self.modules[module_id]
                parts.append(f'# ----- Module: {module_id} ({module.path}) -----')
                
                # Remove local imports from code
                cleaned_code = self._remove_local_imports(module)
                parts.append(cleaned_code)
                parts.append('')
                
        return '\n'.join(parts)
        
    def _remove_local_imports(self, module: ModuleInfo) -> str:
        """Remove imports of local modules that are included in consolidation"""
        if not module.ast_tree:
            return module.code
            
        lines = module.code.split('\n')
        keep_lines = []
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Check if this is an import line that we should remove
            should_remove = False
            
            # Check against module's known local imports
            for import_module, names in module.imports:
                if import_module:
                    # from X import Y
                    if f"from {import_module}" in stripped:
                        should_remove = True
                        break
                else:
                    # import X
                    for name in names:
                        if f"import {name}" in stripped and name in self.modules:
                            should_remove = True
                            break
                            
            if not should_remove:
                keep_lines.append(line)
                
        return '\n'.join(keep_lines)
        
    def _write_output(self, output_path: str, content: str) -> None:
        """Write output and report"""
        # Write consolidated file
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        # Write report
        report = {
            'stats': self.stats,
            'external_packages': sorted(self.external_packages),
            'output_file': output_path,
            'output_size': len(content)
        }
        
        report_path = output_path.replace('.py', '_report.json')
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
            
    def _validate_syntax(self, code: str) -> bool:
        """Validate Python syntax"""
        try:
            ast.parse(code)
            return True
        except SyntaxError as e:
            logger.error(f"Syntax error at line {e.lineno}: {e.msg}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description='Standalone Code Consolidation Tool (No External Dependencies)',
        epilog='''
Examples:
  # Complete consolidation
  %(prog)s /path/to/project --entry-point main.py --output standalone.py
  
  # Reachable only
  %(prog)s /path/to/project --entry-point main.py --output standalone.py --mode reachable
'''
    )
    
    parser.add_argument('root_path', help='Root directory of the project')
    parser.add_argument('--entry-point', '-e', required=True, help='Entry point file (relative to root)')
    parser.add_argument('--output', '-o', required=True, help='Output file path')
    parser.add_argument('--mode', '-m', default='complete',
                       choices=['complete', 'reachable'],
                       help='Inclusion mode: complete (all modules) or reachable (from entry)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    consolidator = StandaloneConsolidator(args.root_path)
    
    try:
        consolidator.consolidate(
            entry_point=args.entry_point,
            output_path=args.output,
            mode=args.mode
        )
        print(f"\n✓ Success! Output written to: {args.output}")
        print(f"  Size: {os.path.getsize(args.output):,} bytes")
        
    except Exception as e:
        logger.error(f"Consolidation failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
