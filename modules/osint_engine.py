from modules.google_search import google_dorks


def investigate(phone):

    report = {

        "phone": phone,

        "google": google_dorks(phone),

        "social": [

            {
                "name": "Facebook",
                "url": "https://www.facebook.com/login/identify/"
            },

            {
                "name": "Instagram",
                "url": "https://www.instagram.com/accounts/password/reset/"
            },

            {
                "name": "WhatsApp",
                "url": f"https://wa.me/{phone.replace('+','')}"
            },

            {
                "name": "Telegram",
                "url": "https://t.me/"
            }

        ]

    }

    return report