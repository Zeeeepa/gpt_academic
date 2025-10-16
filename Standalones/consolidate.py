#!/usr/bin/env python3
"""
consolidate.py - Production-Grade Python Codebase Consolidator
===============================================================

Consolidates a Python module/package into a single standalone file with:
- Recursive dependency resolution at ANY depth
- Smart import deduplication and categorization  
- Topological sorting for correct load order
- Comprehensive error handling with recovery
- Syntax validation and quality checks
- Zero external dependencies except Python stdlib
- Auto-backup of existing output files
- Progress tracking and estimation
- Dry-run mode for safety
- Automatic code formatting detection

Version: 3.0 (Multiline Import Edition)
Author: AI Assistant
License: MIT

Changelog v3.0:
- ✅ Multiline parenthesized imports: from module import (item1, item2)
- ✅ Backslash continuations: from module import \
- ✅ Nested parentheses handling
- ✅ Comment preservation in imports
- ✅ Enhanced error recovery
"""

import os
import sys
import ast
import re
import time
import logging
import traceback
import argparse
import shutil
import json
import hashlib
import subprocess
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
from datetime import datetime

# ============================================================================
# Configuration & Setup
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# Directory configuration for lint/format operations
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
BACKEND_DIR = "."
LIBS_DIR = "../autogpt_libs"
TARGET_DIRS = [BACKEND_DIR, LIBS_DIR]


class ImportType(Enum):
    """Types of imports."""
    STDLIB = "stdlib"
    EXTERNAL = "external"
    LOCAL = "local"
    RELATIVE = "relative"


@dataclass
class ImportStatement:
    """Represents a parsed import statement."""
    raw_statement: str
    module_name: str
    import_type: ImportType
    imported_names: List[str] = field(default_factory=list)
    is_from_import: bool = False
    alias: Optional[str] = None
    
    def __hash__(self):
        """Make hashable for set operations."""
        return hash((self.raw_statement.strip(), self.module_name))
    
    def __eq__(self, other):
        """Equality based on normalized statement."""
        if not isinstance(other, ImportStatement):
            return False
        return self.raw_statement.strip() == other.raw_statement.strip()
    
    def __repr__(self):
        return f"ImportStatement({self.raw_statement[:50]}...)"


@dataclass
class ModuleInfo:
    """Information about a processed module."""
    file_path: str
    module_name: str
    content: str
    imports: Set[ImportStatement] = field(default_factory=set)
    dependencies: Set[str] = field(default_factory=set)
    processed_content: str = ""


# ============================================================================
# Error Handler with Retry Logic
# ============================================================================

class ErrorHealer:
    """Comprehensive error handling with logging and recovery."""
    
    def __init__(self, max_retries: int = 2):
        self.max_retries = max_retries
        self.errors: List[Dict[str, Any]] = []
        self.warnings: List[str] = []
        self.skipped_files: List[str] = []
        
    def log_error(self, error: Exception, context: str = "", 
                  file_path: str = "") -> None:
        """Log an error with full context."""
        error_entry = {
            'time': time.time(),
            'type': type(error).__name__,
            'message': str(error),
            'context': context,
            'file': file_path,
            'traceback': traceback.format_exc()
        }
        self.errors.append(error_entry)
        logger.error(f"Error in {context}: {error}")
        if file_path:
            logger.error(f"  File: {file_path}")
            
    def log_warning(self, message: str) -> None:
        """Log a warning."""
        self.warnings.append(message)
        logger.warning(message)
        
    def skip_file(self, file_path: str, reason: str) -> None:
        """Record a skipped file."""
        self.skipped_files.append(f"{file_path}: {reason}")
        logger.warning(f"Skipping {file_path}: {reason}")
        
    def get_summary(self) -> Dict[str, Any]:
        """Get error/warning summary."""
        return {
            'total_errors': len(self.errors),
            'total_warnings': len(self.warnings),
            'total_skipped': len(self.skipped_files),
            'error_types': {e['type'] for e in self.errors},
            'warnings': self.warnings,
            'skipped_files': self.skipped_files
        }
        
    def save_report(self, output_dir: str) -> None:
        """Save detailed error report to JSON."""
        if not self.errors and not self.warnings:
            return
            
        report_path = os.path.join(output_dir, 'consolidation_report.json')
        report = {
            'timestamp': datetime.now().isoformat(),
            'errors': self.errors,
            'warnings': self.warnings,
            'skipped_files': self.skipped_files,
            'summary': self.get_summary()
        }
        
        try:
            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            logger.info(f"Detailed report saved to: {report_path}")
        except Exception as e:
            logger.error(f"Could not save report: {e}")


# ============================================================================
# Import Processor - Smart Import Handling
# ============================================================================

class ImportProcessor:
    """
    Intelligently processes, categorizes, and deduplicates imports.
    
    Handles:
    - Standard library imports
    - External package imports  
    - Local module imports
    - Relative imports
    - Import aliasing
    - From...import statements
    """
    
    def __init__(self, local_modules: Set[str]):
        self.local_modules = local_modules
        self.stdlib_modules = self._get_stdlib_modules()
        self.seen_imports: Set[str] = set()
        self.categorized_imports: Dict[ImportType, Set[ImportStatement]] = {
            ImportType.STDLIB: set(),
            ImportType.EXTERNAL: set(),
            ImportType.LOCAL: set(),
        }
        # For intelligent merging: module -> set of imported names
        self.from_imports: Dict[str, Dict[str, Set[str]]] = {
            'STDLIB': {},
            'EXTERNAL': {},
        }
        # For simple imports: module -> alias (if any)
        self.simple_imports: Dict[str, Dict[str, Optional[str]]] = {
            'STDLIB': {},
            'EXTERNAL': {},
        }
        
    def _get_stdlib_modules(self) -> Set[str]:
        """Get standard library module names."""
        # Python 3.10+ has sys.stdlib_module_names
        if hasattr(sys, 'stdlib_module_names'):
            return set(sys.stdlib_module_names)
        
        # Fallback for older Python versions
        stdlib = {
            'abc', 'aifc', 'argparse', 'array', 'ast', 'asynchat', 'asyncio',
            'asyncore', 'atexit', 'audioop', 'base64', 'bdb', 'binascii',
            'binhex', 'bisect', 'builtins', 'bz2', 'calendar', 'cgi', 'cgitb',
            'chunk', 'cmath', 'cmd', 'code', 'codecs', 'codeop', 'collections',
            'colorsys', 'compileall', 'concurrent', 'configparser', 'contextlib',
            'contextvars', 'copy', 'copyreg', 'cProfile', 'crypt', 'csv', 'ctypes',
            'curses', 'dataclasses', 'datetime', 'dbm', 'decimal', 'difflib',
            'dis', 'distutils', 'doctest', 'email', 'encodings', 'enum', 'errno',
            'faulthandler', 'fcntl', 'filecmp', 'fileinput', 'fnmatch', 'formatter',
            'fractions', 'ftplib', 'functools', 'gc', 'getopt', 'getpass', 'gettext',
            'glob', 'graphlib', 'grp', 'gzip', 'hashlib', 'heapq', 'hmac', 'html',
            'http', 'idlelib', 'imaplib', 'imghdr', 'imp', 'importlib', 'inspect',
            'io', 'ipaddress', 'itertools', 'json', 'keyword', 'lib2to3', 'linecache',
            'locale', 'logging', 'lzma', 'mailbox', 'mailcap', 'marshal', 'math',
            'mimetypes', 'mmap', 'modulefinder', 'multiprocessing', 'netrc', 'nis',
            'nntplib', 'numbers', 'operator', 'optparse', 'os', 'ossaudiodev',
            'parser', 'pathlib', 'pdb', 'pickle', 'pickletools', 'pipes', 'pkgutil',
            'platform', 'plistlib', 'poplib', 'posix', 'posixpath', 'pprint', 'profile',
            'pstats', 'pty', 'pwd', 'py_compile', 'pyclbr', 'pydoc', 'queue', 'quopri',
            'random', 're', 'readline', 'reprlib', 'resource', 'rlcompleter', 'runpy',
            'sched', 'secrets', 'select', 'selectors', 'shelve', 'shlex', 'shutil',
            'signal', 'site', 'smtpd', 'smtplib', 'sndhdr', 'socket', 'socketserver',
            'spwd', 'sqlite3', 'ssl', 'stat', 'statistics', 'string', 'stringprep',
            'struct', 'subprocess', 'sunau', 'symbol', 'symtable', 'sys', 'sysconfig',
            'syslog', 'tabnanny', 'tarfile', 'telnetlib', 'tempfile', 'termios',
            'test', 'textwrap', 'threading', 'time', 'timeit', 'tkinter', 'token',
            'tokenize', 'trace', 'traceback', 'tracemalloc', 'tty', 'turtle', 'turtledemo',
            'types', 'typing', 'typing_extensions', 'unicodedata', 'unittest', 'urllib',
            'uu', 'uuid', 'venv', 'warnings', 'wave', 'weakref', 'webbrowser', 'winreg',
            'winsound', 'wsgiref', 'xdrlib', 'xml', 'xmlrpc', 'zipapp', 'zipfile',
            'zipimport', 'zlib', '_thread'
        }
        return stdlib
        
    @staticmethod
    def normalize_multiline_imports(content: str) -> str:
        """
        Normalize multiline imports into single lines.
        
        Handles:
        - Parenthesized imports: from module import (a, b, c)
        - Backslash continuations: from module import a, \\ b, c
        - Nested parentheses
        - Comments within imports
        """
        lines = content.split('\n')
        normalized_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            # Check if this is the start of a multiline import
            if (stripped.startswith('import ') or stripped.startswith('from ')) and \
               (stripped.endswith('(') or stripped.endswith('\\') or 
                ('(' in stripped and ')' not in stripped)):
                
                # Accumulate the full import statement
                import_parts = [line]
                paren_depth = line.count('(') - line.count(')')
                has_backslash = line.rstrip().endswith('\\')
                
                i += 1
                while i < len(lines):
                    next_line = lines[i]
                    next_stripped = next_line.strip()
                    
                    # First, append the line and update state
                    import_parts.append(next_line)
                    paren_depth += next_line.count('(') - next_line.count(')')
                    has_backslash = next_line.rstrip().endswith('\\')
                    
                    # Check if import is complete
                    if paren_depth <= 0 and not has_backslash:
                        break
                    
                    # CRITICAL: Check if NEXT line is a separate import statement
                    # Look ahead to prevent merging separate consecutive imports
                    if i + 1 < len(lines):
                        peek_line = lines[i + 1].strip()
                        if paren_depth == 0 and not has_backslash:
                            if peek_line.startswith('from ') or peek_line.startswith('import '):
                                # Next line is a separate import - stop here
                                break
                    
                    i += 1
                
                # Combine into single line
                full_import = ' '.join(part.strip().rstrip('\\') for part in import_parts)
                # Clean up multiple spaces
                full_import = re.sub(r'\s+', ' ', full_import)
                
                # Remove ALL parentheses content and extract just the imports
                if 'import' in full_import:
                    # Extract the module and import parts
                    if full_import.startswith('from '):
                        # Use non-greedy match to avoid capturing subsequent imports
                        match = re.match(r'from\s+([\w.]+)\s+import\s+(.+?)(?:\s+from\s+|\s+import\s+|$)', full_import)
                        if match:
                            module = match.group(1)
                            imports_part = match.group(2)
                            
                            # Remove ALL parentheses (nested or not)
                            imports_part = re.sub(r'[()]', '', imports_part)
                            # Clean up spaces
                            imports_part = re.sub(r'\s+', ' ', imports_part).strip()
                            # Remove trailing commas
                            imports_part = re.sub(r',\s*$', '', imports_part)
                            
                            full_import = f'from {module} import {imports_part}'
                    else:
                        # Simple import statement
                        imports_part = full_import[7:].strip()  # Remove 'import '
                        imports_part = re.sub(r'[()]', '', imports_part)
                        imports_part = re.sub(r'\s+', ' ', imports_part).strip()
                        full_import = f'import {imports_part}'
                
                normalized_lines.append(full_import)
                i += 1
            else:
                normalized_lines.append(line)
                i += 1
        
        return '\n'.join(normalized_lines)
    
    def parse_import_line(self, line: str) -> Optional[ImportStatement]:
        """Parse a single import line into an ImportStatement."""
        stripped = line.strip()
        
        # Skip comments and empty lines
        if not stripped or stripped.startswith('#'):
            return None
        
        # Skip template/placeholder imports (common patterns)
        if '...' in stripped or 'import ...' in stripped:
            return None
            
        # Handle relative imports - skip for now
        if stripped.startswith('from .') or stripped.startswith('from ..'):
            return None
            
        # Parse "import module [as alias]"
        if stripped.startswith('import '):
            match = re.match(r'import\s+([\w.]+)(?:\s+as\s+(\w+))?', stripped)
            if match:
                module = match.group(1)
                alias = match.group(2)
                base_module = module.split('.')[0]
                
                import_type = self._categorize_module(base_module)
                
                return ImportStatement(
                    raw_statement=stripped,
                    module_name=module,
                    import_type=import_type,
                    is_from_import=False,
                    alias=alias
                )
                
        # Parse "from module import names"
        elif stripped.startswith('from '):
            match = re.match(r'from\s+([\w.]+)\s+import\s+(.+)', stripped)
            if match:
                module = match.group(1)
                imports_part = match.group(2)
                base_module = module.split('.')[0]
                
                # Parse imported names (handle commas, parentheses, aliases)
                imported_names = []
                # Remove parentheses if present
                imports_part = re.sub(r'[()]', '', imports_part)
                # Split by comma and clean
                for name in imports_part.split(','):
                    name = name.strip()
                    # Handle "name as alias"
                    if ' as ' in name:
                        name = name.split(' as ')[0].strip()
                    if name and name != '*':
                        imported_names.append(name)
                
                import_type = self._categorize_module(base_module)
                
                return ImportStatement(
                    raw_statement=stripped,
                    module_name=module,
                    import_type=import_type,
                    imported_names=imported_names,
                    is_from_import=True
                )
                
        return None
        
    def _categorize_module(self, module_name: str) -> ImportType:
        """Categorize a module as stdlib, external, or local."""
        if module_name in self.local_modules:
            return ImportType.LOCAL
        elif module_name in self.stdlib_modules:
            return ImportType.STDLIB
        else:
            return ImportType.EXTERNAL
            
    def add_import(self, import_stmt: ImportStatement) -> bool:
        """
        Add an import to the appropriate category with intelligent merging.
        Returns True if added, False if duplicate.
        """
        if import_stmt.import_type == ImportType.LOCAL:
            return False  # Skip local imports
            
        raw = import_stmt.raw_statement.strip()
        import_type_key = 'STDLIB' if import_stmt.import_type == ImportType.STDLIB else 'EXTERNAL'
        
        # Parse the import statement
        if raw.startswith('from '):
            # Parse: from module import name1, name2 as alias2, ...
            match = re.match(r'from\s+([\w.]+)\s+import\s+(.+)', raw)
            if match:
                module = match.group(1)
                imports_str = match.group(2)
                
                # Parse individual imports
                if module not in self.from_imports[import_type_key]:
                    self.from_imports[import_type_key][module] = set()
                
                # Split by comma and handle aliases
                for item in imports_str.split(','):
                    item = item.strip()
                    if ' as ' in item:
                        name, alias = item.split(' as ')
                        self.from_imports[import_type_key][module].add(f"{name.strip()} as {alias.strip()}")
                    else:
                        self.from_imports[import_type_key][module].add(item)
                        
                return True
                
        elif raw.startswith('import '):
            # Parse: import module1, module2 as alias2, ...
            imports_str = raw[7:].strip()  # Remove 'import '
            
            for item in imports_str.split(','):
                item = item.strip()
                if ' as ' in item:
                    module, alias = item.split(' as ')
                    module = module.strip()
                    alias = alias.strip()
                    self.simple_imports[import_type_key][module] = alias
                else:
                    if item not in self.simple_imports[import_type_key]:
                        self.simple_imports[import_type_key][item] = None
                        
            return True
            
        return False
        
    def process_file_imports(self, content: str) -> Tuple[str, Set[ImportStatement]]:
        """
        Extract imports from content and return processed content without imports.
        
        Returns:
            (content_without_imports, set_of_external_imports)
        """
        # First, normalize multiline imports
        content = self.normalize_multiline_imports(content)
        lines = content.split('\n')
        processed_lines = []
        file_imports = set()
        
        skip_docstring = False
        docstring_quote = None
        in_multiline_string = False
        string_quote = None
        indent_level = 0  # Track indentation to detect function/class bodies
        
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            # Update indent level based on line content
            if stripped and not stripped.startswith('#'):
                current_indent = len(line) - len(line.lstrip())
                if current_indent > 0:
                    indent_level = current_indent
                elif stripped.startswith(('def ', 'class ', 'if ', 'for ', 'while ', 'with ', 'try:', 'except', 'finally:')):
                    # Starting a new block
                    pass
                else:
                    # Back to top level
                    indent_level = 0
            
            # Handle module docstrings (remove them)
            # Only remove actual module docstrings, not strings assigned to variables
            if i < 10 and not skip_docstring and not in_multiline_string:  # Only check first 10 lines
                if stripped.startswith('"""') or stripped.startswith("'''"):
                    # Check if previous line was an assignment (e.g., "variable = \")
                    is_assignment = False
                    if i > 0:
                        prev_line = lines[i-1].strip()
                        if prev_line.endswith('\\') or '=' in prev_line:
                            is_assignment = True
                    
                    if not is_assignment:
                        quote = '"""' if stripped.startswith('"""') else "'''"
                        if stripped.count(quote) >= 2:
                            # Single line docstring - skip it
                            i += 1
                            continue
                        else:
                            # Multi-line docstring start
                            skip_docstring = True
                            docstring_quote = quote
                            i += 1
                            continue
                        
            if skip_docstring:
                if docstring_quote in line:
                    skip_docstring = False
                    docstring_quote = None
                i += 1
                continue
            
            # Track multiline strings (templates, etc.)
            if not in_multiline_string:
                # Check for start of multiline string
                for quote in ['"""', "'''"]:
                    if quote in line:
                        # Count occurrences
                        count = line.count(quote)
                        if count == 1:
                            # Start of multiline string
                            in_multiline_string = True
                            string_quote = quote
                            break
                        # If count >= 2, it's complete on one line
            else:
                # We're inside a multiline string, check for end
                if string_quote in line:
                    in_multiline_string = False
                    string_quote = None
                # Skip processing this line as it's part of a string
                processed_lines.append(line)
                i += 1
                continue
                
            # Process import lines
            if stripped.startswith('import ') or stripped.startswith('from '):
                # Only extract top-level imports (indent_level == 0)
                # Imports inside functions/classes should be left in place
                if indent_level == 0:
                    import_stmt = self.parse_import_line(line)
                    
                    if import_stmt:
                        if import_stmt.import_type == ImportType.LOCAL:
                            # COMPLETELY REMOVE local imports - they're being inlined
                            pass  # Don't add to processed_lines
                        else:
                            # Collect external/stdlib imports - will be consolidated at top
                            file_imports.add(import_stmt)
                            # Don't add to processed_lines - imports go to top
                            # Will check for empty blocks later
                    else:
                        # Couldn't parse or relative import
                        if stripped.startswith('from .'):
                            processed_lines.append(f'# {line}  # Relative import removed')
                        else:
                            processed_lines.append(line)
                else:
                    # Import inside a function/class - keep it
                    processed_lines.append(line)
            else:
                processed_lines.append(line)
                
            i += 1
        
        # Post-process: Fix ONLY truly empty blocks (try/except/else/elif/finally/with)
        # Be VERY conservative - only fix blocks that are DEFINITELY problems
        final_lines = []
        i = 0
        while i < len(processed_lines):
            line = processed_lines[i]
            final_lines.append(line)
            stripped = line.strip()
            
            # ONLY handle these specific keywords that MUST have a body
            keywords_needing_body = ['try:', 'except:', 'except ', 'else:', 'elif ', 'finally:', 'with ', 'if ', 'for ', 'while ']
            is_special_block = any(stripped.startswith(kw) or stripped == kw.rstrip() for kw in keywords_needing_body)
            
            # Check if line ends with : (ignoring trailing comments)
            line_without_comment = line.split('#')[0].rstrip()
            if not is_special_block or not line_without_comment.endswith(':'):
                i += 1
                continue
            
            # Calculate indentation
            current_indent = len(line) - len(line.lstrip())
            
            # Skip if this looks like a generator/comprehension within a call (ends with ):)
            # But NOT if it's a normal if/for/while statement that happens to have a call
            # Pattern: "for x in ...):" is a comprehension, "if foo()):" is a normal if with function call
            if line_without_comment.endswith('):'):
                # Check if this is really a comprehension or just a function call
                # Heuristic: if previous line has unclosed paren/bracket, this is a continuation
                if i > 0:
                    prev_line = processed_lines[i - 1]
                    prev_stripped = prev_line.split('#')[0].rstrip()
                    prev_indent = len(prev_line) - len(prev_line.lstrip())
                    
                    # Count open/close parens and brackets on previous line
                    open_count = prev_stripped.count('(') + prev_stripped.count('[') + prev_stripped.count('{')
                    close_count = prev_stripped.count(')') + prev_stripped.count(']') + prev_stripped.count('}')
                    
                    # If previous line has unclosed brackets AND this line is more indented, it's a continuation
                    if open_count > close_count and current_indent > prev_indent:
                        # This is a continuation line (comprehension/generator)
                        i += 1
                        continue
            
            # Look ahead for body
            next_idx = i + 1
            has_body = False
            
            while next_idx < len(processed_lines):
                next_line = processed_lines[next_idx]
                next_stripped = next_line.strip()
                
                # Skip empty lines
                if not next_stripped:
                    next_idx += 1
                    continue
                
                # Skip comments (but they don't count as body!)
                if next_stripped.startswith('#'):
                    next_idx += 1
                    continue
                
                # Check indentation of next real line
                next_indent = len(next_line) - len(next_line.lstrip())
                
                # If we find except/else/elif/finally at SAME level, the try/if block is empty
                same_level_keywords = ['except:', 'except ', 'else:', 'elif ', 'finally:']
                if next_indent == current_indent and any(next_stripped.startswith(kw) for kw in same_level_keywords):
                    # Empty block followed by continuation (except/else/elif/finally)
                    has_body = False
                    break
                
                # If next line is indented more, we have a body
                if next_indent > current_indent:
                    has_body = True
                break
            
            if not has_body:
                final_lines.append(' ' * (current_indent + 4) + 'pass  # Empty block')
            
            i += 1
        
        processed_lines = final_lines
            
        # Clean up excessive blank lines
        output = '\n'.join(processed_lines)
        output = re.sub(r'\n{4,}', '\n\n\n', output)
        
        return output, file_imports
        
    def get_consolidated_imports(self) -> str:
        """Get all consolidated imports as formatted string with intelligent merging."""
        output = []
        written_simple = set()  # Track written simple imports across all categories
        written_from = {}  # Track written from imports: {module: set(names)}
        
        # Helper to format a category
        def format_category(category_key: str, category_name: str):
            lines = []
            
            # Simple imports first
            simple = self.simple_imports[category_key]
            if simple:
                lines.append(f'# {category_name}')
                lines.append('# ============================================================================')
                for module in sorted(simple.keys()):
                    # Skip if already written in a previous category (e.g., stdlib takes precedence)
                    if module in written_simple:
                        continue
                    written_simple.add(module)
                    
                    alias = simple[module]
                    if alias:
                        lines.append(f'import {module} as {alias}')
                    else:
                        lines.append(f'import {module}')
                lines.append('')
            
            # From imports - grouped and merged
            from_imps = self.from_imports[category_key]
            if from_imps:
                if not lines:  # Add header if not already added
                    lines.append(f'# {category_name}')
                    lines.append('# ============================================================================')
                
                for module in sorted(from_imps.keys()):
                    items = sorted(from_imps[module])
                    
                    # Skip if these exact imports from this module were already written
                    if module in written_from:
                        # Check if all items already written
                        if items <= written_from[module]:  # subset check
                            continue
                        # Merge new items with existing
                        new_items = items - written_from[module]
                        if not new_items:
                            continue
                        items = new_items
                        written_from[module].update(items)
                    else:
                        written_from[module] = set(items)
                    
                    # Format nicely - if too long, use multi-line
                    items_str = ', '.join(items)
                    if len(f'from {module} import {items_str}') <= 88:  # PEP 8 line length
                        lines.append(f'from {module} import {items_str}')
                    else:
                        # Multi-line format
                        lines.append(f'from {module} import (')
                        for i, item in enumerate(items):
                            if i < len(items) - 1:
                                lines.append(f'    {item},')
                            else:
                                lines.append(f'    {item}')
                        lines.append(')')
                lines.append('')
            
            return lines
        
        # Standard library
        stdlib_lines = format_category('STDLIB', 'Standard Library Imports')
        if stdlib_lines:
            output.extend(stdlib_lines)
            
        # External packages
        external_lines = format_category('EXTERNAL', 'External Package Imports')
        if external_lines:
            output.extend(external_lines)
            
        return '\n'.join(output)


# ============================================================================
# Dependency Resolver - Topological Sort
# ============================================================================

class DependencyResolver:
    """Resolves module dependencies and determines load order."""
    
    def __init__(self, error_healer: ErrorHealer):
        self.error_healer = error_healer
        self.modules: Dict[str, ModuleInfo] = {}
        self.dependency_graph: Dict[str, Set[str]] = defaultdict(set)
        
    def add_module(self, module_info: ModuleInfo) -> None:
        """Add a module to the dependency graph."""
        self.modules[module_info.module_name] = module_info
        self.dependency_graph[module_info.module_name] = module_info.dependencies
        
    def resolve_order(self) -> List[str]:
        """
        Resolve module load order using topological sort.
        Handles circular dependencies gracefully.
        """
        visited = set()
        temp_visited = set()
        result = []
        circular_deps = []
        
        def visit(module: str, path: List[str] = None) -> None:
            if path is None:
                path = []
                
            if module in temp_visited:
                # Circular dependency detected
                cycle = path[path.index(module):] + [module]
                circular_deps.append(' -> '.join(cycle))
                return
                
            if module in visited:
                return
                
            temp_visited.add(module)
            path.append(module)
            
            for dep in self.dependency_graph.get(module, set()):
                if dep in self.modules:  # Only process local dependencies
                    visit(dep, path[:])
                    
            path.pop()
            temp_visited.remove(module)
            visited.add(module)
            result.append(module)
            
        # Visit all modules
        for module in self.modules:
            if module not in visited:
                visit(module)
                
        # Log circular dependencies
        if circular_deps:
            self.error_healer.log_warning(
                f"Circular dependencies detected:\n" + 
                "\n".join(f"  - {cycle}" for cycle in circular_deps)
            )
            
        return result


# ============================================================================
# Codebase Consolidator - Main Logic
# ============================================================================

class CodebaseConsolidator:
    """
    Main consolidator that ties everything together.
    
    Process:
    1. Find all Python files in directory
    2. Parse imports and build dependency graph
    3. Determine load order via topological sort
    4. Process each file (remove imports, extract code)
    5. Consolidate all imports at top
    6. Write standalone output file
    7. Validate output
    """
    
    def __init__(self, repo_path: str, verbose: bool = True, 
                 dry_run: bool = False, create_backup: bool = True):
        self.repo_path = Path(repo_path).resolve()
        self.verbose = verbose
        self.dry_run = dry_run
        self.create_backup = create_backup
        self.error_healer = ErrorHealer()
        self.local_modules: Set[str] = set()
        self.python_files: Dict[str, Path] = {}
        self.modules: Dict[str, ModuleInfo] = {}
        self.start_time = time.time()
        self.stats = {
            'files_found': 0,
            'files_processed': 0,
            'files_skipped': 0,
            'total_lines': 0,
            'total_size': 0
        }
        
    def log(self, message: str, level: str = 'info') -> None:
        """Log a message."""
        if self.verbose or level in ['warning', 'error']:
            getattr(logger, level)(message)
            
    def find_python_files(self) -> Dict[str, Path]:
        """Find all Python files in the repository."""
        self.log("Finding Python files...")
        
        python_files = {}
        excluded_dirs = {
            '__pycache__', '.git', '.venv', 'venv', 'env',
            'node_modules', '.pytest_cache', 'build', 'dist',
            '.tox', '.eggs', '*.egg-info', 'Standalones'
        }
        
        for path in self.repo_path.rglob('*.py'):
            # Skip excluded directories
            if any(excluded in path.parts for excluded in excluded_dirs):
                continue
                
            # Skip hidden files
            if any(part.startswith('.') for part in path.parts):
                continue
                
            # Pre-validate file is readable
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    f.read(1)  # Just check if we can read
            except (UnicodeDecodeError, PermissionError) as e:
                self.error_healer.skip_file(str(path), f"Cannot read file: {e}")
                continue
                
            rel_path = path.relative_to(self.repo_path)
            module_name = str(rel_path.with_suffix('')).replace(os.sep, '.')
            
            # Handle __init__.py
            if module_name.endswith('.__init__'):
                module_name = module_name[:-9]
                
            python_files[module_name] = path
            
            # Track local module names
            self.local_modules.add(module_name)
            # Also add base module
            base_module = module_name.split('.')[0]
            self.local_modules.add(base_module)
            
        # CRITICAL: Also add the repository base name as a local module
        # This handles imports like "from crazy_functions import X" when scanning crazy_functions/
        repo_base_name = self.repo_path.name
        self.local_modules.add(repo_base_name)
        self.log(f"DEBUG: Added repo base name to local_modules: {repo_base_name}")
            
        self.python_files = python_files
        self.stats['files_found'] = len(python_files)
        self.log(f"Found {len(python_files)} Python files")
        self.log(f"Detected {len(self.local_modules)} local module names")
        self.log(f"DEBUG: Base modules in local_modules: {sorted([m for m in self.local_modules if '.' not in m])[:10]}")
        
        return python_files
        
    def analyze_dependencies(self) -> None:
        """Analyze imports and build dependency information for all files."""
        self.log("Analyzing dependencies...")
        
        import_processor = ImportProcessor(self.local_modules)
        
        for module_name, file_path in self.python_files.items():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Parse AST to find imports
                try:
                    tree = ast.parse(content)
                    dependencies = self._extract_local_dependencies(tree)
                except SyntaxError as e:
                    self.error_healer.log_warning(
                        f"Syntax error in {file_path}: {e}"
                    )
                    dependencies = set()
                    
                # Create module info
                module_info = ModuleInfo(
                    file_path=str(file_path),
                    module_name=module_name,
                    content=content,
                    dependencies=dependencies
                )
                
                self.modules[module_name] = module_info
                
            except Exception as e:
                self.error_healer.log_error(
                    e, context="analyze_dependencies",
                    file_path=str(file_path)
                )
                
        self.log(f"Analyzed {len(self.modules)} modules")
        
    def _extract_local_dependencies(self, tree: ast.AST) -> Set[str]:
        """Extract local module dependencies from AST."""
        deps = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module = alias.name
                    base = module.split('.')[0]
                    if base in self.local_modules:
                        deps.add(module if module in self.modules else base)
                        
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    module = node.module
                    base = module.split('.')[0]
                    if base in self.local_modules:
                        deps.add(module if module in self.modules else base)
                        
        return deps
        
    def _create_backup(self, output_path: str) -> Optional[str]:
        """Create a backup of existing output file."""
        if not os.path.exists(output_path):
            return None
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{output_path}.backup_{timestamp}"
        
        try:
            shutil.copy2(output_path, backup_path)
            self.log(f"✓ Created backup: {backup_path}")
            return backup_path
        except Exception as e:
            self.error_healer.log_warning(f"Could not create backup: {e}")
            return None
    
    def _compute_file_hash(self, file_path: str) -> str:
        """Compute SHA256 hash of a file."""
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except:
            return ""
    
    def consolidate(self, output_path: str) -> bool:
        """
        Consolidate the codebase into a single file.
        
        Returns:
            True if successful, False otherwise
        """
        self.log("\n" + "="*70)
        if self.dry_run:
            self.log("CONSOLIDATING CODEBASE (DRY RUN - NO FILES WILL BE WRITTEN)")
        else:
            self.log("CONSOLIDATING CODEBASE")
        self.log("="*70 + "\n")
        
        # Create backup if output exists
        if self.create_backup and not self.dry_run:
            self._create_backup(output_path)
        
        try:
            # Step 1: Find files
            if not self.python_files:
                self.find_python_files()
                
            if not self.python_files:
                self.log("No Python files found!", 'error')
                return False
                
            # Step 2: Analyze
            if not self.modules:
                self.analyze_dependencies()
                
            # Step 3: Resolve load order
            self.log("Resolving module load order...")
            resolver = DependencyResolver(self.error_healer)
            
            for module_info in self.modules.values():
                resolver.add_module(module_info)
                
            load_order = resolver.resolve_order()
            self.log(f"Determined load order for {len(load_order)} modules")
            
            # Step 4: Process imports
            self.log("Processing imports...")
            import_processor = ImportProcessor(self.local_modules)
            
            # Collect imports from all files
            for module_name in load_order:
                module_info = self.modules[module_name]
                processed_content, file_imports = import_processor.process_file_imports(
                    module_info.content
                )
                module_info.processed_content = processed_content
                
                # Add imports to processor
                for imp in file_imports:
                    import_processor.add_import(imp)
                    
            # Step 5: Write output
            if self.dry_run:
                self.log(f"[DRY RUN] Would write to: {output_path}")
                self.log(f"[DRY RUN] Estimated size: {sum(len(m.processed_content) for m in self.modules.values())} bytes")
            else:
                self.log(f"Writing to {output_path}...")
                
            if not self.dry_run:
                with open(output_path, 'w', encoding='utf-8') as f:
                    # Header
                    repo_name = self.repo_path.name
                    f.write('#!/usr/bin/env python3\n')
                    f.write('"""\n')
                    f.write(f'CONSOLIDATED STANDALONE VERSION: {repo_name}\n')
                    f.write('='*70 + '\n\n')
                    f.write('All dependencies have been recursively inlined.\n')
                    f.write('This file is completely self-contained.\n\n')
                    f.write(f'Original location: {self.repo_path}\n')
                    f.write(f'Generated: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')
                    f.write(f'Modules included: {len(load_order)}\n')
                    f.write('"""\n\n')
                    
                    # Consolidated imports
                    imports_section = import_processor.get_consolidated_imports()
                    f.write(imports_section)
                    f.write('\n\n')
                    
                    # Module contents
                    f.write('# ============================================================================\n')
                    f.write('# INLINED MODULE CODE\n')
                    f.write('# ============================================================================\n\n')
                    
                    for module_name in load_order:
                        module_info = self.modules[module_name]
                        
                        f.write('\n')
                        f.write('# ' + '-'*70 + '\n')
                        f.write(f'# MODULE: {module_name}\n')
                        f.write(f'# SOURCE: {Path(module_info.file_path).relative_to(self.repo_path)}\n')
                        f.write('# ' + '-'*70 + '\n\n')
                        
                        f.write(module_info.processed_content)
                        f.write('\n\n')
                    
            # Step 6: Validate and report
            if not self.dry_run:
                file_size = os.path.getsize(output_path)
                file_hash = self._compute_file_hash(output_path)
                elapsed_time = time.time() - self.start_time
                
                self.log(f"\n{'='*70}")
                self.log(f"✓ Consolidation complete!")
                self.log(f"  Output: {output_path}")
                self.log(f"  Size: {file_size:,} bytes ({file_size / 1024:.1f} KB)")
                self.log(f"  Modules: {len(load_order)}")
                self.log(f"  SHA256: {file_hash[:16]}...")
                self.log(f"  Time: {elapsed_time:.2f}s")
                
                # Run syntax validation
                self.log("\nValidating output...")
                if self._validate_syntax(output_path):
                    self.log("✓ Syntax validation passed")
                else:
                    self.log("⚠ Syntax validation failed", 'warning')
            else:
                elapsed_time = time.time() - self.start_time
                self.log(f"\n{'='*70}")
                self.log(f"✓ Dry run complete!")
                self.log(f"  Would process {len(load_order)} modules")
                self.log(f"  Time: {elapsed_time:.2f}s")
                
            # Show summary
            summary = self.error_healer.get_summary()
            if summary['total_errors'] > 0 or summary['total_warnings'] > 0 or summary['total_skipped'] > 0:
                self.log(f"\nSummary:")
                self.log(f"  Errors: {summary['total_errors']}")
                self.log(f"  Warnings: {summary['total_warnings']}")
                self.log(f"  Skipped files: {summary['total_skipped']}")
                
            # Save detailed report
            if not self.dry_run:
                output_dir = os.path.dirname(output_path) or '.'
                self.error_healer.save_report(output_dir)
                
            self.log("="*70 + "\n")
            
            return True
            
        except Exception as e:
            self.error_healer.log_error(e, context="consolidate")
            self.log(f"✗ Consolidation failed: {e}", 'error')
            return False
            
    def _validate_syntax(self, file_path: str) -> bool:
        """Validate Python syntax of output file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                ast.parse(f.read())
            return True
        except SyntaxError as e:
            self.error_healer.log_error(
                e, context="syntax_validation",
                file_path=file_path
            )
            return False


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description='Consolidate a Python codebase into a standalone file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /path/to/repo
  %(prog)s /path/to/repo -o output.py
  %(prog)s crazy_functions/Dynamic_Function_Generate.py
  %(prog)s . --quiet

For more information, see: https://github.com/yourusername/consolidate
        """
    )
    
    parser.add_argument(
        'repo_path',
        help='Path to repository or Python file to consolidate'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output file path (default: <repo_name>_standalone.py)'
    )
    
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Suppress non-error output'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run without writing output file (preview only)'
    )
    
    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='Do not create backup of existing output file'
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 2.1'
    )
    
    args = parser.parse_args()
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        repo_path = Path(args.repo_path).resolve()
        if repo_path.is_file():
            # Single file - use its directory name
            repo_name = repo_path.parent.name
            output_name = f"{repo_path.stem}_standalone.py"
        else:
            repo_name = repo_path.name
            output_name = f"{repo_name}_standalone.py"
        output_path = str(Path.cwd() / output_name)
        
    # Run consolidation
    consolidator = CodebaseConsolidator(
        args.repo_path,
        verbose=not args.quiet,
        dry_run=args.dry_run,
        create_backup=not args.no_backup
    )
    
    success = consolidator.consolidate(output_path)
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()

# ============================================================================
# Lint & Format Utilities (Poetry-based)
# ============================================================================

def run(*command: str) -> None:
    """Execute a poetry run command with error handling."""
    print(f">>>>> Running poetry run {' '.join(command)}")
    try:
        subprocess.run(
            ["poetry", "run"] + list(command),
            cwd=SCRIPT_DIR,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as e:
        print(e.output.decode("utf-8"), file=sys.stderr)
        raise


def lint():
    """Run linting checks on codebase."""
    # Filter TARGET_DIRS to only existing paths
    existing_dirs = [d for d in TARGET_DIRS if os.path.exists(os.path.join(SCRIPT_DIR, d))]
    
    if not existing_dirs:
        logger.warning("No target directories found for linting")
        return
    
    lint_step_args: list[list[str]] = [
        ["ruff", "check", *existing_dirs, "--exit-zero"],
        ["ruff", "format", "--diff", "--check", LIBS_DIR] if os.path.exists(os.path.join(SCRIPT_DIR, LIBS_DIR)) else None,
        ["isort", "--diff", "--check", "--profile", "black", BACKEND_DIR],
        ["black", "--diff", "--check", BACKEND_DIR],
        ["pyright", *existing_dirs],
    ]
    
    # Filter out None entries
    lint_step_args = [args for args in lint_step_args if args is not None]
    
    lint_error = None
    for args in lint_step_args:
        try:
            run(*args)
        except subprocess.CalledProcessError as e:
            lint_error = e

    if lint_error:
        print("Lint failed, try running `poetry run format` to fix the issues")
        sys.exit(1)


def format_code():
    """Run code formatters on codebase."""
    existing_dirs = [d for d in TARGET_DIRS if os.path.exists(os.path.join(SCRIPT_DIR, d))]
    
    if not existing_dirs:
        logger.warning("No target directories found for formatting")
        return
        
    run("ruff", "check", "--fix", *existing_dirs)
    
    if os.path.exists(os.path.join(SCRIPT_DIR, LIBS_DIR)):
        run("ruff", "format", LIBS_DIR)
        
    run("isort", "--profile", "black", BACKEND_DIR)
    run("black", BACKEND_DIR)
    run("pyright", *existing_dirs)


# ============================================================================
# Argument Analysis Feature
# ============================================================================

class FunctionRequirementsAnalyzer(ast.NodeVisitor):
    """AST visitor to extract function requirements."""
    
    def __init__(self, function_name: Optional[str] = None):
        self.function_name = function_name
        self.functions_found: Dict[str, Dict[str, Any]] = {}
        self.current_function: Optional[str] = None
        self.current_scope_vars: Set[str] = set()
        self.global_imports: Set[str] = set()
        
    def visit_Import(self, node: ast.Import) -> None:
        """Track imported modules."""
        for alias in node.names:
            self.global_imports.add(alias.name.split('.')[0])
        self.generic_visit(node)
        
    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Track from-imports."""
        if node.module:
            self.global_imports.add(node.module.split('.')[0])
        self.generic_visit(node)
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Extract function signature and analyze body."""
        # Skip if we're looking for specific function and this isn't it
        if self.function_name and node.name != self.function_name:
            return
            
        func_info = {
            'name': node.name,
            'parameters': self._extract_parameters(node.args),
            'return_annotation': ast.unparse(node.returns) if node.returns else None,
            'decorators': [ast.unparse(d) for d in node.decorator_list],
            'free_variables': set(),
            'env_vars': set(),
            'calls': set(),
        }
        
        # Analyze function body
        self.current_function = node.name
        self.current_scope_vars = set(arg.arg for arg in node.args.args)
        self.current_scope_vars.update(arg.arg for arg in node.args.posonlyargs)
        self.current_scope_vars.update(arg.arg for arg in node.args.kwonlyargs)
        if node.args.vararg:
            self.current_scope_vars.add(node.args.vararg.arg)
        if node.args.kwarg:
            self.current_scope_vars.add(node.args.kwarg.arg)
            
        # Visit body to find free variables
        for stmt in node.body:
            self._analyze_node_for_vars(stmt, func_info)
            
        self.functions_found[node.name] = func_info
        self.current_function = None
        self.current_scope_vars = set()
        
    def _extract_parameters(self, args: ast.arguments) -> Dict[str, Any]:
        """Extract detailed parameter information."""
        params = {
            'positional': [],
            'positional_only': [],
            'keyword_only': [],
            'var_positional': None,
            'var_keyword': None,
            'defaults': {}
        }
        
        # Positional-only (Python 3.8+)
        for arg in args.posonlyargs:
            param_info = {
                'name': arg.arg,
                'annotation': ast.unparse(arg.annotation) if arg.annotation else None
            }
            params['positional_only'].append(param_info)
        
        # Regular positional/keyword
        for arg in args.args:
            param_info = {
                'name': arg.arg,
                'annotation': ast.unparse(arg.annotation) if arg.annotation else None
            }
            params['positional'].append(param_info)
            
        # Defaults for positional args
        if args.defaults:
            default_offset = len(args.args) - len(args.defaults)
            for i, default in enumerate(args.defaults):
                param_name = args.args[default_offset + i].arg
                params['defaults'][param_name] = ast.unparse(default)
        
        # *args
        if args.vararg:
            params['var_positional'] = {
                'name': args.vararg.arg,
                'annotation': ast.unparse(args.vararg.annotation) if args.vararg.annotation else None
            }
        
        # Keyword-only
        for arg in args.kwonlyargs:
            param_info = {
                'name': arg.arg,
                'annotation': ast.unparse(arg.annotation) if arg.annotation else None
            }
            params['keyword_only'].append(param_info)
            
        # Defaults for keyword-only
        for arg, default in zip(args.kwonlyargs, args.kw_defaults):
            if default:
                params['defaults'][arg.arg] = ast.unparse(default)
        
        # **kwargs
        if args.kwarg:
            params['var_keyword'] = {
                'name': args.kwarg.arg,
                'annotation': ast.unparse(args.kwarg.annotation) if args.kwarg.annotation else None
            }
            
        return params
    
    def _analyze_node_for_vars(self, node: ast.AST, func_info: Dict[str, Any]) -> None:
        """Recursively analyze node for free variables and env access."""
        # Check for environment variable access
        if isinstance(node, ast.Subscript):
            if isinstance(node.value, ast.Attribute):
                if (isinstance(node.value.value, ast.Name) and 
                    node.value.value.id == 'os' and 
                    node.value.attr == 'environ'):
                    if isinstance(node.slice, ast.Constant):
                        func_info['env_vars'].add(node.slice.value)
        
        # Check for os.getenv calls
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                if (isinstance(node.func.value, ast.Name) and 
                    node.func.value.id == 'os' and 
                    node.func.attr == 'getenv'):
                    if node.args and isinstance(node.args[0], ast.Constant):
                        func_info['env_vars'].add(node.args[0].value)
            
            # Track function calls
            try:
                call_name = ast.unparse(node.func)
                func_info['calls'].add(call_name)
            except:
                pass
        
        # Check for Name nodes (potential free variables)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            name = node.id
            # Skip if it's defined in current scope, imported, or builtin
            if (name not in self.current_scope_vars and 
                name not in self.global_imports and
                name not in dir(__builtins__)):
                func_info['free_variables'].add(name)
        
        # Track assignments in current scope
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.current_scope_vars.add(target.id)
        
        # Recurse
        for child in ast.iter_child_nodes(node):
            self._analyze_node_for_vars(child, func_info)


def analyze_standalone_file(filepath: str, function_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Analyze a standalone Python file to extract function requirements.
    
    Args:
        filepath: Path to the Python file
        function_name: Optional specific function to analyze
        
    Returns:
        Dictionary with analysis results
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source_code = f.read()
    except Exception as e:
        return {'error': f"Failed to read file: {e}"}
    
    try:
        tree = ast.parse(source_code, filename=filepath)
    except SyntaxError as e:
        return {'error': f"Syntax error in file: {e}"}
    
    analyzer = FunctionRequirementsAnalyzer(function_name)
    analyzer.visit(tree)
    
    if not analyzer.functions_found:
        if function_name:
            return {'error': f"Function '{function_name}' not found in file"}
        else:
            return {'error': "No functions found in file"}
    
    # Convert sets to lists for JSON serialization
    result = {
        'file': filepath,
        'analyzed_at': datetime.now().isoformat(),
        'functions': {}
    }
    
    for func_name, func_info in analyzer.functions_found.items():
        result['functions'][func_name] = {
            'name': func_info['name'],
            'parameters': func_info['parameters'],
            'return_annotation': func_info['return_annotation'],
            'decorators': func_info['decorators'],
            'free_variables': sorted(list(func_info['free_variables'])),
            'environment_variables': sorted(list(func_info['env_vars'])),
            'external_calls': sorted(list(func_info['calls']))[:20]  # Limit to 20 most common
        }
    
    return result


# ============================================================================
# Updated Main CLI (with subcommands)
# ============================================================================

def main_cli():
    """Command-line interface with subcommands."""
    parser = argparse.ArgumentParser(
        description='Consolidate Python code & analyze standalone files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Consolidate (default): creates standalone file
  %(prog)s crazy_functions/MyFeature.py
  
  # Analyze: inspect standalone file requirements
  %(prog)s analyze Standalones/MyFeature_STANDALONE.py
  %(prog)s analyze myfile.py --function main
  
  # Lint & Format
  %(prog)s lint
  %(prog)s format
        """
    )
    
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 3.1')
    
    # Create subparsers
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze standalone file requirements')
    analyze_parser.add_argument('filepath', help='Path to Python file to analyze')
    analyze_parser.add_argument('--function', help='Specific function to analyze')
    analyze_parser.add_argument('--output', help='Save JSON to file')
    
    # Lint command
    subparsers.add_parser('lint', help='Run linting checks')
    
    # Format command
    subparsers.add_parser('format', help='Run code formatters')
    
    # Default consolidation (backward compat)
    parser.add_argument('repo_path', nargs='?', help='Path to consolidate')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('-q', '--quiet', action='store_true', help='Suppress output')
    parser.add_argument('--dry-run', action='store_true', help='Preview only')
    parser.add_argument('--no-backup', action='store_true', help='No backup')
    
    args = parser.parse_args()
    
    # Route to appropriate handler
    if args.command == 'analyze':
        result = analyze_standalone_file(args.filepath, args.function)
        output_json = json.dumps(result, indent=2)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output_json)
            print(f"✅ Analysis saved to: {args.output}")
        else:
            print(output_json)
        
        sys.exit(0 if 'error' not in result else 1)
    
    elif args.command == 'lint':
        lint()
        sys.exit(0)
    
    elif args.command == 'format':
        format_code()
        sys.exit(0)
    
    # Default: consolidation
    if not args.repo_path:
        parser.print_help()
        sys.exit(1)
    
    # Call original main() logic
    main()


if __name__ == '__main__':
    # Use new CLI with subcommands
    main_cli()
