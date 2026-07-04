import phonenumbers


def normalize_phone(phone):

    phone = phone.strip()

    try:
        # Philippines
        parsed = phonenumbers.parse(phone, "PH")

        if not phonenumbers.is_valid_number(parsed):
            return None

        return phonenumbers.format_number(
            parsed,
            phonenumbers.PhoneNumberFormat.E164
        )

    except:
        return None