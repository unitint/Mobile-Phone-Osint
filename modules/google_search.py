from urllib.parse import quote


def google_dorks(phone):

    queries = [

        f'"{phone}"',

        f'site:facebook.com "{phone}"',

        f'site:instagram.com "{phone}"',

        f'site:x.com "{phone}"',

        f'site:linkedin.com "{phone}"',

        f'site:tiktok.com "{phone}"',

        f'site:youtube.com "{phone}"',

        f'site:reddit.com "{phone}"',

        f'site:github.com "{phone}"',

        f'"{phone}" scam',

        f'"{phone}" fraud',

        f'"{phone}" whatsapp',

        f'"{phone}" telegram'

    ]

    results = []

    for query in queries:

        results.append({

            "title": query,

            "url": "https://www.google.com/search?q=" + quote(query)

        })

    return results