import requests

print("Digital Footprint Finder")

email = input("Tumcha email taka: ")
username = input("Tumcha username taka: ")

# ---------- 1. Breach check ----------
print("\n[1] Breach check suru ahe...")

url = "https://api.xposedornot.com/v1/check-email/" + email
response = requests.get(url, timeout=10)

breach_count = 0

if response.status_code == 200:
    data = response.json()
    if "breaches" in data:
        breaches = data["breaches"][0]
        breach_count = len(breaches)
        print("Tumcha email", breach_count, "breaches madhe sapadla:")
        for name in breaches:
            print(" -", name)
    else:
        print("Chhan! Konatya breach madhe sapadla nahi.")
elif response.status_code == 404:
    print("Chhan! Konatya breach madhe sapadla nahi.")
else:
    print("Kahitari problem aala. Code:", response.status_code)

# ---------- 2. Username check ----------
print("\n[2] Username check suru ahe...")

sites = {
    "GitHub": "https://github.com/" + username,
    "Dev.to": "https://dev.to/" + username,
    "Medium": "https://medium.com/@" + username,
    "Reddit": "https://www.reddit.com/user/" + username,
}

found_count = 0

for site_name in sites:
    try:
        r = requests.get(sites[site_name], timeout=8,
                         headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200:
            print(" ", site_name, ": Found")
            found_count = found_count + 1
        elif r.status_code == 404:
            print(" ", site_name, ": Not found")
        else:
            print(" ", site_name, ": Unknown (site ne block kela)")
    except requests.RequestException:
        print(" ", site_name, ": Error")

# ---------- 3. Risk score ----------
print("\n[3] Risk score")

score = breach_count * 11 + found_count * 3

if score > 100:
    score = 100

if score >= 61:
    level = "High"
elif score >= 31:
    level = "Medium"
else:
    level = "Low"

print("Score:", score, "/ 100")
print("Risk level:", level)
