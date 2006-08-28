from django.conf import settings

# See __init__.py for documentation on setting the values of
# FCKEDITOR_CONNECTOR_ROOT and FCKEDITOR_CONNECTOR_URL

try:
    # if using the fckeditor package
    from fckeditor.settings import FCKEDITOR_JS

    FCKEDITOR_CONNECTOR_ROOT = settings.MEDIA_ROOT + FCKEDITOR_JS
    FCKEDITOR_CONNECTOR_URL = settings.MEDIA_URL + FCKEDITOR_JS
except ImportError:
    FCKEDITOR_CONNECTOR_ROOT = settings.MEDIA_ROOT + 'Media'
    FCKEDITOR_CONNECTOR_URL = settings.MEDIA_URL + 'Media'
    
