import os
import sys
import sae

sys.path.append(os.path.join(os.path.dirname(__file__), 'website'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'website.settings'

from website import wsgi
application = sae.create_wsgi_app(wsgi.application) 