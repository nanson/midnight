from django.conf import settings
import os


settings.STATICFILES_DIRS += (
        os.path.join(settings.BASE_DIR, "midnight_banners", "static"),
)
