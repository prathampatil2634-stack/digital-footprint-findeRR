import requests

HEADERS = {"User-Agent": "Mozilla/5.0"}


def check_email(email):
    """Email breaches chi list deto."""
    url = "https://api.xposedornot.com/v1/check-email/" + email
    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException:
        return [], "Internet kinva API error"

    if response.status_code == 200:
        data = response.json()
        if "breaches" in data:
            return data["breaches"][0], None
        return [], None
    elif response.status_code == 404:
        return [], None
    return [], "API error, code " + str(response.status_code)


def check_username(username):
    """Kontya sites var username ahe te deto."""
    sites = {
        "GitHub": "https://github.com/" + username,
        "Dev.to": "https://dev.to/" + username,
        "Medium": "https://medium.com/@" + username,
        "Reddit": "https://www.reddit.com/user/" + username,
    }
    results = {}
    for site_name in sites:
        try:
            r = requests.get(sites[site_name], timeout=8, headers=HEADERS)
            if r.status_code == 200:
                results[site_name] = "Found"
            elif r.status_code == 404:
                results[site_name] = "Not found"
            else:
                results[site_name] = "Unknown"
        except requests.RequestException:
            results[site_name] = "Unknown"
    return results


def calculate_score(breach_count, found_count):
    score = breach_count * 11 + found_count * 3
    if score > 100:
        score = 100
    if score >= 61:
        level = "High"
    elif score >= 31:
        level = "Medium"
    else:
        level = "Low"
    return score, level