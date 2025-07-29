def extract_features(url):
    return {
        'url_length': len(url),
        'has_at': '@' in url,
        'has_dash': '-' in url,
        'has_https': 'https' in url,
        'digit_count': sum(char.isdigit() for char in url)
    }

# Example URLs
urls = [
    "http://paypal-login.com",
    "https://secure-google.com@fake.ru",
    "http://192.168.0.1/login",
    "https://bankofamerica.com",
    "http://verify-update-security.com"
]

for u in urls:
    print(extract_features(u))
