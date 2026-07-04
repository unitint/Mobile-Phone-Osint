import requests
from bs4 import BeautifulSoup
import time
import urllib.parse
import random

def google_dorks(query):
    """Search Google for a specific query - WORKING VERSION"""
    results = {
        "found": False,
        "results": [],
        "count": 0,
        "error": None,
        "query": query
    }
    
    try:
        # Encode query for URL
        encoded_query = urllib.parse.quote(query)
        
        # Use multiple Google domains
        search_urls = [
            f"https://www.google.com/search?q={encoded_query}&num=100&hl=en",
            f"https://www.google.com.ph/search?q={encoded_query}&num=100&hl=en",
        ]
        
        # Rotate User-Agents to avoid blocking
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"
        ]
        
        headers = {
            "User-Agent": random.choice(user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0"
        }
        
        all_links = []
        seen_links = set()
        
        # Try multiple search URLs
        for search_url in search_urls:
            try:
                print(f"🔍 Searching: {search_url}")
                response = requests.get(search_url, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Find all search result links - multiple selectors
                    selectors = [
                        'div.g',
                        'div.tF2Cxc',
                        'div.yuRUbf',
                        'div#search div.g',
                        'div[data-hveid]'
                    ]
                    
                    for selector in selectors:
                        for result in soup.select(selector):
                            # Try different link selectors
                            link_tag = result.select_one('a')
                            if not link_tag:
                                link_tag = result.select_one('h3 a')
                            if not link_tag:
                                link_tag = result.select_one('.yuRUbf a')
                            
                            # Try different title selectors
                            title_tag = result.select_one('h3')
                            if not title_tag:
                                title_tag = result.select_one('.LC20lb')
                            if not title_tag:
                                title_tag = result.select_one('.DKV0Md')
                            
                            # Try different snippet selectors
                            snippet_tag = result.select_one('.VwiC3b')
                            if not snippet_tag:
                                snippet_tag = result.select_one('.lEBKkf')
                            if not snippet_tag:
                                snippet_tag = result.select_one('.IsZvec')
                            
                            if link_tag and title_tag:
                                link = link_tag.get('href', '')
                                title = title_tag.get_text().strip()
                                snippet = snippet_tag.get_text().strip() if snippet_tag else ""
                                
                                # Clean the link
                                if link.startswith('/url?q='):
                                    link = link.split('/url?q=')[1].split('&')[0]
                                elif not link.startswith('http'):
                                    continue
                                
                                # Only add real websites (not Google)
                                if link.startswith('http') and 'google.com' not in link and 'youtube.com' not in link:
                                    if link not in seen_links and title:
                                        seen_links.add(link)
                                        all_links.append({
                                            "title": title,
                                            "link": link,
                                            "snippet": snippet
                                        })
                    
                    # If we found results, break
                    if all_links:
                        break
                    
            except Exception as e:
                print(f"Search attempt failed: {e}")
                continue
            
            time.sleep(random.uniform(1, 3))
        
        # If still no results, try a simpler approach with different headers
        if not all_links:
            print("Trying alternative search method...")
            try:
                simple_headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
                }
                
                url = f"https://www.google.com/search?q={encoded_query}&num=50"
                response = requests.get(url, headers=simple_headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    for link in soup.find_all('a'):
                        href = link.get('href', '')
                        text = link.get_text().strip()
                        
                        if href.startswith('/url?q=') and text:
                            real_url = href.split('/url?q=')[1].split('&')[0]
                            if 'google.com' not in real_url and real_url.startswith('http') and text:
                                if real_url not in seen_links:
                                    seen_links.add(real_url)
                                    all_links.append({
                                        "title": text[:100],
                                        "link": real_url,
                                        "snippet": ""
                                    })
            except Exception as e:
                print(f"Alternative search failed: {e}")
        
        # Remove duplicates and limit results
        unique_results = []
        seen = set()
        for result in all_links:
            if result['link'] not in seen:
                seen.add(result['link'])
                unique_results.append(result)
        
        results["results"] = unique_results
        results["count"] = len(unique_results)
        results["found"] = results["count"] > 0
        
        print(f"✅ Found {results['count']} results for '{query}'")
        
    except Exception as e:
        results["error"] = str(e)
        print(f"❌ Google search error for '{query}': {e}")
    
    return results