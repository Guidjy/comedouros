from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

router = DefaultRouter()
router.register(r'', views.UserViewSet)

urlpatterns = [
    # CRUD usuários
    path('usuarios/', include(router.urls)),    
    # registrar
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('change_password/', views.ChangePasswordView.as_view(), name='change-password'),
    # login
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]