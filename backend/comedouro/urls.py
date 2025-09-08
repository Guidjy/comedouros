from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'lotes', views.LoteViewSet)
router.register(r'brincos', views.BrincoViewSet)
router.register(r'animais', views.AnimalViewSet)
router.register(r'refeicoes', views.RefeicaoViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('consumo-diario/<str:animal_ou_lote>/<int:id>', views.consumo_diario)
]

