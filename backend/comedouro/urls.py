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
    # comportamento ingestivo
    path('consumo-diario/<str:animal_ou_lote>/<int:id>/', views.consumo_diario),
    path('consumo-diario/<str:animal_ou_lote>/<int:id>/<str:data>/', views.consumo_diario),
    path('minuto-por-refeicao/<str:animal_ou_lote>/<int:id>/', views.minuto_por_refeicao),
    path('minuto-por-refeicao/<str:animal_ou_lote>/<int:id>/<str:data>/', views.minuto_por_refeicao),
]

