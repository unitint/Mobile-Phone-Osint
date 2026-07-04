import time
from modules.google_search import google_dorks
from modules.phone_parser import get_all_search_terms, get_phone_info, normalize_phone


def investigate(phone):
    """Main investigation function with ALL variations"""
    
    # Normalize the phone first
    normalized = normalize_phone(phone)
    if not normalized:
        return {"error": "Invalid phone number"}
    
    # Get ALL search variations
    search_terms = get_all_search_terms(normalized)
    
    # Get phone info (carrier, location, etc.)
    phone_info = get_phone_info(normalized)
    
    # Search Google for ALL variations
    all_google_links = []
    seen_links = set()
    
    # Search with multiple variations
    for term in search_terms[:10]:
        print(f"Searching: {term}")
        result = google_dorks(term)
        
        if result.get('found'):
            for item in result.get('results', []):
                link = item.get('link', '')
                if link and link not in seen_links:
                    seen_links.add(link)
                    all_google_links.append(item)
        
        # Small delay between searches
        time.sleep(1)
    
    # Also search with just the digits (in case other formats fail)
    digits_only = ''.join(filter(str.isdigit, phone))
    if digits_only:
        result = google_dorks(digits_only)
        if result.get('found'):
            for item in result.get('results', []):
                link = item.get('link', '')
                if link and link not in seen_links:
                    seen_links.add(link)
                    all_google_links.append(item)
    
    # Social media platforms with search URLs
    social_media = [
        {
            "name": "Facebook",
            "icon": "📘",
            "url": f"https://www.facebook.com/search/top/?q={normalized.replace('+', '')}",
            "search_url": f"https://www.facebook.com/search/top/?q={normalized}",
            "found": False
        },
        {
            "name": "Instagram",
            "icon": "📸",
            "url": "https://www.instagram.com/accounts/password/reset/",
            "search_url": f"https://www.google.com/search?q=site:instagram.com+{normalized}",
            "found": False
        },
        {
            "name": "WhatsApp",
            "icon": "💬",
            "url": f"https://wa.me/{normalized.replace('+', '')}",
            "search_url": f"https://wa.me/{normalized.replace('+', '')}",
            "found": False
        },
        {
            "name": "Telegram",
            "icon": "✈️",
            "url": "https://t.me/",
            "search_url": f"https://www.google.com/search?q=site:t.me+{normalized}",
            "found": False
        },
        {
            "name": "Twitter/X",
            "icon": "🐦",
            "url": f"https://twitter.com/search?q={normalized}",
            "search_url": f"https://twitter.com/search?q={normalized}",
            "found": False
        },
        {
            "name": "LinkedIn",
            "icon": "💼",
            "url": f"https://www.linkedin.com/search/results/all/?keywords={normalized}",
            "search_url": f"https://www.linkedin.com/search/results/all/?keywords={normalized}",
            "found": False
        },
        {
            "name": "Google Docs",
            "icon": "📄",
            "url": f"https://www.google.com/search?q=site:docs.google.com+{normalized}",
            "search_url": f"https://www.google.com/search?q=site:docs.google.com+{normalized}",
            "found": False
        },
        {
            "name": "PDF Documents",
            "icon": "📑",
            "url": f"https://www.google.com/search?q=filetype:pdf+{normalized}",
            "search_url": f"https://www.google.com/search?q=filetype:pdf+{normalized}",
            "found": False
        },
        {
            "name": "Public Records",
            "icon": "📋",
            "url": f"https://www.google.com/search?q={normalized}+site:.gov+OR+site:.edu",
            "search_url": f"https://www.google.com/search?q={normalized}+site:.gov+OR+site:.edu",
            "found": False
        },
        {
            "name": "Viber",
            "icon": "💜",
            "url": f"https://www.viber.com/en/people-search/?number={normalized}",
            "search_url": f"https://www.viber.com/en/people-search/?number={normalized}",
            "found": False
        }
    ]
    
    # Build report
    report = {
        "phone": normalized,
        "original_input": phone,
        "phone_info": phone_info,
        "search_variations": search_terms[:20],
        "google": {
            "total_results": len(all_google_links),
            "unique_links": all_google_links[:50]
        },
        "social": social_media,
        "summary": {
            "total_search_terms": len(search_terms),
            "google_matches": len(all_google_links)
        }
    }
    
    return report