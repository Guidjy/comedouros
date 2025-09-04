from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import *

from .calculos import *


class LoteViewSet(viewsets.ModelViewSet):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer
    

class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['lote', 'raca', 'categoria']

    
class RefeicaoViewSet(viewsets.ModelViewSet):
    queryset = Refeicao.objects.all()
    serializer_class = RefeicaoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['animal']
    ordering_fields = ['data']
    ordering = ['-data']  # default ordering


@api_view(['GET'])
def consumo_diario(request, animal_ou_lote, id):
    """Gera um relatório do comportamento ingestivo do
    animal de id "animal_id".
    - Retorno:
        - consumo_diario: [{"dd-mm-aaaa": consumo_kg}]
    """
    # gera o consumo diário de um animal
    if animal_ou_lote == 'animal': 
        consumo = gera_consumo_diario_animal(id)
        if 'erro' in consumo:
            return Response(consumo, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(consumo, status=status.HTTP_200_OK)
    
    # gera o consumo diário de um lote
    elif animal_ou_lote == 'lote':
        consumo_lote = gera_consumo_diario_lote(id)
        if 'erro' in consumo_lote:
            Response(consumo_lote, status=status.HTTP_400_BAD_REQUEST)
        return Response(consumo_lote, status=status.HTTP_200_OK)
    
    # erro 
    else:
        return Response({'erro': f'argumento invárlido "{animal_ou_lote}"'}, status=status.HTTP_400_BAD_REQUEST)
        