from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import *

from .calculos import comportamento_ingestivo as ci


class LoteViewSet(viewsets.ModelViewSet):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer
    

class BrincoViewSet(viewsets.ModelViewSet):
    queryset = Brinco.objects.all()
    serializer_class = BrincoSerializer
    

class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['lote', 'raca', 'categoria']

    
class RefeicaoViewSet(viewsets.ModelViewSet):
    queryset = Refeicao.objects.all()
    serializer_class = RefeicaoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['animal', 'data']
    ordering_fields = ['data']
    ordering = ['-data']  # default ordering


@api_view(['GET'])
def consumo_diario(request, animal_ou_lote, id, data=None):
    """Gera um relatório do comportamento ingestivo do
    animal de id "animal_id".
    - Retorno:
        - consumo_diario: [{"dd-mm-aaaa": consumo_kg}]
    """
    # gera o consumo diário de um animal
    if animal_ou_lote == 'animal': 
        if data is None:
            consumo_diario = ci.gera_consumo_diario_animal(id)
        else:
            consumo_diario = ci.gera_consumo_diario_animal(id, data)
        
        if 'erro' in consumo_diario:
            return Response(consumo_diario, status=status.HTTP_400_BAD_REQUEST)
        return Response(consumo_diario, status=status.HTTP_200_OK)
        
    # gera o consumo diário de um lote
    elif animal_ou_lote == 'lote':
        if data is None:
            consumo_diario = ci.gera_consumo_diario_lote(id)
        else:
            consumo_diario = ci.gera_consumo_diario_lote(id, data)
        if 'erro' in consumo_diario:
            return Response(consumo_diario, status=status.HTTP_400_BAD_REQUEST)
        return Response(consumo_diario, status=status.HTTP_200_OK)
    
    # erro 
    else:
        return Response({'erro': f'argumento invárlido "{animal_ou_lote}"'}, status=status.HTTP_400_BAD_REQUEST)
        