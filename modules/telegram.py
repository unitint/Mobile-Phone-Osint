def check_telegram(phone):
    """Check if phone number exists on Telegram"""
    result = {
        "found": False,
        "url": "https://t.me/",
        "details": "Manual check required - Telegram requires API token",
        "error": None
    }
    return result