import sys
 
sys.path.insert(0, 'C:/Users/laim/Desktop/SLAPS/django/app')
 
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

application = get_wsgi_application()