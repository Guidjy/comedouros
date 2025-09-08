from rest_framework import serializers
from .models import Lote, Brinco, Animal, Refeicao


class LoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = '__all__'
        

class BrincoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brinco
        fields = '__all__'
        

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = "__all__"
        
        
class RefeicaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refeicao
        fields = '__all__'