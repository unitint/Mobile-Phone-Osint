import re

def classify_link(url, title=""):
    """Classify a link into a category and assign a score"""
    
    url_lower = url.lower()
    title_lower = title.lower()
    
    # ===== HIGH PRIORITY (90-100) =====
    
    # Government (.gov, .mil, .edu)
    if '.gov' in url_lower or '.gov.ph' in url_lower:
        return {
            "category": "Government Document",
            "score": 100,
            "icon": "🏛️",
            "badge": "Official"
        }
    
    # Business Registration / SEC
    if any(x in url_lower for x in ['sec.gov', 'business', 'corporation', 'company', 'inc.', 'llc', 'corp']):
        return {
            "category": "Business Registration",
            "score": 90,
            "icon": "🏢",
            "badge": "Business"
        }
    
    # LinkedIn
    if 'linkedin.com' in url_lower:
        return {
            "category": "Professional Profile",
            "score": 90,
            "icon": "💼",
            "badge": "Professional"
        }
    
    # ===== HIGH PRIORITY (80-89) =====
    
    # Facebook
    if 'facebook.com' in url_lower:
        if 'profile' in url_lower or 'page' in url_lower or 'photo' in url_lower:
            return {
                "category": "Facebook Profile",
                "score": 85,
                "icon": "📘",
                "badge": "Social"
            }
        return {
            "category": "Facebook Page",
            "score": 80,
            "icon": "📘",
            "badge": "Social"
        }
    
    # Instagram
    if 'instagram.com' in url_lower:
        return {
            "category": "Instagram Profile",
            "score": 80,
            "icon": "📸",
            "badge": "Social"
        }
    
    # Twitter/X
    if 'twitter.com' in url_lower or 'x.com' in url_lower:
        return {
            "category": "Twitter/X Profile",
            "score": 80,
            "icon": "🐦",
            "badge": "Social"
        }
    
    # YouTube
    if 'youtube.com' in url_lower:
        return {
            "category": "YouTube Channel",
            "score": 75,
            "icon": "▶️",
            "badge": "Social"
        }
    
    # ===== MEDIUM PRIORITY (60-79) =====
    
    # Whitepages / People Search
    if any(x in url_lower for x in ['whitepages', 'anywho', 'truecaller', 'spokeo', 'zabasearch', 'pipl']):
        return {
            "category": "People Directory",
            "score": 75,
            "icon": "📋",
            "badge": "Directory"
        }
    
    # Company Website
    if any(x in url_lower for x in ['about', 'contact', 'team', 'careers']) and '.com' in url_lower:
        return {
            "category": "Company Website",
            "score": 70,
            "icon": "🌐",
            "badge": "Business"
        }
    
    # News Article
    if any(x in url_lower for x in ['news', 'article', 'blog', 'post']):
        return {
            "category": "News Article",
            "score": 65,
            "icon": "📰",
            "badge": "Media"
        }
    
    # ===== LOW PRIORITY (40-59) =====
    
    # Forum / Discussion
    if any(x in url_lower for x in ['forum', 'thread', 'discussion', 'reddit']):
        return {
            "category": "Forum Discussion",
            "score": 40,
            "icon": "💬",
            "badge": "Forum"
        }
    
    # PDF Document
    if '.pdf' in url_lower:
        return {
            "category": "PDF Document",
            "score": 50,
            "icon": "📄",
            "badge": "Document"
        }
    
    # ===== DEFAULT =====
    return {
        "category": "Web Page",
        "score": 30,
        "icon": "🌍",
        "badge": "General"
    }

def process_result(result):
    """Process a single result with classification"""
    
    url = result.get('link', '')
    title = result.get('title', '')
    snippet = result.get('snippet', '')
    
    classification = classify_link(url, title)
    
    return {
        "url": url,
        "title": title,
        "snippet": snippet,
        "category": classification['category'],
        "score": classification['score'],
        "icon": classification['icon'],
        "badge": classification['badge'],
        "name": None,
        "emails": []
    }

def get_summary(results):
    """Generate summary statistics from classified results"""
    
    summary = {
        "total": len(results),
        "categories": {},
        "scores": {
            "high": 0,
            "medium": 0,
            "low": 0
        },
        "names": [],
        "emails": []
    }
    
    for result in results:
        category = result.get('category', 'Unknown')
        score = result.get('score', 0)
        
        summary['categories'][category] = summary['categories'].get(category, 0) + 1
        
        if score >= 80:
            summary['scores']['high'] += 1
        elif score >= 50:
            summary['scores']['medium'] += 1
        else:
            summary['scores']['low'] += 1
        
        if result.get('name'):
            summary['names'].append(result['name'])
        
        for email in result.get('emails', []):
            if email and email not in summary['emails']:
                summary['emails'].append(email)
    
    summary['names'] = list(set(summary['names']))
    summary['emails'] = list(set(summary['emails']))
    
    return summary