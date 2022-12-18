from rest_framework import routers
from rest_framework.urls import path
from django.urls import re_path

from api.views import *
from api.views.viewsets import *

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

"""Module responsible for storing API routes & OpenAPI config"""

schema_view = get_schema_view(
   openapi.Info(
      title="ARKultur API",
      default_version='v2',
      description="API storing and managing GeoJSON data for the ARKultur service",
      terms_of_service="https://arkultur.creative-rift.com/terms",
      contact=openapi.Contact(email="contact@arkultur.creative-rift.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

router = routers.SimpleRouter(trailing_slash=False,)
router.register(r'node', NodeViewset)
router.register(r'address', AddressViewset)
router.register(r'admin', AdminViewset)
router.register(r'customer', CustomerViewset)

urlpatterns = [
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('ping', PingView.as_view()),
    path('register', RegisterViewset.as_view({'post': 'create'})),
    re_path(r'^docs/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + router.urls
