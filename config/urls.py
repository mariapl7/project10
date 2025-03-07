from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('newsletter.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include(router.urls)),
    path('api/', include('users.urls')),
]
