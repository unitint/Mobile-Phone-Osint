import time
from modules.duckduckgo_search import search_duckduckgo
from modules.phone_parser import normalize_phone, get_phone_info
from modules.link_classifier import process_result, get_summary


def investigate(phone):
    """Main investigation function - tracks each variation"""
    
    # Normalize the phone first
    normalized = normalize_phone(phone)
    if not normalized:
        return {"error": "Invalid phone number"}
    
    # Get the exact number (remove formatting)
    exact_number = phone.replace('+', '').replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
    
    # Get phone info
    phone_info = get_phone_info(normalized)
    
    # Define the variations we want to check
    variations_to_check = [
        f'"{exact_number}"',                    # "09946563099"
        exact_number,                            # 09946563099
        f'"{exact_number[:4]} {exact_number[4:7]} {exact_number[7:]}"',  # "0994 656 3099"
        f'"{exact_number[:4]}-{exact_number[4:7]}-{exact_number[7:]}"',  # "0994-656-3099"
        f'"+63{exact_number[1:]}"',              # "+639946563099"
        f'{exact_number[:4]} {exact_number[4:7]} {exact_number[7:]}',    # 0994 656 3099
        f'{exact_number[:4]}-{exact_number[4:7]}-{exact_number[7:]}',    # 0994-656-3099
        f'+63{exact_number[1:]}',                # +639946563099
        f'63{exact_number[1:]}',                 # 639946563099
    ]
    
    print(f"\n🎯 Searching for: {exact_number}")
    print(f"🔍 Using {len(variations_to_check)} variations\n")
    
    # ===== SEARCH EACH VARIATION =====
    variation_results = []
    all_links = []
    seen_links = set()
    
    for i, term in enumerate(variations_to_check, 1):
        print(f"[{i}/{len(variations_to_check)}] 🔍 Searching: {term}")
        
        result = search_duckduckgo(term)
        
        variation_data = {
            "term": term,
            "found": result.get('found', False),
            "count": result.get('count', 0),
            "links": []
        }
        
        if result.get('found'):
            for item in result.get('results', []):
                link = item.get('link', '')
                if link and link not in seen_links:
                    seen_links.add(link)
                    all_links.append(item)
                    variation_data["links"].append(item)
            
            variation_data["count"] = len(variation_data["links"])
        
        variation_results.append(variation_data)
        
        print(f"   ✅ Found {variation_data['count']} links")
        
        time.sleep(1.5)  # Delay between searches
    
    # ===== CLASSIFY ALL UNIQUE LINKS =====
    print("\n🔍 Classifying all unique results...")
    
    classified_results = []
    for link in all_links:
        processed = process_result(link)
        classified_results.append(processed)
    
    # Sort by score
    classified_results.sort(key=lambda x: x.get('score', 0), reverse=True)
    
    # Generate summary
    summary = get_summary(classified_results)
    
    # Calculate totals
    total_variations = len(variation_results)
    total_with_results = sum(1 for v in variation_results if v['count'] > 0)
    total_links = len(all_links)
    
    print(f"\n📊 SUMMARY:")
    print(f"   Total variations: {total_variations}")
    print(f"   Variations with results: {total_with_results}")
    print(f"   Total unique links: {total_links}")
    
    # Social media platforms
    social_media = [
        {
            "name": "Facebook",
            "icon": "📘",
            "url": f"https://www.facebook.com/search/top/?q={exact_number}",
            "found": any('facebook' in s.get('url', '').lower() for s in classified_results)
        },
        {
            "name": "Instagram",
            "icon": "📸",
            "url": f"https://www.instagram.com/explore/search/?q={exact_number}",
            "found": any('instagram' in s.get('url', '').lower() for s in classified_results)
        },
        {
            "name": "WhatsApp",
            "icon": "💬",
            "url": f"https://wa.me/{exact_number}",
            "found": False
        },
        {
            "name": "Telegram",
            "icon": "✈️",
            "url": "https://t.me/",
            "found": False
        }
    ]
    
    # Build report
    report = {
        "phone": normalized,
        "exact_number": exact_number,
        "phone_info": phone_info,
        "variations": variation_results,  # Each variation with its count
        "classified_results": classified_results[:30],
        "summary": summary,
        "social": social_media,
        "metadata": {
            "total_variations": total_variations,
            "variations_with_results": total_with_results,
            "total_unique_links": total_links
        }
    }
    
    return report