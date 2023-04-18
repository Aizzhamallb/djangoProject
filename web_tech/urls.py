from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static          #lib needs to open image
from django.conf import settings                    #lib needs to open image

from rest_framework.routers import SimpleRouter
from category.views import CategoryViewSet
from books.views import BookViewSet


from rest_framework import permissions
from drf_yasg.views import get_schema_view         # swagger lib
from drf_yasg import openapi                       # swagger lib

schema_view = get_schema_view(                     # swagger
   openapi.Info(
      title="Library API",
      default_version='v1',
      description="",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

router = SimpleRouter()
router.register('books', BookViewSet)
router.register('category', CategoryViewSet)

urlpatterns = [
    # drf_yasg       swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/v1/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    path('api/v1/account/', include('account.urls')),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include('profile1.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
