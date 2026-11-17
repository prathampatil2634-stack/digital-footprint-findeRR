# Digital Footprint Finder – Deployment

## Stack
- Python / Flask
- HTML template in `templates/index.html`
- `requests` for external checks
- Gunicorn production server

## Run locally
1. Create and activate a virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Start: `python app.py`
4. Open `http://127.0.0.1:5000`.

## Deploy on Render
1. Push this folder's contents to a GitHub repository (the `app.py`, `checker.py`, `requirements.txt`, `Procfile`, and `templates/` folder must be at the repository root).
2. In Render, create a **New Web Service** and connect that GitHub repository.
3. Choose Python as the runtime.
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn app:app`
6. Create the service and wait for the deploy to finish.
7. Open the `onrender.com` URL Render provides.

## Important notes
- Use only your own email address and username when testing.
- The app sends the email to the XposedOrNot public API and requests public profile pages for username checks.
- The current project does not include a database.
- Username checks based on HTTP status codes can be inaccurate; a `200` response does not always prove a profile exists.
- Do not collect or store visitors' personal information without their informed consent.
