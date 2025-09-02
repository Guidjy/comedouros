from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()
router.register(r'lotes', LoteViewSet)
router.register(r'animais', AnimalViewSet)
router.register(r'refeicoes', RefeicaoViewSet)


urlpatterns = [
    path('', include(router.urls)),
]

