import json
from datetime import datetime

def generate_report(report_data):
    """Generate a detailed report from investigation results"""
    
    report = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "phone_number": report_data.get("phone", ""),
        "summary": {
            "total_search_terms": report_data.get("summary", {}).get("total_search_terms", 0),
            "google_matches": report_data.get("summary", {}).get("google_matches", 0),
            "platforms_checked": report_data.get("summary", {}).get("platforms_checked", 0)
        },
        "search_variations": report_data.get("search_variations", []),
        "google_results": report_data.get("google", {}),
        "social_results": report_data.get("social", [])
    }
    
    return report

def save_report(report, filename=None):
    """Save report to JSON file"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{timestamp}.json"
    
    with open(filename, "w") as f:
        json.dump(report, f, indent=2)
    
    return filename