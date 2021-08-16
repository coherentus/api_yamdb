from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import UsersViewSet, signup, token

router = SimpleRouter()
router.register(r'users', UsersViewSet)

urlpatterns = [
    path('auth/signup/', signup),
    path('auth/token/', token),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
