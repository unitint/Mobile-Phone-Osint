import time
from modules.duckduckgo_search import search_duckduckgo
from modules.phone_parser import normalize_phone, get_phone_info
from modules.link_classifier import process_result, get_summary


def investigate(phone, raw_input=None):
    """Main investigation function - tracks each variation"""
    
    # Normalize the phone first
    normalized = normalize_phone(phone)
    if not normalized:
        return {"error": "Invalid phone number"}
    
    # Get phone info
    phone_info = get_phone_info(normalized)
    
    # ===== USE THE RAW INPUT (what user typed) =====
    # If raw_input is provided, use it. Otherwise use phone.
    if raw_input:
        original_input = raw_input.strip()
    else:
        original_input = phone.strip()
    
    # Clean the number to get digits only for formatting
    clean_number = original_input.replace('+', '').replace('-', '').replace(' ', '').replace('(', '').replace(')', '').strip()
    
    # ===== ONLY 4 FORMATS =====
    # Format 1: Plain number (09623293747) - KEEP THE ORIGINAL WITH 0
    plain = original_input
    
    # Format 2: International with +63 (+639623293747)
    # Remove leading 0 and add +63
    if clean_number.startswith('0'):
        international = f'+63{clean_number[1:]}'
    else:
        international = f'+63{clean_number}'
    
    # Format 3: With spaces (0962 329 3747) - KEEP THE ORIGINAL WITH 0
    if len(clean_number) >= 11 and clean_number.startswith('0'):
        spaces = f'{clean_number[:4]} {clean_number[4:7]} {clean_number[7:]}'
    else:
        spaces = original_input
    
    # Format 4: With dashes (0962-329-3747) - KEEP THE ORIGINAL WITH 0
    if len(clean_number) >= 11 and clean_number.startswith('0'):
        dashes = f'{clean_number[:4]}-{clean_number[4:7]}-{clean_number[7:]}'
    else:
        dashes = original_input
    
    # Build the variations list (ONLY 4) - WITH THE 0 INTACT
    variations_to_check = [
        plain,          # 09623293747
        international,  # +639623293747
        spaces,         # 0962 329 3747
        dashes,         # 0962-329-3747
    ]
    
    print(f"\n🎯 Searching for: {plain}")
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
            "url": f"https://www.facebook.com/search/top/?q={plain}",
            "found": any('facebook' in s.get('url', '').lower() for s in classified_results)
        },
        {
            "name": "Instagram",
            "icon": "📸",
            "url": f"https://www.instagram.com/explore/search/?q={plain}",
            "found": any('instagram' in s.get('url', '').lower() for s in classified_results)
        },
        {
            "name": "WhatsApp",
            "icon": "💬",
            "url": f"https://wa.me/{plain}",
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
        "exact_number": plain,
        "phone_info": phone_info,
        "variations": variation_results,
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