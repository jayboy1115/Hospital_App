# Use SQLite for tests to avoid PostgreSQL sequence issues
from .settings import *
import sys

if 'test' in sys.argv or 'test_coverage' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
