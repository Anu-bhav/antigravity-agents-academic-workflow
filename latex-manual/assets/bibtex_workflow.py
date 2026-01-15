#!/usr/bin/env python3
"""
BibTeX Workflow Script
Runs complete bibliography compilation workflow:
  1. pdflatex (creates .aux file)
  2. bibtex (processes bibliography)
  3. pdflatex (incorporates bibliography)
  4. pdflatex (resolves all references)
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

def run_command(cmd, verbose=False):
    """Run a shell command."""
    if verbose:
        print(f"Running: {' '.join(cmd)}")
    
    try:
        # On Windows, we need shell=True for some commands to be found if not fully qual, 
        # but usually for executables in PATH like pdflatex it's fine without if using list.
        # However, capture_output=True allows us to hide output unless verbose.
        result = subprocess.run(
            cmd, 
            check=False, 
            capture_output=not verbose, 
            text=True
        )
        
        if result.returncode != 0:
            print(f"Error running command: {' '.join(cmd)}")
            if not verbose: # If not verbose, print the captured stderr/stdout now
                print(result.stdout)
                print(result.stderr)
            return False
            
        return True
    except FileNotFoundError:
        print(f"Error: Command not found: {cmd[0]}")
        return False

def main():
    parser = argparse.ArgumentParser(description="BibTeX Compilation Workflow")
    parser.add_argument("texfile", help="The .tex file to compile")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed output")
    parser.add_argument("-c", "--clean", action="store_true", help="Clean auxiliary files after compilation")
    
    args = parser.parse_args()
    
    tex_path = Path(args.texfile).resolve()
    if not tex_path.exists():
        print(f"Error: File '{tex_path}' not found")
        sys.exit(1)
        
    basename = tex_path.stem
    directory = tex_path.parent
    
    # Change to directory of tex file to avoid path issues
    os.chdir(directory)
    
    # 1. First pdflatex
    print(f"\n[1/4] First LaTeX pass (creating .aux)...")
    if not run_command(["pdflatex", "-interaction=nonstopmode", tex_path.name], args.verbose):
        sys.exit(1)
        
    # Check for .aux
    if not Path(f"{basename}.aux").exists():
        print("Error: .aux file not created")
        sys.exit(1)

    # 2. BibTeX
    print(f"[2/4] Running BibTeX...")
    if not run_command(["bibtex", basename], args.verbose):
        print("BibTeX failed. Proceeding anyway (might be limited references)...")
        
    # 3. Second pdflatex
    print(f"[3/4] Second LaTeX pass (incorporating bibliography)...")
    if not run_command(["pdflatex", "-interaction=nonstopmode", tex_path.name], args.verbose):
        sys.exit(1)

    # 4. Third pdflatex
    print(f"[4/4] Final LaTeX pass (resolving references)...")
    if not run_command(["pdflatex", "-interaction=nonstopmode", tex_path.name], args.verbose):
        sys.exit(1)
        
    print(f"\nSuccess! Output: {basename}.pdf")
    
    if args.clean:
        print("Cleaning auxiliary files...")
        extensions = ['.aux', '.log', '.bbl', '.blg', '.out', '.toc']
        for ext in extensions:
            f = Path(f"{basename}{ext}")
            if f.exists():
                f.unlink()

if __name__ == "__main__":
    main()
