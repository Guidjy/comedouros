from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'lote', views.LoteViewSet)
router.register(r'animal', views.AnimalViewSet)
router.register(r'refeicao', views.RefeicaoViewSet)

urlpatterns = [
    path('', views.teste),
    path('', include(router.urls)),
]