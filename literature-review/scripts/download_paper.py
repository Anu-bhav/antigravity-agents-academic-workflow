import argparse
import requests
import re
from pathlib import Path
from pypdf import PdfReader
from io import BytesIO

def clean_filename(text):
    """Remove invalid characters for filenames."""
    return re.sub(r'[<>:"/\\|?*]', '', text).strip()

def format_author(author_str):
    """Format author string: 'Smith, Jones' -> 'Smith et al.'"""
    # Check for multiple authors indicators
    if "," in author_str or " and " in author_str:
        # Split separators and take the first one
        parts = re.split(r',| and ', author_str)
        if len(parts) > 1:
            return f"{parts[0].strip()} et al."
    return author_str

def download_and_parse(url, author, year, title):
    formatted_author = format_author(author)
    filename = f"{clean_filename(formatted_author)} - {year} - {clean_filename(title)}.pdf"
    
    print(f"Downloading from {url}...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Save PDF
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Saved to: {filename}")
        
        # Parse Text
        print("Extracting text...")
        reader = PdfReader(filename)
        text = ""
        # extracting first 5 pages to avoid overwhelming output, usually enough for Intro/Abstract
        for i, page in enumerate(reader.pages[:5]): 
            text += page.extract_text() + "\n"
            
        print("-" * 40)
        print(f"--- TEXT CONTENT ({min(5, len(reader.pages))} pages) ---")
        print(text[:2000] + "..." if len(text) > 2000 else text) # Preview
        print("-" * 40)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download and parse academic papers.")
    parser.add_argument("url", help="Direct URL to the PDF")
    parser.add_argument("--author", required=True, help="Primary Author's Last Name")
    parser.add_argument("--year", required=True, help="Publication Year")
    parser.add_argument("--title", required=True, help="Paper Title")
    
    args = parser.parse_args()
    download_and_parse(args.url, args.author, args.year, args.title)
