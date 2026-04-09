# Namecheap (cPanel) Deployment Guide 🚀

Follow these steps to host your **Universal Poultry Farm** website on Namecheap Shared Hosting using the "Setup Python App" tool.

## 1. Prepare Your Files
1.  **Database**: Ensure your `db.sqlite3` file is in the project root if you want to keep your local data.
2.  **Environment Variables**: You will need to set your `.env` variables (Secret Key, Gmail Password) in the cPanel interface later.
3.  **Requirements**: Ensure `requirements.txt` is up to date (run `pip freeze > requirements.txt` locally).
4.  **Static Files**: Run `python manage.py collectstatic` locally to ensure the `staticfiles` folder is ready, or run it in the cPanel terminal.

## 2. Upload to Namecheap
1.  Log in to your **Namecheap cPanel**.
2.  Open **File Manager**.
3.  Create a new folder in your home directory (e.g., `/home/username/chicks`).
4.  **Upload** all your project files EXCEPT for `venv` into this folder.
    - *Tip: Zip your files locally, upload the zip, and extract it in cPanel for speed.*

## 3. Setup Python App
1.  In cPanel, search for **"Setup Python App"**.
2.  Click **"CREATE APPLICATION"**.
3.  **Python Version**: Select `3.10` or higher.
4.  **Application root**: Enter the folder path (e.g., `chicks`).
5.  **Application URL**: Select your domain (`universalpoultryfarm.com`).
6.  **Application startup file**: Enter `passenger_wsgi.py`.
7.  Click **"CREATE"**.

## 4. Configure Passenger WSGI
Namecheap uses the Phusion Passenger server. Create a file named `passenger_wsgi.py` in your project root (inside `universalpoultryfarm.com`) and paste this **exact** code:

```python
import os
import sys

# This tells Passenger where your project is
sys.path.insert(0, os.getcwd())

# Set the Django settings module 
# (Make sure this matches your project folder name)
os.environ['DJANGO_SETTINGS_MODULE'] = 'poultry_farm.settings'

# Import the application from your wsgi.py
from poultry_farm.wsgi import application
```

## 5. Install Dependencies
1.  In the "Setup Python App" interface, scroll down to **"Configuration files"**.
2.  Type `requirements.txt` and click **"Add"**.
3.  Click **"Run Pip Install"** and choose `requirements.txt`.
4.  Wait for it to finish.

## 6. Set Environment Variables
In the same "Setup Python App" screen, look for **"Environment variables"**:
- Add `SECRET_KEY`
- Add `EMAIL_HOST_USER`
- Add `EMAIL_HOST_PASSWORD`
- Add `DEBUG` (set to `False`)

## 7. Final Steps (Terminal)
1.  Open the **Terminal** in cPanel.
2.  Activate the virtualenv using the command provided at the top of the "Setup Python App" page (e.g., `source /home/username/nodevenv/chicks/3.10/bin/activate`).
3.  Run migrations:
    ```bash
    python manage.py migrate
    ```
4.  (If needed) Collect static files:
    ```bash
    python manage.py collectstatic
    ```

## 8. Static Files in cPanel
In your Django `settings.py`, ensure:
- `STATIC_URL = '/static/'`
- `STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')`

In cPanel **File Manager**:
1.  Go to `public_html`.
2.  Create a **Symbolic Link** or copy the contents of your `staticfiles` folder into `public_html/static`.
    - *Or better: In cPanel "Static Files" setting, map `/static/` to your project's `staticfiles` folder.*

## 9. Reload
Go back to "Setup Python App" and click **"RESTART"**. Your site should now be live at your domain! 🎊
