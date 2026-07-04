def check_instagram(phone):
    """Check if phone number exists on Instagram"""
    result = {
        "found": False,
        "url": "https://www.instagram.com/accounts/password/reset/",
        "details": "Manual check required - Instagram requires authentication",
        "error": None
    }
    return result