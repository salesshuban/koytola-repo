from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.staticfiles.views import serve
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

from .graphql.api import schema
from .graphql.views import GraphQLView


urlpatterns = [
    path("", TemplateView.as_view(template_name='index.html'), name="home"),

    # Graphql API
    path("graphql/", csrf_exempt(GraphQLView.as_view(schema=schema)), name="api"),

    # Admin Interface
    path('admin/', admin.site.urls),  # 'admin-board/' on production
]


if settings.DEBUG:
    import warnings

    try:
        import debug_toolbar
    except ImportError:
        warnings.warn(
            "The debug toolbar was not installed. Ignore the error. \
            settings.py should already have warned the user about it."
        )
    else:
        urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]

    urlpatterns += static("/media/", document_root=settings.MEDIA_ROOT) + [
        path("static/<path>", serve),
    ]
