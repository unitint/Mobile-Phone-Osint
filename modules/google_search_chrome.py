from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def google_search_with_chrome(query):
    """Search Google using Chrome browser"""
    results = {
        "found": False,
        "results": [],
        "count": 0,
        "error": None,
        "query": query
    }

    print(f"🌐 Searching: {query}")
    
    # Chrome options - VISIBLE mode (so you can see it working)
    chrome_options = Options()
    # DO NOT use headless - let's see the browser!
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = None
    try:
        # Auto-install Chrome driver
        print("⏳ Loading Chrome...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Go to Google
        print("⏳ Going to Google...")
        driver.get("https://www.google.com")
        time.sleep(2)

        # Type the search
        print(f"⏳ Searching for: {query}")
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.submit()
        time.sleep(3)

        # Get results
        print("⏳ Getting results...")
        search_results = driver.find_elements(By.CSS_SELECTOR, "div.g a")
        
        for link in search_results:
            href = link.get_attribute("href")
            title = link.text
            
            if href and href.startswith("http") and "google.com" not in href:
                results["results"].append({
                    "title": title if title else "Link",
                    "link": href,
                    "snippet": ""
                })

        results["count"] = len(results["results"])
        results["found"] = results["count"] > 0
        print(f"✅ Found {results['count']} results!")

    except Exception as e:
        results["error"] = str(e)
        print(f"❌ Error: {e}")

    finally:
        if driver:
            driver.quit()
            print("🔒 Done")

    return results