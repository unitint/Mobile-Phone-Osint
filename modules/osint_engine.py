import time
from modules.duckduckgo_search import search_duckduckgo
from modules.phone_parser import get_all_search_terms, get_phone_info, normalize_phone


def investigate(phone):
    """Main investigation function using DuckDuckGo"""
    
    # Normalize the phone first
    normalized = normalize_phone(phone)
    if not normalized:
        return {"error": "Invalid phone number"}
    
    # Get ALL search variations
    search_terms = get_all_search_terms(normalized)
    
    # Get the exact number
    exact_number = phone.replace('+', '').replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
    
    # Get phone info
    phone_info = get_phone_info(normalized)
    
    # Search DuckDuckGo for ALL variations
    all_search_links = []
    seen_links = set()
    
    print("🦆 Starting DuckDuckGo searches...")
    
    # First search with exact number quoted (for exact match)
    print(f"\n🔍 PRIMARY SEARCH: \"{exact_number}\"")
    result = search_duckduckgo(f'"{exact_number}"')
    
    if result.get('found'):
        for item in result.get('results', []):
            link = item.get('link', '')
            if link and link not in seen_links:
                seen_links.add(link)
                all_search_links.append(item)
    
    time.sleep(2)
    
    # Search with each variation
    for term in search_terms[:5]:  # Limit to avoid issues
        if term not in [f'"{exact_number}"', exact_number]:
            print(f"\n🔍 Searching: {term}")
            result = search_duckduckgo(term)
            
            if result.get('found'):
                for item in result.get('results', []):
                    link = item.get('link', '')
                    if link and link not in seen_links:
                        seen_links.add(link)
                        all_search_links.append(item)
            
            time.sleep(2)
    
    # Social media platforms
    social_media = [
        {
            "name": "Facebook",
            "icon": "📘",
            "url": f"https://www.facebook.com/search/top/?q={exact_number}",
            "search_url": f"https://www.facebook.com/search/top/?q={exact_number}",
            "found": False
        },
        {
            "name": "Instagram",
            "icon": "📸",
            "url": "https://www.instagram.com/accounts/password/reset/",
            "search_url": f"https://www.google.com/search?q=site:instagram.com+{exact_number}",
            "found": False
        },
        {
            "name": "WhatsApp",
            "icon": "💬",
            "url": f"https://wa.me/{exact_number}",
            "search_url": f"https://wa.me/{exact_number}",
            "found": False
        },
        {
            "name": "Telegram",
            "icon": "✈️",
            "url": "https://t.me/",
            "search_url": f"https://www.google.com/search?q=site:t.me+{exact_number}",
            "found": False
        }
    ]
    
    # Build report
    report = {
        "phone": normalized,
        "original_input": phone,
        "exact_number": exact_number,
        "phone_info": phone_info,
        "search_variations": search_terms[:20],
        "search_results": {  # RENAMED from 'google' to 'search_results'
            "total_results": len(all_search_links),
            "unique_links": all_search_links[:50]
        },
        "social": social_media,
        "summary": {
            "total_search_terms": len(search_terms),
            "search_matches": len(all_search_links)  # RENAMED
        }
    }
    
    print(f"\n✅ Total results found: {len(all_search_links)}")
    return report