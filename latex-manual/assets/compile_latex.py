#!/usr/bin/env python3
"""
Compile LaTeX Document
Wrapper for pdflatex/xelatex/lualatex with optional BibTeX workflow.
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
        result = subprocess.run(
            cmd, 
            check=False, 
            capture_output=not verbose, 
            text=True
        )
        if result.returncode != 0:
            print(f"Error running command: {' '.join(cmd)}")
            if not verbose:
                print(result.stdout)
                print(result.stderr)
            return False
        return True
    except FileNotFoundError:
        print(f"Error: Command not found: {cmd[0]}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Compile LaTeX document")
    parser.add_argument("texfile", help="The .tex file to compile")
    parser.add_argument("-b", "--bibtex", action="store_true", help="Run full BibTeX workflow")
    parser.add_argument("-c", "--clean", action="store_true", help="Clean auxiliary files after")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed output")
    parser.add_argument("--compiler", default="pdflatex", choices=["pdflatex", "xelatex", "lualatex"], help="Compiler to use")
    
    args = parser.parse_args()
    
    tex_path = Path(args.texfile).resolve()
    if not tex_path.exists():
        print(f"Error: File '{tex_path}' not found")
        sys.exit(1)
        
    basename = tex_path.stem
    directory = tex_path.parent
    os.chdir(directory)
    
    compiler = args.compiler
    
    # Simple compilation
    if not args.bibtex:
        print(f"Compiling with {compiler}...")
        if not run_command([compiler, "-interaction=nonstopmode", tex_path.name], args.verbose):
            sys.exit(1)
            
    # Full workflow
    else:
        print(f"\n[1/4] First pass ({compiler})...")
        if not run_command([compiler, "-interaction=nonstopmode", tex_path.name], args.verbose):
            sys.exit(1)
            
        print(f"[2/4] BibTeX...")
        run_command(["bibtex", basename], args.verbose) # Ignore error if no bib
        
        print(f"[3/4] Second pass ({compiler})...")
        if not run_command([compiler, "-interaction=nonstopmode", tex_path.name], args.verbose):
            sys.exit(1)

        print(f"[4/4] Final pass ({compiler})...")
        if not run_command([compiler, "-interaction=nonstopmode", tex_path.name], args.verbose):
            sys.exit(1)
            
    print(f"\nSuccess! Output: {basename}.pdf")
    
    if args.clean:
        # Call the clean script module if available, or just do it inline
        print("Cleaning auxiliary files...")
        extensions = ['.aux', '.log', '.bbl', '.blg', '.out', '.toc', '.nav', '.snm']
        for ext in extensions:
            f = Path(f"{basename}{ext}")
            if f.exists():
                f.unlink()

if __name__ == "__main__":
    main()
