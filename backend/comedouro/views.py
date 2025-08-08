from rest_framework import viewsets

from .models import *
from .serializers import *


class LoteViewSet(viewsets.ModelViewSet):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer


class RacaViewSet(viewsets.ModelViewSet):
    queryset = Raca.objects.all()
    serializer_class = RacaSerializer
    
    
class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

    
class RefeicaoViewSet(viewsets.ModelViewSet):
    queryset = Refeicao.objects.all()
    serializer_class = RefeicaoSerializer
