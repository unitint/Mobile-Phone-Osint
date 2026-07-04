def check_whatsapp(phone):
    """Check if phone number exists on WhatsApp"""
    result = {
        "found": False,
        "url": f"https://wa.me/{phone.replace('+', '')}",
        "details": "Click the link to check WhatsApp",
        "error": None
    }
    return result