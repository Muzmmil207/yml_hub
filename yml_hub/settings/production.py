from .base import DEBUG, MIDDLEWARE, env

if not DEBUG:
    ADMINS = [
        ("Admin", env("ADMIN_EMAIL") ),
    ]
      
    STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

