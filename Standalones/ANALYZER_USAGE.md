# Standalone File Analyzer - Usage Guide

The `StandaloneAnalyzer` feature helps you understand what external dependencies, configuration, and arguments are required to run consolidated standalone Python files.

## Quick Start

### Method 1: Using the CLI Tool

```bash
# Analyze a single file
python analyze_standalone.py Internet_GPT_STANDALONE.py

# Analyze multiple files
python analyze_standalone.py *.py

# Analyze specific files
python analyze_standalone.py github_search_STANDALONE.py edge_gpt_free_STANDALONE.py
```

### Method 2: Using Python API

```python
from consolidate import StandaloneAnalyzer

# Create analyzer instance
analyzer = StandaloneAnalyzer('Internet_GPT_STANDALONE.py')

# Perform analysis
analysis = analyzer.analyze()

# Print formatted report
analyzer.print_report(analysis)

# Access raw data
print(f"External imports: {len(analysis['external_imports'])}")
print(f"Functions: {len(analysis['function_parameters'])}")
print(f"Config keys: {len(analysis['config_access'])}")
```

## What Does It Analyze?

### 1. External Dependencies 📦
Identifies imports that weren't successfully inlined during consolidation:

```
📦 EXTERNAL DEPENDENCIES
  crazy_functions.crazy_utils:
    - from crazy_functions.crazy_utils import input_clipping (line 30)
    - from crazy_functions.crazy_utils import request_gpt_model... (line 30)
  
  request_llms.bridge_all:
    - from request_llms.bridge_all import model_info (line 38)
```

### 2. Configuration Requirements ⚙️
Finds calls to configuration functions and extracts required keys:

```
⚙️ CONFIGURATION REQUIREMENTS
  Required configuration keys:
    - JINA_API_KEY
    - SEARXNG_URLS
    - proxies
```

### 3. Function Analysis 🎯
Extracts function signatures and identifies potential entry points:

```
🎯 FUNCTION ANALYSIS
  Total functions: 7
  
  Potential entry points:
    - search_optimizer(query, proxies, history, llm_kwargs, ...)
    - main()
```

### 4. Global Variables 🌐
Lists global variable assignments:

```
🌐 GLOBAL VARIABLES
  Found 41 global variables:
    - mutable = ['', time.time(), '']
    - query_json = re.sub('```json|```', '', query_json)
    - links = []
    ... and 38 more
```

### 5. Recommendations 💡
Provides actionable next steps:

```
💡 RECOMMENDATIONS
  ⚠️  This file has external dependencies and is NOT fully standalone
     Consider re-running consolidation with these modules included
  
  ⚠️  This file requires runtime configuration
     Ensure config values are provided when running
```

## Analysis Data Structure

The `analyze()` method returns a dictionary with:

```python
{
    "file": str,                      # File path
    "external_imports": [             # List of import dicts
        {
            "type": "from_import",    # or "import"
            "module": str,            # Module name
            "name": str,              # Imported name
            "alias": str or None,     # Import alias
            "line": int               # Line number
        }
    ],
    "function_parameters": {          # Function signatures
        "function_name": {
            "args": [str],            # Argument names
            "defaults": int,          # Number of defaults
            "kwonlyargs": [str],      # Keyword-only args
            "vararg": str or None,    # *args name
            "kwarg": str or None,     # **kwargs name
            "line": int               # Line number
        }
    },
    "global_variables": {             # Global vars
        "var_name": {
            "value": str,             # String representation
            "line": int               # Line number
        }
    },
    "config_access": [                # Config function calls
        {
            "function": str,          # Function name
            "key": str or None,       # Config key
            "line": int               # Line number
        }
    ],
    "summary": {                      # High-level summary
        "total_external_imports": int,
        "unique_modules": int,
        "total_functions": int,
        "potential_entry_points": [str],
        "config_dependencies": int,
        "global_variables": int
    }
}
```

## Export to JSON

```python
import json
from consolidate import StandaloneAnalyzer

analyzer = StandaloneAnalyzer('myfile.py')
analysis = analyzer.analyze()

# Save to JSON
with open('analysis.json', 'w') as f:
    json.dump(analysis, f, indent=2)
```

## Batch Analysis

```python
from pathlib import Path
from consolidate import StandaloneAnalyzer

# Analyze all standalone files
standalone_files = Path('.').glob('*_STANDALONE.py')

for filepath in standalone_files:
    analyzer = StandaloneAnalyzer(str(filepath))
    analysis = analyzer.analyze()
    
    if "error" not in analysis:
        print(f"\n{filepath.name}:")
        print(f"  Modules: {analysis['summary']['unique_modules']}")
        print(f"  Functions: {analysis['summary']['total_functions']}")
```

## Use Cases

1. **Before Running Standalone Files**: Identify what needs to be installed
2. **Debugging Consolidation**: See what dependencies weren't inlined
3. **Documentation**: Generate dependency lists automatically
4. **CI/CD Integration**: Validate standalone files in pipelines
5. **Code Review**: Understand file requirements quickly

## Error Handling

The analyzer gracefully handles errors:

```python
analyzer = StandaloneAnalyzer('nonexistent.py')
result = analyzer.analyze()

if "error" in result:
    print(f"Error: {result['error']}")
    # Error: File not found: nonexistent.py
```

## Tips

- Run analyzer after consolidation to verify results
- Use the summary section for quick overviews
- Check line numbers to locate dependencies in source
- Export to JSON for integration with other tools
- Rerun consolidation with missing modules if needed

## Example Workflow

```bash
# 1. Consolidate a module
python consolidate.py ../crazy_functions/Internet_GPT.py -o Internet_GPT_STANDALONE.py

# 2. Analyze the result
python analyze_standalone.py Internet_GPT_STANDALONE.py

# 3. Review the dependencies
# 4. If needed, re-consolidate with additional modules
# 5. Repeat until fully standalone
```

## Integration with Other Tools

The analyzer output can be easily integrated with:

- **CI/CD pipelines** (GitHub Actions, GitLab CI)
- **Documentation generators** (Sphinx, MkDocs)
- **Dependency scanners** (pip-audit, safety)
- **Static analysis tools** (pylint, mypy)

---

For more information, see:
- `consolidate.py` - Main consolidation tool
- `batch_consolidate.py` - Batch processing script
- `analyze_standalone.py` - CLI analyzer tool

