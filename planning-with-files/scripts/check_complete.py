#!/usr/bin/env python3
"""
Check Complete Script
Parses a markdown task plan and checks if all items are marked as complete [x].
"""

import sys
import re
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Check if task plan is complete")
    parser.add_argument("file", nargs="?", default="task_plan.md", help="Markdown file to check")
    
    args = parser.parse_args()
    
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File '{file_path}' not found")
        sys.exit(1)
        
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
        
    # Find all checklist items
    # Matches: - [ ] or - [x] or - [/]
    items = re.findall(r'-\s*\[([ x/])\]', content)
    
    total = len(items)
    complete = items.count('x')
    in_progress = items.count('/')
    pending = items.count(' ')
    
    print(f"Status for {file_path.name}:")
    print(f"Total Items:  {total}")
    print(f"Completed:    {complete}")
    print(f"In Progress:  {in_progress}")
    print(f"Pending:      {pending}")
    
    if pending == 0 and in_progress == 0 and total > 0:
        print("\n✅ All tasks completed!")
        sys.exit(0)
    elif total == 0:
        print("\n⚠️ No tasks found.")
        sys.exit(1)
    else:
        print("\n❌ Tasks remaining.")
        sys.exit(1)

if __name__ == "__main__":
    main()
