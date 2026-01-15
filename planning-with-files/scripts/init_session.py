#!/usr/bin/env python3
"""
Init Session Script
Initializes planning files (task_plan.md, findings.md, progress.md) if they don't exist.
"""

import sys
import argparse
from pathlib import Path

TASK_PLAN_TEMPLATE = """# Task Plan

## Objective
[Describe the main objective of this session]

## Phases
- [ ] **Phase 1: Analysis**
    - [ ] [Subtask 1]
- [ ] **Phase 2: Execution**
    - [ ] [Subtask 1]
- [ ] **Phase 3: Verification**
    - [ ] [Subtask 1]
"""

FINDINGS_TEMPLATE = """# Findings & Notes

## Key Discoveries
- [Discovery 1]

## Issues / Roadblocks
- [Issue 1]

## References
- [Reference 1]
"""

PROGRESS_TEMPLATE = """# Session Progress Log

| Time | Activity | Status |
|------|----------|--------|
| Start | Session Initialized | Ready |
"""

def create_file(path: Path, template: str):
    if not path.exists():
        path.write_text(template, encoding='utf-8')
        print(f"Created: {path.name}")
    else:
        print(f"Skipped: {path.name} (already exists)")

def main():
    parser = argparse.ArgumentParser(description="Initialize session files")
    parser.add_argument("dir", nargs="?", default=".", help="Directory to initialize")
    
    args = parser.parse_args()
    
    directory = Path(args.dir)
    if not directory.exists():
        directory.mkdir(parents=True)
        
    create_file(directory / "task_plan.md", TASK_PLAN_TEMPLATE)
    create_file(directory / "findings.md", FINDINGS_TEMPLATE)
    create_file(directory / "progress.md", PROGRESS_TEMPLATE)
    
    print("\nSession initialized.")

if __name__ == "__main__":
    main()
