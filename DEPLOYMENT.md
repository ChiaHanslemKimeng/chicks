# Universal Poultry Farm Deployment Guide 🚀

Follow these steps to deploy your poultry farm website to GitHub and PythonAnywhere.

## 1. Local Preparation
Before pushing your code, ensure your environment is clean:
1. Ensure your `.gitignore` is present (I've created this for you).
2. Check `requirements.txt` is updated: `pip freeze > requirements.txt`.
3. Set `DEBUG = False` and configure `ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']` in `settings.py` (do this *after* testing locally).

## 2. Push to GitHub
1. Create a new repository on [GitHub](https://github.com/new).
2. Open your terminal in the project folder and run:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - PoultryElite Production"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

## 3. Deploy to PythonAnywhere
1. Create a [PythonAnywhere](https://www.pythonanywhere.com/) account.
2. Open a **Bash Console** and clone your repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
   ```
3. Create a Virtual Environment and install dependencies:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 venv
   pip install -r requirements.txt
   ```
4. **Web Tab Configuration**:
   - Go to the **Web** tab on PythonAnywhere.
   - Click **Add a new web app** (choose Manual Configuration -> Python 3.10).
   - **Virtualenv**: Enter the path to your venv (e.g., `/home/yourusername/.virtualenvs/venv`).
   - **Static Files**: Add mappings:
     - URL: `/static/` -> Path: `/home/yourusername/YOUR_REPO_NAME/staticfiles/`
     - URL: `/media/` -> Path: `/home/yourusername/YOUR_REPO_NAME/media/`
   - **WSGI Configuration File**: Edit it and set it up for Django:
     ```python
     import os
     import sys
     path = '/home/yourusername/YOUR_REPO_NAME'
     if path not in sys.path:
         sys.path.append(path)
     os.environ['DJANGO_SETTINGS_MODULE'] = 'poultry_farm.settings'
     from django.core.wsgi import get_wsgi_application
     application = get_wsgi_application()
     ```

## 4. Final Finalizing
In your PythonAnywhere Bash console:
```bash
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py createsuperuser
```
**Reload your web app** from the Web tab. Your site is now live! 🎊
