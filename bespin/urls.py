"""Module responsible for storing API routes & OpenAPI config"""

from rest_framework import routers
from rest_framework import permissions
from rest_framework.urls import path

from django.urls import re_path
from django.conf.urls import include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api.views import LoginView, LogoutView, PingView, ConfirmAccountView, ResetPasswordView
from api.views.viewsets import NodeViewset, AddressViewset, RegisterViewset, CustomerViewset, \
        AdminViewset

# SchemaView provides view for OpenAPI specifications (using Redoc template)
SchemaView = get_schema_view(
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
    path('confirm', ConfirmAccountView.as_view()),
    path('reset', ResetPasswordView.as_view()),
    path('register', RegisterViewset.as_view({'post': 'create'})),
    re_path(r'^docs/$', SchemaView.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^auth/', include('trench.urls')),
    re_path(r'^auth/', include('trench.urls.authtoken')),
] + router.urls
