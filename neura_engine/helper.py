import os

def get_site_info(name, full=False):
    site_dict = {
        "google": {"url": "https://www.google.com", "search_box": "//textarea[@name='q']"},
        "youtube": {"url": "https://www.youtube.com", "search_box": "//input[@id='search']"},
        "amazon": {"url": "https://www.amazon.com", "search_box": "//input[@id='twotabsearchtextbox']"},
        "wikipedia": {"url": "https://www.wikipedia.org", "search_box": "//input[@id='searchInput']"},
        "facebook": {"url": "https://www.facebook.com"},
        "twitter": {"url": "https://www.twitter.com"},
        "instagram": {"url": "https://www.instagram.com"},
        "github": {"url": "https://www.github.com"},
        "linkedin": {"url": "https://www.linkedin.com"},
    }
    site = name.strip().lower()
    return site_dict.get(site) if full else site_dict.get(site, {}).get("url")

def write_content_file(topic, content):
    filename = f"{topic.replace(' ', '_')}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)
    return filename