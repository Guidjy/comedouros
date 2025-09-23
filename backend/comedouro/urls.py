from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'lotes', views.LoteViewSet)
router.register(r'brincos', views.BrincoViewSet)
router.register(r'animais', views.AnimalViewSet)
router.register(r'refeicoes', views.RefeicaoViewSet)


urlpatterns = [
    # CRUD
    path('', include(router.urls)),
    path('cria-animais-com-csv/', views.cria_animais_com_csv),
    # comportamento ingestivo
    path('consumo-diario/<str:animal_ou_lote>/<int:numero>/', views.consumo_diario),
    path('consumo-diario/<str:animal_ou_lote>/<int:numero>/<str:data>/', views.consumo_diario),
    path('minuto-por-refeicao/<str:animal_ou_lote>/<int:numero>/', views.minuto_por_refeicao),
    path('minuto-por-refeicao/<str:animal_ou_lote>/<int:numero>/<str:data>/', views.minuto_por_refeicao),
    # desempenho
    path('evolucao-peso-por-dia/<int:numero>/', views.evolucao_peso_por_dia),
    path('evolucao-consumo-diario/<str:animal_ou_lote>/<int:numero>/', views.evolucao_consumo_diario),
    path('evolucao-ganho/<int:numero>/', views.evolucao_ganho),
    path('evolucao-gmd/<int:numero>/', views.evolucao_gmd),
]

