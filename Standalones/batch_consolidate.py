#!/usr/bin/env python3
"""
Batch consolidation script for creating standalone files from individual Python modules.
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

# File mappings: output_name -> source_path
FILES_TO_CONSOLIDATE = {
    "Internet_GPT_STANDALONE.py": "../crazy_functions/Internet_GPT.py",
    "github_search_STANDALONE.py": "../crazy_functions/paper_fns/github_search.py",
    "SourceCode_Analyse_STANDALONE.py": "../crazy_functions/SourceCode_Analyse.py",
    "Dynamic_Function_Generate_STANDALONE.py": "../crazy_functions/Dynamic_Function_Generate.py",
    "fastapi_stream_server_STANDALONE.py": "../shared_utils/fastapi_stream_server.py",
    "multi_language_STANDALONE.py": "../multi_language.py",
    "edge_gpt_free_STANDALONE.py": "../request_llms/edge_gpt_free.py",
}

def consolidate_single_file(source_path: str, output_name: str) -> bool:
    """
    Consolidate a single Python file by:
    1. Creating a temporary directory with just that file
    2. Running consolidate.py on that directory  
    3. Moving the output to the desired location
    """
    source = Path(source_path).resolve()
    if not source.exists():
        print(f"❌ Source file not found: {source}")
        return False
    
    # Create temp directory in PARENT directory to avoid Standalones exclusion
    script_dir = Path(__file__).parent
    parent_dir = script_dir.parent
    temp_dir = parent_dir / f"temp_{source.stem}_consolidate"
    temp_dir.mkdir(exist_ok=True)
    
    try:
        # Copy source file to temp directory
        temp_file = temp_dir / source.name
        shutil.copy2(source, temp_file)
        
        print(f"\n{'='*70}")
        print(f"📦 Consolidating: {source.name}")
        print(f"   Source: {source}")
        print(f"   Output: {output_name}")
        print(f"{'='*70}\n")
        
        # Run consolidation from parent directory
        output_path = script_dir / output_name
        cmd = [
            sys.executable,
            str(script_dir / "consolidate.py"),
            str(temp_dir),
            "--output", str(output_path)
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=parent_dir  # Run from parent to avoid Standalones exclusion
        )
        
        if result.returncode != 0:
            print(f"❌ Consolidation failed for {source.name}")
            print(f"STDERR: {result.stderr}")
            return False
        
        # Show last lines of output
        output_lines = result.stdout.strip().split('\n')
        for line in output_lines[-15:]:
            print(line)
        
        print(f"\n✅ Successfully created: {output_name}\n")
        return True
        
    finally:
        # Cleanup temp directory
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

def main():
    os.chdir(Path(__file__).parent)
    
    print("="*70)
    print("BATCH CONSOLIDATION - Creating Standalone Files")
    print("="*70)
    
    results = {}
    for output_name, source_path in FILES_TO_CONSOLIDATE.items():
        success = consolidate_single_file(source_path, output_name)
        results[output_name] = success
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    successful = [name for name, success in results.items() if success]
    failed = [name for name, success in results.items() if not success]
    
    print(f"\n✅ Successful: {len(successful)}/{len(results)}")
    for name in successful:
        print(f"   • {name}")
    
    if failed:
        print(f"\n❌ Failed: {len(failed)}/{len(results)}")
        for name in failed:
            print(f"   • {name}")
    
    return 0 if not failed else 1

if __name__ == "__main__":
    sys.exit(main())
