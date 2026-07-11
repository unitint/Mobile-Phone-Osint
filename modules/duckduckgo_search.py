from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def search_duckduckgo(query):
    """Search DuckDuckGo using Chrome browser"""
    results = {
        "found": False,
        "results": [],
        "count": 0,
        "error": None,
        "query": query
    }

    print(f"🦆 Searching DuckDuckGo for: {query}")
    
    # Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = None
    try:
        # Start Chrome
        print("⏳ Loading Chrome...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Go to DuckDuckGo
        print("⏳ Going to DuckDuckGo...")
        driver.get("https://duckduckgo.com")
        time.sleep(2)

        # Find search box and search
        print(f"⏳ Searching for: {query}")
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.submit()
        
        # Wait for results
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='result']"))
            )
        except:
            pass
        
        # Get results
        print("⏳ Getting results...")
        
        # DuckDuckGo result selectors
        search_results = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='result'] a, article a, div.result a")
        
        for link in search_results:
            href = link.get_attribute("href")
            title = link.text
            
            if href and href.startswith("http") and "duckduckgo.com" not in href:
                results["results"].append({
                    "title": title if title else "Link",
                    "link": href,
                    "snippet": ""
                })

        results["count"] = len(results["results"])
        results["found"] = results["count"] > 0
        print(f"✅ Found {results['count']} results on DuckDuckGo!")

    except Exception as e:
        results["error"] = str(e)
        print(f"❌ Error: {e}")

    finally:
        if driver:
            driver.quit()
            print("🔒 Done")

    return results