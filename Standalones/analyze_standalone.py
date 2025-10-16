#!/usr/bin/env python3
"""
Analyze standalone files to identify their requirements and dependencies.
"""
import sys
from pathlib import Path
from consolidate import StandaloneAnalyzer


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_standalone.py <file1.py> [file2.py ...]")
        print("   or: python analyze_standalone.py *.py")
        sys.exit(1)
    
    files = sys.argv[1:]
    
    for filepath in files:
        path = Path(filepath)
        if not path.exists():
            print(f"❌ File not found: {filepath}")
            continue
        
        if not path.suffix == '.py':
            print(f"⚠️  Skipping non-Python file: {filepath}")
            continue
        
        analyzer = StandaloneAnalyzer(str(path))
        analysis = analyzer.analyze()
        
        if "error" in analysis:
            print(f"\n❌ ERROR analyzing {filepath}: {analysis['error']}\n")
            continue
        
        analyzer.print_report(analysis)


if __name__ == "__main__":
    main()

