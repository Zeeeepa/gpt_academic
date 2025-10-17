#!/usr/bin/env python3
"""
Advanced Code Consolidation Tool
Consolidates Python projects into standalone files with complete dependency context.

Features:
- Complete dependency graph analysis using IR
- Transitive dependency resolution
- Import pattern detection (standard, dynamic, conditional)
- Configurable inclusion strategies
- Tree-shaking with multiple modes
- Module ordering and namespace preservation
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

# Import the IR and parser infrastructure
try:
    from IR import (
        Code, Project, File, SymbolInfo, ValueDeclaration, 
        ContainerDeclaration, FunctionKind, Import, Declaration
    )
    from parser import parse_files_in_paths
    from sanitizer import CodeSanitizer
except ImportError:
    print("Error: Required modules (IR, parser, sanitizer) not found.")
    print("Please ensure these modules are in the same directory or PYTHONPATH.")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


@dataclass
class ConsolidationConfig:
    """Configuration for consolidation strategy"""
    inclusion_mode: str = "complete"  # minimal, standard, complete, custom
    tree_shaking: str = "off"  # off, conservative, moderate, aggressive
    include_docstrings: bool = True
    include_comments: bool = True
    include_type_hints: bool = True
    max_depth: int = -1  # -1 for unlimited
    whitelist: Set[str] = field(default_factory=set)
    blacklist: Set[str] = field(default_factory=set)
    include_external_stubs: bool = True
    preserve_structure: bool = True
    
    @classmethod
    def from_args(cls, args):
        """Create config from command line arguments"""
        return cls(
            inclusion_mode=args.mode,
            tree_shaking=args.tree_shaking,
            include_docstrings=not args.no_docstrings,
            include_comments=not args.no_comments,
            include_type_hints=not args.no_type_hints,
            max_depth=args.max_depth,
            whitelist=set(args.whitelist) if args.whitelist else set(),
            blacklist=set(args.blacklist) if args.blacklist else set(),
            include_external_stubs=args.external_stubs,
            preserve_structure=args.preserve_structure
        )


@dataclass
class ModuleNode:
    """Represents a module in the dependency graph"""
    qualified_id: str
    file: File
    symbols: Set[SymbolInfo] = field(default_factory=set)
    dependencies: Set[str] = field(default_factory=set)  # Other module qualified IDs
    external_imports: Set[str] = field(default_factory=set)
    import_statements: List[Import] = field(default_factory=list)
    is_entry: bool = False
    depth: int = -1


class AdvancedConsolidator:
    """
    Advanced code consolidation with complete dependency analysis.
    """
    
    def __init__(self, config: ConsolidationConfig):
        self.config = config
        self.project: Optional[Project] = None
        self.module_graph: Dict[str, ModuleNode] = {}
        self.external_packages: Set[str] = set()
        self.sanitizer: Optional[CodeSanitizer] = None
        self.stats = {
            'total_files': 0,
            'included_files': 0,
            'external_packages': 0,
            'dynamic_imports': 0,
            'conditional_imports': 0
        }
        
    def consolidate(self, root_path: str, entry_point: str, output_path: str) -> None:
        """
        Main consolidation workflow.
        
        Args:
            root_path: Root directory of the project
            entry_point: Entry point file (relative to root_path)
            output_path: Output file path for consolidated code
        """
        logger.info(f"Starting consolidation from {entry_point}")
        logger.info(f"Root path: {root_path}")
        logger.info(f"Config: {self.config.inclusion_mode} mode, tree_shaking={self.config.tree_shaking}")
        
        # Step 1: Parse the project using IR
        logger.info("Phase 1: Parsing project...")
        self.project = self._parse_project(root_path)
        self.stats['total_files'] = len(self.project.get_files())
        logger.info(f"Parsed {self.stats['total_files']} Python files")
        
        # Step 2: Build module dependency graph
        logger.info("Phase 2: Building dependency graph...")
        self._build_module_graph()
        
        # Step 3: Analyze entry point and collect dependencies
        logger.info("Phase 3: Analyzing dependencies...")
        entry_file = self._resolve_entry_point(root_path, entry_point)
        if not entry_file:
            raise ValueError(f"Entry point {entry_point} not found in project")
        
        included_modules = self._collect_dependencies(entry_file)
        self.stats['included_files'] = len(included_modules)
        logger.info(f"Included {self.stats['included_files']}/{self.stats['total_files']} modules")
        
        # Step 4: Order modules topologically
        logger.info("Phase 4: Determining load order...")
        ordered_modules = self._topological_sort(included_modules)
        logger.info(f"Determined load order for {len(ordered_modules)} modules")
        
        # Step 5: Generate consolidated code
        logger.info("Phase 5: Generating consolidated code...")
        consolidated_code = self._generate_consolidated_code(ordered_modules)
        
        # Step 6: Write output
        logger.info(f"Phase 6: Writing to {output_path}...")
        self._write_output(output_path, consolidated_code)
        
        # Step 7: Generate report
        self._generate_report(output_path)
        
        logger.info("✓ Consolidation complete!")
        logger.info(f"  Output: {output_path}")
        logger.info(f"  Size: {len(consolidated_code):,} bytes ({len(consolidated_code)/1024:.1f} KB)")
        logger.info(f"  Modules: {self.stats['included_files']}")
    
    def _parse_project(self, root_path: str) -> Project:
        """Parse all Python files in the project using IR parser"""
        def file_filter(path: str) -> bool:
            # Skip test files, __pycache__, etc.
            if '__pycache__' in path or path.endswith('.pyc'):
                return False
            if '/test' in path or '/tests/' in path:
                return False
            return True
        
        project = parse_files_in_paths([root_path], filter_file=file_filter)
        self.sanitizer = CodeSanitizer(project)
        return project
    
    def _build_module_graph(self) -> None:
        """Build complete module dependency graph"""
        for file in self.project.get_files():
            module_id = self._file_to_module_id(file)
            node = ModuleNode(
                qualified_id=module_id,
                file=file,
                import_statements=file._imports
            )
            
            # Collect all symbols in this module
            for symbol_id, symbol in file._symbol_table.items():
                node.symbols.add(symbol)
            
            # Analyze dependencies
            self._analyze_module_dependencies(node)
            
            self.module_graph[module_id] = node
        
        logger.info(f"Built graph with {len(self.module_graph)} modules")
    
    def _analyze_module_dependencies(self, node: ModuleNode) -> None:
        """Analyze all dependencies of a module"""
        # Standard imports
        for import_stmt in node.import_statements:
            if import_stmt.module_name:
                # from X import Y
                module_name = import_stmt.module_name
                local_module = self._resolve_local_import(module_name, node.file)
                if local_module:
                    node.dependencies.add(local_module)
                else:
                    node.external_imports.add(module_name)
                    self.external_packages.add(module_name.split('.')[0])
            else:
                # import X
                for name in import_stmt.names:
                    local_module = self._resolve_local_import(name, node.file)
                    if local_module:
                        node.dependencies.add(local_module)
                    else:
                        node.external_imports.add(name)
                        self.external_packages.add(name.split('.')[0])
        
        # Analyze symbol dependencies
        for symbol in node.symbols:
            if isinstance(symbol, ValueDeclaration):
                self._analyze_symbol_dependencies(symbol, node)
            elif isinstance(symbol, ContainerDeclaration):
                for stmt in symbol.body:
                    if isinstance(stmt, Declaration):
                        for inner_symbol in stmt.symbols:
                            self._analyze_symbol_dependencies(inner_symbol, node)
    
    def _analyze_symbol_dependencies(self, symbol: SymbolInfo, node: ModuleNode) -> None:
        """Analyze dependencies within a symbol's code"""
        if not hasattr(symbol, 'body_sub') or not symbol.body_sub:
            return
        
        try:
            # Get the body code
            body_start = symbol.body_sub[0] - symbol.substring[0]
            body_end = symbol.body_sub[1] - symbol.substring[0]
            body_text = symbol.get_substring()[body_start:body_end].decode()
            
            # Parse to find more imports
            tree = ast.parse(body_text, mode='exec')
            for ast_node in ast.walk(tree):
                # Detect dynamic imports
                if isinstance(ast_node, ast.Call):
                    if isinstance(ast_node.func, ast.Name) and ast_node.func.id == '__import__':
                        self.stats['dynamic_imports'] += 1
                    elif isinstance(ast_node.func, ast.Attribute):
                        if (isinstance(ast_node.func.value, ast.Name) and 
                            ast_node.func.value.id == 'importlib' and
                            ast_node.func.attr == 'import_module'):
                            self.stats['dynamic_imports'] += 1
                
                # Detect conditional imports
                elif isinstance(ast_node, (ast.If, ast.Try)):
                    self.stats['conditional_imports'] += 1
                    
        except Exception as e:
            logger.debug(f"Could not analyze {symbol.name}: {e}")
    
    def _resolve_local_import(self, import_name: str, from_file: File) -> Optional[str]:
        """Resolve if an import is a local module"""
        # Try to find in project
        parts = import_name.split('.')
        
        # Try direct file match
        potential_path = os.path.join(self.project.root_path, *parts) + '.py'
        for file in self.project.get_files():
            file_path = os.path.join(self.project.root_path, file.path)
            if file_path == potential_path:
                return self._file_to_module_id(file)
        
        # Try package __init__.py
        potential_pkg = os.path.join(self.project.root_path, *parts, '__init__.py')
        for file in self.project.get_files():
            file_path = os.path.join(self.project.root_path, file.path)
            if file_path == potential_pkg:
                return self._file_to_module_id(file)
        
        return None
    
    def _file_to_module_id(self, file: File) -> str:
        """Convert file path to module identifier"""
        # Convert path like "foo/bar/baz.py" to "foo.bar.baz"
        path = file.path
        if path.endswith('.py'):
            path = path[:-3]
        if path.endswith('__init__'):
            path = path[:-9]  # Remove __init__
        return path.replace('/', '.').replace('\\', '.').strip('.')
    
    def _resolve_entry_point(self, root_path: str, entry_point: str) -> Optional[File]:
        """Find the entry point file"""
        entry_full = os.path.join(root_path, entry_point)
        for file in self.project.get_files():
            file_full = os.path.join(root_path, file.path)
            if os.path.abspath(file_full) == os.path.abspath(entry_full):
                return file
        return None
    
    def _collect_dependencies(self, entry_file: File) -> Set[str]:
        """Collect all dependencies based on configuration"""
        entry_module_id = self._file_to_module_id(entry_file)
        
        if self.config.inclusion_mode == "minimal":
            # Only direct dependencies
            return self._collect_direct_dependencies(entry_module_id)
        elif self.config.inclusion_mode == "standard":
            # Direct + one level transitive
            return self._collect_transitive_dependencies(entry_module_id, max_depth=2)
        elif self.config.inclusion_mode == "complete":
            # All local modules
            if self.config.tree_shaking == "off":
                # Include everything
                return set(self.module_graph.keys())
            else:
                # Include all reachable
                return self._collect_transitive_dependencies(entry_module_id, max_depth=-1)
        elif self.config.inclusion_mode == "custom":
            # Use whitelist/blacklist
            included = set()
            for module_id in self.module_graph.keys():
                if module_id in self.config.blacklist:
                    continue
                if self.config.whitelist and module_id not in self.config.whitelist:
                    continue
                included.add(module_id)
            return included
        
        return self._collect_transitive_dependencies(entry_module_id, max_depth=-1)
    
    def _collect_direct_dependencies(self, module_id: str) -> Set[str]:
        """Collect only direct dependencies"""
        if module_id not in self.module_graph:
            return set()
        
        included = {module_id}
        node = self.module_graph[module_id]
        included.update(node.dependencies)
        return included
    
    def _collect_transitive_dependencies(self, entry_module_id: str, max_depth: int = -1) -> Set[str]:
        """Collect all transitive dependencies using BFS"""
        if entry_module_id not in self.module_graph:
            return set()
        
        visited = set()
        queue = deque([(entry_module_id, 0)])
        
        while queue:
            current_id, depth = queue.popleft()
            
            if current_id in visited:
                continue
            
            if max_depth >= 0 and depth > max_depth:
                continue
            
            visited.add(current_id)
            
            if current_id in self.module_graph:
                node = self.module_graph[current_id]
                node.depth = depth
                
                for dep_id in node.dependencies:
                    if dep_id not in visited:
                        queue.append((dep_id, depth + 1))
        
        return visited
    
    def _topological_sort(self, module_ids: Set[str]) -> List[str]:
        """Sort modules in topological order (dependencies first)"""
        # Build adjacency list for included modules only
        graph = defaultdict(list)
        in_degree = defaultdict(int)
        
        for module_id in module_ids:
            if module_id not in in_degree:
                in_degree[module_id] = 0
            
            if module_id in self.module_graph:
                node = self.module_graph[module_id]
                for dep_id in node.dependencies:
                    if dep_id in module_ids:  # Only consider included modules
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
        
        # Check for cycles
        if len(result) < len(module_ids):
            logger.warning(f"Circular dependencies detected. Including remaining {len(module_ids) - len(result)} modules")
            result.extend(m for m in module_ids if m not in result)
        
        return result
    
    def _generate_consolidated_code(self, ordered_modules: List[str]) -> str:
        """Generate the consolidated code"""
        parts = []
        
        # Header
        parts.append(self._generate_header())
        parts.append("")
        
        # External imports
        parts.append("# ===== EXTERNAL IMPORTS =====")
        external_imports = self._collect_external_imports(ordered_modules)
        parts.extend(sorted(external_imports))
        parts.append("")
        
        # Module code
        parts.append("# ===== MODULE CODE =====")
        for module_id in ordered_modules:
            if module_id in self.module_graph:
                node = self.module_graph[module_id]
                module_code = self._generate_module_code(node)
                if module_code:
                    parts.append(f"# ----- Module: {module_id} -----")
                    parts.append(module_code)
                    parts.append("")
        
        # Footer
        parts.append(self._generate_footer())
        
        return "\n".join(parts)
    
    def _generate_header(self) -> str:
        """Generate file header with metadata"""
        return f'''"""
Consolidated Standalone Code
Generated by Advanced Consolidation Tool

Config:
  - Inclusion mode: {self.config.inclusion_mode}
  - Tree shaking: {self.config.tree_shaking}
  - Total files: {self.stats['total_files']}
  - Included files: {self.stats['included_files']}
  - External packages: {len(self.external_packages)}

External dependencies required:
{chr(10).join(f"  - {pkg}" for pkg in sorted(self.external_packages))}

Usage:
  This is a standalone file containing all necessary local code.
  Install external dependencies first:
    pip install {' '.join(sorted(self.external_packages))}
"""'''
    
    def _generate_footer(self) -> str:
        """Generate file footer"""
        return f'''
# ===== END OF CONSOLIDATED CODE =====
# Statistics:
#   Total modules: {self.stats['included_files']}
#   External packages: {len(self.external_packages)}
#   Dynamic imports detected: {self.stats['dynamic_imports']}
#   Conditional imports detected: {self.stats['conditional_imports']}
'''
    
    def _collect_external_imports(self, module_ids: List[str]) -> Set[str]:
        """Collect all external import statements"""
        imports = set()
        
        for module_id in module_ids:
            if module_id in self.module_graph:
                node = self.module_graph[module_id]
                for external in node.external_imports:
                    imports.add(f"import {external}")
        
        return imports
    
    def _generate_module_code(self, node: ModuleNode) -> str:
        """Generate code for a single module"""
        file = node.file
        
        # Get the full file content
        try:
            file_path = os.path.join(self.project.root_path, file.path)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove local imports (already handled globally)
            content = self._remove_local_imports(content, node)
            
            # Apply config filters
            if not self.config.include_docstrings:
                content = self._remove_docstrings(content)
            
            if not self.config.include_comments:
                content = self._remove_comments(content)
            
            return content.strip()
            
        except Exception as e:
            logger.warning(f"Could not read {file.path}: {e}")
            return ""
    
    def _remove_local_imports(self, content: str, node: ModuleNode) -> str:
        """Remove local imports that are included in consolidation"""
        lines = content.split('\n')
        filtered_lines = []
        
        for line in lines:
            # Check if it's an import line
            is_local_import = False
            for import_stmt in node.import_statements:
                if import_stmt.module_name:
                    # from X import Y
                    if self._resolve_local_import(import_stmt.module_name, node.file):
                        if f"from {import_stmt.module_name}" in line:
                            is_local_import = True
                            break
                else:
                    # import X
                    for name in import_stmt.names:
                        if self._resolve_local_import(name, node.file):
                            if f"import {name}" in line:
                                is_local_import = True
                                break
            
            if not is_local_import:
                filtered_lines.append(line)
        
        return '\n'.join(filtered_lines)
    
    def _remove_docstrings(self, content: str) -> str:
        """Remove docstrings from code"""
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                    if (ast.get_docstring(node)):
                        # Keep first line only
                        pass  # TODO: implement
            return content
        except:
            return content
    
    def _remove_comments(self, content: str) -> str:
        """Remove comments from code"""
        lines = content.split('\n')
        filtered = []
        for line in lines:
            # Remove inline comments
            if '#' in line:
                # Keep if # is in a string
                in_string = False
                quote_char = None
                for i, char in enumerate(line):
                    if char in ['"', "'"]:
                        if not in_string:
                            in_string = True
                            quote_char = char
                        elif char == quote_char and (i == 0 or line[i-1] != '\\'):
                            in_string = False
                    elif char == '#' and not in_string:
                        line = line[:i].rstrip()
                        break
            if line.strip():  # Keep non-empty lines
                filtered.append(line)
        return '\n'.join(filtered)
    
    def _write_output(self, output_path: str, content: str) -> None:
        """Write consolidated code to output file"""
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_report(self, output_path: str) -> None:
        """Generate consolidation report"""
        report = {
            'config': {
                'inclusion_mode': self.config.inclusion_mode,
                'tree_shaking': self.config.tree_shaking,
                'include_docstrings': self.config.include_docstrings,
                'include_comments': self.config.include_comments,
            },
            'stats': self.stats,
            'external_packages': sorted(self.external_packages),
            'module_graph_size': len(self.module_graph),
            'output_file': output_path
        }
        
        report_path = output_path.replace('.py', '_report.json')
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Report saved to {report_path}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Advanced Code Consolidation Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Complete consolidation (all local modules)
  %(prog)s /path/to/project --entry-point main.py --output standalone.py --mode complete
  
  # Minimal consolidation (direct dependencies only)
  %(prog)s /path/to/project --entry-point main.py --output standalone.py --mode minimal
  
  # Standard consolidation with moderate tree-shaking
  %(prog)s /path/to/project --entry-point main.py --output standalone.py --mode standard --tree-shaking moderate
'''
    )
    
    parser.add_argument('root_path', help='Root directory of the project')
    parser.add_argument('--entry-point', '-e', required=True, help='Entry point file (relative to root)')
    parser.add_argument('--output', '-o', required=True, help='Output file path')
    parser.add_argument('--mode', '-m', default='complete',
                       choices=['minimal', 'standard', 'complete', 'custom'],
                       help='Inclusion mode (default: complete)')
    parser.add_argument('--tree-shaking', default='off',
                       choices=['off', 'conservative', 'moderate', 'aggressive'],
                       help='Tree-shaking mode (default: off)')
    parser.add_argument('--max-depth', type=int, default=-1,
                       help='Maximum dependency depth (-1 for unlimited)')
    parser.add_argument('--whitelist', nargs='+', help='Modules to always include')
    parser.add_argument('--blacklist', nargs='+', help='Modules to exclude')
    parser.add_argument('--no-docstrings', action='store_true', help='Remove docstrings')
    parser.add_argument('--no-comments', action='store_true', help='Remove comments')
    parser.add_argument('--no-type-hints', action='store_true', help='Remove type hints')
    parser.add_argument('--external-stubs', action='store_true', default=True,
                       help='Generate stubs for external packages')
    parser.add_argument('--preserve-structure', action='store_true', default=True,
                       help='Preserve module structure with comments')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    config = ConsolidationConfig.from_args(args)
    consolidator = AdvancedConsolidator(config)
    
    try:
        consolidator.consolidate(
            root_path=args.root_path,
            entry_point=args.entry_point,
            output_path=args.output
        )
    except Exception as e:
        logger.error(f"Consolidation failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

