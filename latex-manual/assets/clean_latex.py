#!/usr/bin/env python3
"""
Clean LaTeX Auxiliary Files
Removes .aux, .log, .bbl, .blg, .out, .toc, .synctex.gz, .fls, .fdb_latexmk files.
"""

import sys
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Clean LaTeX auxiliary files")
    parser.add_argument("target", nargs="?", help="Specific .tex file basename (optional)")
    parser.add_argument("-d", "--deep", action="store_true", help="Deep clean (include PDFs)")
    
    args = parser.parse_args()
    
    extensions = ['.aux', '.log', '.bbl', '.blg', '.out', '.toc', '.synctex.gz', '.fls', '.fdb_latexmk', '.nav', '.snm']
    if args.deep:
        extensions.append('.pdf')
        
    cwd = Path.cwd()
    count = 0
    
    if args.target:
        # Clean for specific file
        name = Path(args.target).stem
        for ext in extensions:
            f = cwd / f"{name}{ext}"
            if f.exists():
                try:
                    f.unlink()
                    print(f"Removed: {f.name}")
                    count += 1
                except Exception as e:
                    print(f"Error removing {f.name}: {e}")
    else:
        # Clean global
        print(f"Cleaning all LaTeX auxiliary files in {cwd}...")
        for ext in extensions:
            for f in cwd.glob(f"*{ext}"):
                try:
                    f.unlink()
                    print(f"Removed: {f.name}")
                    count += 1
                except Exception as e:
                    print(f"Error removing {f.name}: {e}")
                    
    print(f"\nDone. Removed {count} files.")

if __name__ == "__main__":
    main()
