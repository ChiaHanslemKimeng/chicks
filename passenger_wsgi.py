import os
import sys

# Set up the paths
# The path to your project folder (e.g., /home/globteiq/universalpoultryfarm.com)
sys.path.insert(0, os.getcwd())

# Add the project directory to sys.path
# This ensures that 'poultry_farm' can be found
sys.path.append(os.path.join(os.getcwd(), '..'))

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'poultry_farm.settings'

# Import the Django application
from poultry_farm.wsgi import application
