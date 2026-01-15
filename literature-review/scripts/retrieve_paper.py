#!/usr/bin/env python3
"""
Paper Retrieval Tool
Finds full-text PDFs using Unpaywall (Legal OA), Google Scholar, and Anna's Archive.
"""

import sys
import argparse
import requests
import urllib.parse
import json
import re
from typing import Optional, Dict

def get_unpaywall_url(doi: str, email: str = "unpaywall_user@example.com") -> Optional[str]:
    """Check Unpaywall for Open Access PDF."""
    try:
        url = f"https://api.unpaywall.org/v2/{doi}?email={email}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('is_oa') and data.get('best_oa_location'):
                return data['best_oa_location'].get('url_for_pdf')
    except Exception as e:
        print(f"Warning: Unpaywall check failed: {e}", file=sys.stderr)
    return None

def get_google_scholar_url(title: str) -> Optional[str]:
    """Search Google Scholar for PDF link."""
    try:
        from scholarly import scholarly
        search_query = scholarly.search_pubs(title)
        pub = next(search_query, None)
        if pub:
            # Check for direct PDF link
            if 'eprint_url' in pub and pub['eprint_url']:
                return pub['eprint_url']
            # Check pub_url if it looks like a PDF
            if 'pub_url' in pub and pub['pub_url'].lower().endswith('.pdf'):
                return pub['pub_url']
    except ImportError:
        print("Warning: scholarly module not installed. Skipping Google Scholar.", file=sys.stderr)
    except Exception as e:
        print(f"Warning: Google Scholar check failed: {e}", file=sys.stderr)
    return None

def main():
    parser = argparse.ArgumentParser(description="Retrieve paper PDF links")
    parser.add_argument("query", help="DOI or Paper Title")
    parser.add_argument("--doi", action="store_true", help="Treat query as DOI")
    parser.add_argument("--title", action="store_true", help="Treat query as Title")
    
    args = parser.parse_args()
    
    query = args.query.strip()
    is_doi = args.doi or query.startswith("10.")
    
    print(f"Searching for: {query}")
    print("-" * 40)

    # 1. Unpaywall (if DOI)
    if is_doi:
        print("Checking Unpaywall (Open Access)... ", end="", flush=True)
        oa_url = get_unpaywall_url(query)
        if oa_url:
            print("FOUND!")
            print(f"Legal PDF: {oa_url}")
            return
        else:
            print("Not found.")
            
    # 2. Google Scholar
    print("Checking Google Scholar... ", end="", flush=True)
    gs_query = query
    if is_doi:
        gs_query = f"doi:{query}" # Use DOI in GS search if available
        
    pdf_url = get_google_scholar_url(gs_query)
    if pdf_url:
        print("FOUND!")
        print(f"Direct Link: {pdf_url}")
        # We continue to Anna's Archive as fallback/alternative even if GS found something
    else:
        print("Not found.")

    # 3. Anna's Archive
    print("Generating Anna's Archive Link... ", end="", flush=True)
    encoded_query = urllib.parse.quote(query)
    annas_url = f"https://annas-archive.li/search?q={encoded_query}"
    print("DONE")
    print("-" * 40)
    print(f"Anna's Archive Search: {annas_url}")
    print("(Click to find cached/shadow library versions)")

if __name__ == "__main__":
    main()
