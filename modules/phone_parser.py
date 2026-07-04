import re
import phonenumbers
from phonenumbers import carrier, geocoder, timezone

def normalize_phone(phone):
    """Validate and normalize phone number - ACCEPTS ALL FORMATS"""
    try:
        # Clean the phone number
        phone = re.sub(r'[\s\-\(\)\.]', '', phone)
        
        # If it starts with 0, assume it's a local number
        # Try to parse with Philippines default (+63)
        if phone.startswith('0'):
            try:
                parsed = phonenumbers.parse(phone, 'PH')
                if phonenumbers.is_valid_number(parsed):
                    formatted = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
                    return formatted
            except:
                pass
        
        # Try parsing without country code
        try:
            parsed = phonenumbers.parse(phone, None)
            if phonenumbers.is_valid_number(parsed):
                formatted = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
                return formatted
        except:
            pass
        
        # If it starts with +, parse as international
        if phone.startswith('+'):
            try:
                parsed = phonenumbers.parse(phone, None)
                if phonenumbers.is_valid_number(parsed):
                    formatted = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
                    return formatted
            except:
                pass
        
        # Last resort: try Philippines
        try:
            parsed = phonenumbers.parse(phone, 'PH')
            if phonenumbers.is_valid_number(parsed):
                formatted = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
                return formatted
        except:
            pass
        
        return None
        
    except:
        return None

def get_phone_info(phone):
    """Get carrier, location, timezone for a phone number"""
    try:
        clean = re.sub(r'[\s\-\(\)\.]', '', phone)
        
        try:
            parsed = phonenumbers.parse(clean, 'PH')
        except:
            try:
                parsed = phonenumbers.parse(clean, None)
            except:
                return None
        
        if not phonenumbers.is_valid_number(parsed):
            return None
        
        info = {
            "country": geocoder.country_name_for_number(parsed, "en"),
            "location": geocoder.description_for_number(parsed, "en"),
            "carrier": carrier.name_for_number(parsed, "en"),
            "timezone": str(timezone.time_zones_for_number(parsed)),
            "valid": phonenumbers.is_valid_number(parsed),
            "possible": phonenumbers.is_possible_number(parsed)
        }
        return info
    except:
        return None

def get_phone_variations(phone):
    """Generate ONLY the formats you want for searching"""
    try:
        clean = re.sub(r'[\s\-\(\)\.]', '', phone)
        
        variations = {}
        
        # Parse as PH number
        try:
            parsed = phonenumbers.parse(clean, 'PH')
            if phonenumbers.is_valid_number(parsed):
                # International format with +
                variations["international"] = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
                # International without +
                variations["international_no_plus"] = variations["international"].replace('+', '')
                # National format (local with 0)
                variations["national"] = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
        except:
            pass
        
        # If parsing failed, try without country code
        if "international" not in variations:
            try:
                parsed = phonenumbers.parse(clean, None)
                if phonenumbers.is_valid_number(parsed):
                    variations["international"] = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
                    variations["international_no_plus"] = variations["international"].replace('+', '')
                    variations["national"] = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
            except:
                pass
        
        # Add the original input
        variations["original"] = phone
        
        # Get digits only
        digits = re.sub(r'[^0-9]', '', clean)
        
        # Philippine number formatting
        if len(digits) >= 10:
            # Remove country code if present
            if digits.startswith('63'):
                local_part = digits[2:]
            elif digits.startswith('0'):
                local_part = digits[1:]
            else:
                local_part = digits
            
            # Only add if we have a valid local part (10 digits for PH)
            if len(local_part) >= 10:
                # Local with 0 (Philippine format)
                local_with_zero = '0' + local_part
                variations["local_with_zero"] = local_with_zero
                
                # Local with dashes
                variations["local_with_dash"] = local_with_zero[:4] + '-' + local_with_zero[4:7] + '-' + local_with_zero[7:]
                
                # Local with spaces
                variations["local_with_space"] = local_with_zero[:4] + ' ' + local_with_zero[4:7] + ' ' + local_with_zero[7:]
        
        return variations
        
    except Exception as e:
        return {"error": str(e), "original": phone}

def get_all_search_terms(phone):
    """Get ONLY the search terms you want"""
    variations = get_phone_variations(phone)
    
    search_terms = set()
    
    # Add the formats you want
    for key, value in variations.items():
        if value and key != "error" and key != "original":
            # Skip unwanted formats
            if key in ["international_no_plus", "national"]:
                continue
            
            # Add the variation
            search_terms.add(str(value))
            # Also add quoted version for exact match
            search_terms.add(f'"{str(value)}"')
    
    # Get digits for additional formatting
    digits = re.sub(r'[^0-9]', '', phone)
    
    # Remove country code if present
    if digits.startswith('63'):
        local_part = digits[2:]
    elif digits.startswith('0'):
        local_part = digits[1:]
    else:
        local_part = digits
    
    # Add the specific formats you want
    if len(local_part) >= 10:
        # Format 1: 09088600114 (no formatting)
        local_with_zero = '0' + local_part
        search_terms.add(local_with_zero)
        search_terms.add(f'"{local_with_zero}"')
        
        # Format 2: 0908-860-0114 (with dashes)
        formatted_dash = local_with_zero[:4] + '-' + local_with_zero[4:7] + '-' + local_with_zero[7:]
        search_terms.add(formatted_dash)
        search_terms.add(f'"{formatted_dash}"')
        
        # Format 3: 0908 860 0114 (with spaces)
        formatted_space = local_with_zero[:4] + ' ' + local_with_zero[4:7] + ' ' + local_with_zero[7:]
        search_terms.add(formatted_space)
        search_terms.add(f'"{formatted_space}"')
    
    # Add international format with +
    if digits.startswith('63'):
        international = '+' + digits
        search_terms.add(international)
        search_terms.add(f'"{international}"')
    
    # Remove empty strings and None
    search_terms = {term for term in search_terms if term}
    
    # Convert to list and sort
    result = list(search_terms)
    
    # Filter to only show the formats you want
    filtered = []
    for term in result:
        # Only keep these formats
        if any([
            term.startswith('+63'),
            term.startswith('0'),
            '-' in term and len(term) >= 12,
            ' ' in term and len(term) >= 12
        ]):
            filtered.append(term)
    
    # If filtered is empty, return the original set
    if not filtered:
        filtered = result
    
    return filtered[:20]  # Limit to 20 variations