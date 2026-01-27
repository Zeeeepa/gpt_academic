#!/usr/bin/env python3
"""
Batch consolidation script - FIXED VERSION
============================================

Creates standalone versions of multiple Python files with FULL PROJECT CONTEXT.

KEY FIX: Points consolidate.py to the FULL project directory with --entry-point,
not an isolated temp directory!

This ensures:
- Full dependency inlining
- No external project imports remain
- No duplicated code
- Correct ordering
- Actually standalone files!
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

# File mappings: output_name -> source_path (relative to project root)
FILES_TO_CONSOLIDATE = {
    "Internet_GPT_STANDALONE.py": "crazy_functions/Internet_GPT.py",
    "github_search_STANDALONE.py": "crazy_functions/paper_fns/github_search.py",
    "SourceCode_Analyse_STANDALONE.py": "crazy_functions/SourceCode_Analyse.py",
    "Dynamic_Function_Generate_STANDALONE.py": "crazy_functions/Dynamic_Function_Generate.py",
    "fastapi_stream_server_STANDALONE.py": "shared_utils/fastapi_stream_server.py",
    "multi_language_STANDALONE.py": "multi_language.py",
    "edge_gpt_free_STANDALONE.py": "request_llms/edge_gpt_free.py",
}

def consolidate_single_file(source_path: str, output_name: str, project_root: Path) -> bool:
    """
    Consolidate a single Python file with FULL PROJECT CONTEXT.
    
    NEW APPROACH (FIXED):
    1. Point consolidate.py at the PROJECT ROOT (not temp dir!)
    2. Specify the TARGET FILE as --entry-point
    3. consolidate.py will:
       - Scan full project for ALL modules
       - Find dependencies from entry point (tree shaking)
       - Inline ALL project dependencies
       - Generate clean standalone file
    4. Output goes to Standalones/
    
    Result: Properly inlined, no duplicates, correct ordering!
    """
    source = project_root / source_path
    if not source.exists():
        print(f"❌ Source file not found: {source}")
        return False
    
    script_dir = Path(__file__).parent
    output_path = script_dir / output_name
    
    print(f"\n{'='*70}")
    print(f"📦 Consolidating: {source_path}")
    print(f"   Project root: {project_root}")
    print(f"   Entry point: {source}")
    print(f"   Output: {output_name}")
    print(f"{'='*70}\n")
    
    # Run consolidation with FULL project context + entry point
    cmd = [
        sys.executable,
        str(script_dir / "consolidate.py"),
        str(project_root),           # Full project directory
        "--entry-point", source_path, # Which file to consolidate
        "--output", str(output_path)  # Where to write result
    ]
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=project_root
    )
    
    if result.returncode != 0:
        print(f"❌ Consolidation failed for {source_path}")
        print(f"\n--- STDERR ---")
        print(result.stderr)
        print(f"\n--- STDOUT (last 2000 chars) ---")
        print(result.stdout[-2000:] if len(result.stdout) > 2000 else result.stdout)
        return False
    
    # Show last lines of output
    output_lines = result.stdout.strip().split('\n')
    for line in output_lines[-20:]:
        print(line)
    
    # Verify output file was created
    if not output_path.exists():
        print(f"❌ Output file not created: {output_path}")
        return False
    
    file_size = output_path.stat().st_size
    print(f"\n✅ Successfully created: {output_name} ({file_size:,} bytes / {file_size/1024:.1f} KB)\n")
    return True

def main():
    script_dir = Path(__file__).parent
    project_root = script_dir.parent  # Go up from Standalones/ to project root
    
    if not project_root.exists():
        print(f"❌ Project root not found: {project_root}")
        return 1
    
    print("="*70)
    print("BATCH CONSOLIDATION (FIXED) - Creating Standalone Files")
    print(f"Project Root: {project_root}")
    print(f"Output Dir: {script_dir}")
    print("="*70)
    print(f"\nFiles to process: {len(FILES_TO_CONSOLIDATE)}")
    for output_name, source_path in FILES_TO_CONSOLIDATE.items():
        print(f"  • {source_path} → {output_name}")
    print()
    
    results = {}
    for output_name, source_path in FILES_TO_CONSOLIDATE.items():
        success = consolidate_single_file(source_path, output_name, project_root)
        results[output_name] = success
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    successful = [name for name, success in results.items() if success]
    failed = [name for name, success in results.items() if not success]
    
    print(f"\n✅ Successful: {len(successful)}/{len(results)}")
    for name in successful:
        size = (script_dir / name).stat().st_size if (script_dir / name).exists() else 0
        print(f"   • {name:<45} ({size:>8,} bytes)")
    
    if failed:
        print(f"\n❌ Failed: {len(failed)}/{len(results)}")
        for name in failed:
            print(f"   • {name}")
        print("\n💡 Tip: Check the error messages above for details")
    else:
        print("\n🎉 All files consolidated successfully!")
    
    print("="*70)
    
    return 0 if not failed else 1

if __name__ == "__main__":
    sys.exit(main())

