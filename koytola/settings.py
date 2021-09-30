import os
import ast
from pathlib import Path
import warnings
from datetime import timedelta
import environ

import dj_database_url
import dj_email_url
import django_cache_url
import jaeger_client
import jaeger_client.config
import pkg_resources
import sentry_sdk
from django.core.exceptions import ImproperlyConfigured
from django.core.management.utils import get_random_secret_key
from django_prices.utils.formatting import get_currency_fraction
from pytimeparse import parse
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration

env = environ.Env(
    DEBUG=(bool, False)  # set casting, default value
)
environ.Env.read_env()


def get_bool_from_env(name, default_value):
    if name in os.environ:
        value = os.environ[name]
        try:
            return ast.literal_eval(value)
        except ValueError as e:
            raise ValueError("{} is an invalid value for {}".format(value, name)) from e
    return default_value


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
SITE_ID = 1
SITE_NAME = "koytola.com"
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "api.koytola.com", "panel.koytola.com", "*"]
ALLOWED_CLIENT_HOSTS = ["localhost", "127.0.0.1", "api.koytola.com", "34.94.218.150", "koytola.com", "panel.koytola.com"]
ALLOWED_GRAPHQL_ORIGINS = ["localhost", "34.94.218.150", "api.koytola.com", "*"]

ROOT_URLCONF = "koytola.urls"

WSGI_APPLICATION = "koytola.wsgi.application"

ADMINS = (
    ('Olcay Sari', 'olcay@koytola.com'),
)
MANAGERS = ADMINS

_DEFAULT_CLIENT_HOSTS = ["localhost", "127.0.0.1", "34.94.218.150", "api.koytola.com", "panel.koytola.com"]

if not ALLOWED_CLIENT_HOSTS:
    if DEBUG:
        ALLOWED_CLIENT_HOSTS = _DEFAULT_CLIENT_HOSTS
    else:
        raise ImproperlyConfigured(
            "ALLOWED_CLIENT_HOSTS environment variable must be set when DEBUG=False."
        )
DATA_UPLOAD_MAX_MEMORY_SIZE = 20621440
INTERNAL_IPS = ["localhost", "127.0.0.1", "34.94.218.150", "api.koytola.com"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'koytoladb',
        'USER': 'koytoladbadmin',
        'PASSWORD': '4FNa17Z3iV1FWCezAL',
        'HOST': '35.235.96.195',
        'PORT': '5432',
    }
}


TIME_ZONE = "UTC"
LANGUAGE_CODE = "en"
LANGUAGES = [
    ("en", "English"),
    ("es", "Spanish"),
    ("tr", "Turkey")
]
LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]
USE_I18N = True
USE_L10N = True
USE_TZ = True

# FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

EMAIL_URL = os.environ.get("EMAIL_URL")
SENDGRID_USERNAME = os.environ.get("SENDGRID_USERNAME")
SENDGRID_PASSWORD = os.environ.get("SENDGRID_PASSWORD")
if not EMAIL_URL and SENDGRID_USERNAME and SENDGRID_PASSWORD:
    EMAIL_URL = "smtp://%s:%s@smtp.gmail.com:587/?tls=True" % (
        SENDGRID_USERNAME,
        SENDGRID_PASSWORD,
    )
email_config = dj_email_url.parse(
    EMAIL_URL or "console://demo@example.com:console@example/"
)
EMAIL_FILE_PATH = email_config["EMAIL_FILE_PATH"]
EMAIL_HOST_USER = email_config["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = email_config["EMAIL_HOST_PASSWORD"]
EMAIL_HOST = email_config["EMAIL_HOST"]
EMAIL_PORT = email_config["EMAIL_PORT"]
EMAIL_BACKEND = email_config["EMAIL_BACKEND"]
EMAIL_USE_TLS = email_config["EMAIL_USE_TLS"]
EMAIL_USE_SSL = email_config["EMAIL_USE_SSL"]

# If enabled, make sure you have set proper frontend address in ALLOWED_CLIENT_HOSTS.
ENABLE_ACCOUNT_CONFIRMATION_BY_EMAIL = get_bool_from_env(
    "ENABLE_ACCOUNT_CONFIRMATION_BY_EMAIL", True
)

ENABLE_SSL = get_bool_from_env("ENABLE_SSL", False)

if ENABLE_SSL:
    SECURE_SSL_REDIRECT = not DEBUG
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)

MEDIA_URL = os.environ.get("MEDIA_URL", "/media/")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# STATIC_ROOT = os.path.join(BASE_DIR, "koytola/static")
# STATIC_URL = os.environ.get("STATIC_URL", "/static/")
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

STATICFILES_DIRS = [
    ("images", os.path.join(BASE_DIR, "koytola", "images"))
]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

context_processors = [
    "django.template.context_processors.debug",
    "django.template.context_processors.request",
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    "django.template.context_processors.media",
    "django.template.context_processors.static",
    "koytola.site.context_processors.site",
]

loaders = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "OPTIONS": {
            "debug": DEBUG,
            "context_processors": context_processors,
            "loaders": loaders,
            "string_if_invalid": '<< MISSING VARIABLE "%s" >>' if DEBUG else "",
        },
    }
]

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ.get("SECRET_KEY")

if not SECRET_KEY and DEBUG:
    warnings.warn("SECRET_KEY not configured, using a random temporary key.")
    SECRET_KEY = get_random_secret_key()

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "koytola.core.middleware.request_time",
    "koytola.core.middleware.country",
    "koytola.core.middleware.currency",
    "koytola.core.middleware.site",
    "koytola.core.middleware.plugins",
    "koytola.core.middleware.jwt_refresh_token_middleware",
]


CORS_ALLOWED_ORIGINS = [
    "http://34.94.218.150",
    "https://api.koytola.com",
    "https://panel.koytola.com",
    "https://koytola.com",
    "http://localhost",
]
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
CORS_ALLOW_CREDENTIALS = True


INSTALLED_APPS = [
    # Django modules
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    "django.contrib.postgres",
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    # Local apps
    "koytola.plugins",
    "koytola.account",
    "koytola.analytics",
    "koytola.app",
    "koytola.blog",
    "koytola.core",
    "koytola.graphql",
    "koytola.helpdesk",
    "koytola.invoice",
    "koytola.menu",
    "koytola.news",
    "koytola.order",
    "koytola.page",
    "koytola.payment",
    "koytola.profile",
    "koytola.product",
    "koytola.seo",
    "koytola.site",
    "koytola.webhook",

    # External apps
    "versatileimagefield",
    # "django_measurement",
    # "django_prices",
    # "django_prices_openexchangerates",
    # "django_prices_vatlayer",
    "graphene_django",
    "mptt",
    "django_countries",
    "django_filters",
    "phonenumber_field",
    'corsheaders',
]

CRONJOBS = [
    ('*/1 * * * *', 'koytola.product.cron.open_exchange_rates_cron_job')
]

APPEND_SLASH = False
ENABLE_DEBUG_TOOLBAR = get_bool_from_env("ENABLE_DEBUG_TOOLBAR", False)
if ENABLE_DEBUG_TOOLBAR:
    # Ensure the graphiql debug toolbar is actually installed before adding it
    try:
        __import__("graphiql_debug_toolbar")
    except ImportError as exc:
        msg = (
            f"{exc} -- Install the missing dependencies by "
            f"running `pip install -r requirements_dev.txt`"
        )
        warnings.warn(msg)
    else:
        INSTALLED_APPS += ["django.forms", "debug_toolbar", "graphiql_debug_toolbar"]
        MIDDLEWARE.append("koytola.graphql.middleware.DebugToolbarMiddleware")

        DEBUG_TOOLBAR_PANELS = [
            "ddt_request_history.panels.request_history.RequestHistoryPanel",
            "debug_toolbar.panels.timer.TimerPanel",
            "debug_toolbar.panels.headers.HeadersPanel",
            "debug_toolbar.panels.request.RequestPanel",
            "debug_toolbar.panels.sql.SQLPanel",
            "debug_toolbar.panels.profiling.ProfilingPanel",
        ]
        DEBUG_TOOLBAR_CONFIG = {"RESULTS_CACHE_SIZE": 100}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"level": "INFO", "handlers": ["default"]},
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        },
        "json": {
            "()": "koytola.core.logging.JsonFormatter",
            "datefmt": "%Y-%m-%dT%H:%M:%SZ",
            "format": (
                "%(asctime)s %(levelname)s %(lineno)s %(message)s %(name)s "
                + "%(pathname)s %(process)d %(threadName)s"
            ),
        },
        "verbose": {
            "format": (
                "%(levelname)s %(name)s %(message)s [PID:%(process)d:%(threadName)s]"
            )
        },
    },
    "handlers": {
        "default": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose" if DEBUG else "json",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server" if DEBUG else "json",
        },
    },
    "loggers": {
        "django": {"level": "INFO", "propagate": True},
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
        "koytola": {"level": "DEBUG", "propagate": True},
        "koytola.graphql.errors.handled": {
            "handlers": ["default"],
            "level": "ERROR",
            "propagate": False,
        },
        "graphql.execution.utils": {"propagate": False},
    },
}

AUTH_USER_MODEL = "account.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        "OPTIONS": {"min_length": 8},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

DEFAULT_COUNTRY = os.environ.get("DEFAULT_COUNTRY", "US")
DEFAULT_CURRENCY = os.environ.get("DEFAULT_CURRENCY", "USD")
DEFAULT_DECIMAL_PLACES = get_currency_fraction(DEFAULT_CURRENCY)
DEFAULT_MAX_DIGITS = 12
DEFAULT_CURRENCY_CODE_LENGTH = 4

# The default max length for the display name of the
# sender email address.
# Following the recommendation of https://tools.ietf.org/html/rfc5322#section-2.1.1
DEFAULT_MAX_EMAIL_DISPLAY_NAME_LENGTH = 78

# note: having multiple currencies is not supported yet
AVAILABLE_CURRENCIES = [DEFAULT_CURRENCY]


def get_host():
    from django.contrib.sites.models import Site

    return Site.objects.get_current().domain


PAYMENT_HOST = get_host

PAYMENT_MODEL = "order.Payment"

MAX_CHECKOUT_LINE_QUANTITY = int(os.environ.get("MAX_CHECKOUT_LINE_QUANTITY", 50))

TEST_RUNNER = "koytola.tests.runner.PytestTestRunner"

PLAYGROUND_ENABLED = get_bool_from_env("PLAYGROUND_ENABLED", True)

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
    "images": [
        ("image_gallery", "thumbnail__540x540"),
        ("image_gallery_2x", "thumbnail__1080x1080"),
        ("image_small", "thumbnail__60x60"),
        ("image_small_2x", "thumbnail__120x120"),
        ("image_list", "thumbnail__255x255"),
        ("image_list_2x", "thumbnail__510x510"),
    ],
    "products": [
        ("product_gallery", "thumbnail__540x540"),
        ("product_gallery_2x", "thumbnail__1080x1080"),
        ("product_small", "thumbnail__60x60"),
        ("product_small_2x", "thumbnail__120x120"),
        ("product_list", "thumbnail__255x255"),
        ("product_list_2x", "thumbnail__510x510"),
    ],
    "background_images": [("header_image", "thumbnail__1080x440")],
    "user_avatars": [("default", "thumbnail__445x445")],
    "company_logos": [
        ("image_small", "thumbnail__60x60"),
        ("image_medium", "thumbnail__120x120"),
        ("image_medium", "thumbnail__180x180"),
        ("image_big", "thumbnail__240x240"),
    ],
}

VERSATILEIMAGEFIELD_SETTINGS = {
    # Images should be pre-generated on Production environment
    "create_images_on_demand": get_bool_from_env("CREATE_IMAGES_ON_DEMAND", DEBUG)
}

PLACEHOLDER_IMAGES = {
    60: "images/placeholder60x60.png",
    120: "images/placeholder120x120.png",
    255: "images/placeholder255x255.png",
    540: "images/placeholder540x540.png",
    1080: "images/placeholder1080x1080.png",
}

DEFAULT_PLACEHOLDER = "images/placeholder255x255.png"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "koytola.core.auth_backend.JSONWebTokenBackend",
]

# CELERY SETTINGS
CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = (
    os.environ.get("CELERY_BROKER_URL", os.environ.get("CLOUDAMQP_URL")) or ""
)
CELERY_TASK_ALWAYS_EAGER = not CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", None)

# Change this value if your application is running behind a proxy,
# e.g. HTTP_CF_Connecting_IP for Cloudflare or X_FORWARDED_FOR
REAL_IP_ENVIRON = os.environ.get("REAL_IP_ENVIRON", "REMOTE_ADDR")

# The maximum length of a graphql query to log in tracings
OPENTRACING_MAX_QUERY_LENGTH_LOG = 2000

# Slugs for menus precreated in Django migrations
DEFAULT_MENUS = {"top_menu_name": "navbar", "bottom_menu_name": "footer"}

#  Sentry
SENTRY_DSN = os.environ.get("SENTRY_DSN")
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN, integrations=[CeleryIntegration(), DjangoIntegration()]
    )

GRAPHENE = {
    "RELAY_CONNECTION_ENFORCE_FIRST_OR_LAST": True,
    "RELAY_CONNECTION_MAX_LIMIT": 100,
    "MIDDLEWARE": [
        "koytola.graphql.middleware.OpentracingGrapheneMiddleware",
        "koytola.graphql.middleware.JWTMiddleware",
        "koytola.graphql.middleware.app_middleware",
    ],
}

PLUGINS_MANAGER = "koytola.plugins.manager.PluginsManager"

PLUGINS = []
# PLUGINS = [
#     "koytola.payment.gateways.dummy.plugin.DummyGatewayPlugin",
#     "koytola.plugins.webhook.plugin.WebhookPlugin",
#     "koytola.payment.gateways.dummy_credit_card.plugin.DummyCreditCardGatewayPlugin",
#     "koytola.payment.gateways.stripe.plugin.StripeGatewayPlugin",
#     "koytola.payment.gateways.braintree.plugin.BraintreeGatewayPlugin",
#     "koytola.plugins.invoicing.plugin.InvoicingPlugin",
# ]

# Plugin discovery
installed_plugins = pkg_resources.iter_entry_points("koytola.plugins")
for entry_point in installed_plugins:
    plugin_path = "{}.{}".format(entry_point.module_name, entry_point.attrs[0])
    if plugin_path not in PLUGINS:
        if entry_point.name not in INSTALLED_APPS:
            INSTALLED_APPS.append(entry_point.name)
        PLUGINS.append(plugin_path)

if (
    not DEBUG
    and ENABLE_ACCOUNT_CONFIRMATION_BY_EMAIL
    and ALLOWED_CLIENT_HOSTS == _DEFAULT_CLIENT_HOSTS
):
    raise ImproperlyConfigured(
        "Make sure you've added frontend address to ALLOWED_CLIENT_HOSTS "
        "if ENABLE_ACCOUNT_CONFIRMATION_BY_EMAIL is enabled."
    )

# Initialize a simple and basic Jaeger Tracing integration
# for open-tracing if enabled.


# If running locally, set:
#   JAEGER_AGENT_HOST=localhost
if "JAEGER_AGENT_HOST" in os.environ:
    jaeger_client.Config(
        config={
            "sampler": {"type": "const", "param": 1},
            "local_agent": {
                "reporting_port": os.environ.get(
                    "JAEGER_AGENT_PORT", jaeger_client.config.DEFAULT_REPORTING_PORT
                ),
                "reporting_host": os.environ.get("JAEGER_AGENT_HOST"),
            },
            "logging": get_bool_from_env("JAEGER_LOGGING", False),
        },
        service_name="koytola",
        validate=True,
    ).initialize_tracer()


# Some cloud providers (Heroku) export REDIS_URL variable instead of CACHE_URL
REDIS_URL = os.environ.get("REDIS_URL")
if REDIS_URL:
    CACHE_URL = os.environ.setdefault("CACHE_URL", REDIS_URL)
CACHES = {"default": django_cache_url.config()}

# Default False because frontend and dashboard don't support expiration of token
JWT_EXPIRE = get_bool_from_env("JWT_EXPIRE", False)
JWT_TTL_ACCESS = timedelta(seconds=parse(os.environ.get("JWT_TTL_ACCESS", "5 minutes")))
JWT_TTL_APP_ACCESS = timedelta(
    seconds=parse(os.environ.get("JWT_TTL_APP_ACCESS", "5 minutes"))
)
JWT_TTL_REFRESH = timedelta(seconds=parse(os.environ.get("JWT_TTL_REFRESH", "30 days")))


JWT_TTL_REQUEST_EMAIL_CHANGE = timedelta(
    seconds=parse(os.environ.get("JWT_TTL_REQUEST_EMAIL_CHANGE", "1 hour")),
)
# API_URI=http://localhost:8000/graphql/ npm start
