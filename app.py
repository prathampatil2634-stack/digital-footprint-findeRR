from datetime import datetime
from flask import Flask, render_template, request
from checker import check_email, check_username, calculate_score

app = Flask(__name__)


def get_suggestions(breach_count, found_count, level):
    tips = []
    if breach_count > 0:
        tips.append(("High", "Breach zalelya sagalya sites var password lagech badla, ani te password kuthe reuse kele asel tithe pan."))
    tips.append(("High", "Email, banking ani social accounts var Two-Factor Authentication (2FA) chalu kara."))
    tips.append(("Medium", "Password manager vapara, mhanje pratyek account la vegla strong password milel."))
    if found_count > 0:
        tips.append(("Medium", "Je " + str(found_count) + " public profiles sapadle, tyatle junne ani na vaparlele accounts delete kara."))
        tips.append(("Low", "Social profiles private kara ani phone number / email hide kara."))
    if level == "Low":
        tips.append(("Low", "Tumcha footprint kami ahe. Pratyek 3 mahinyani parat scan kara."))
    return tips


@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        email = request.form["email"].strip()
        username = request.form["username"].strip()

        breaches, error = check_email(email)
        profiles = check_username(username)
        found_count = list(profiles.values()).count("Found")
        unknown_count = list(profiles.values()).count("Unknown")
        score, level = calculate_score(len(breaches), found_count)

        result = {
            "email": email,
            "username": username,
            "breaches": breaches,
            "profiles": profiles,
            "found_count": found_count,
            "unknown_count": unknown_count,
            "checked_sites": len(profiles),
            "score": score,
            "level": level,
            "error": error,
            "breach_risk": min(100, len(breaches) * 25),
            "visibility_risk": min(100, found_count * 25),
            "tips": get_suggestions(len(breaches), found_count, level),
            "time": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        }

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=False)