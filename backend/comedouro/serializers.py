from rest_framework import serializers
from .models import Lote, Raca, Animal, Refeicao


class LoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = '__all__'
        
        
class RacaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raca
        fields = '__all__'
        
        
from rest_framework import serializers
from .models import Animal, Raca

class AnimalSerializer(serializers.ModelSerializer):
    # Optionally, you can accept raca by name instead of ID
    raca = serializers.CharField()

    class Meta:
        model = Animal
        fields = "__all__"

    def create(self, validated_data):
        # Get the raca name from validated data
        raca_nome = validated_data.pop("raca", None)

        if raca_nome:
            # Get or create the Raca object
            raca_obj, _ = Raca.objects.get_or_create(nome=raca_nome)
            validated_data["raca"] = raca_obj

        # Let DRF handle the Animal creation
        return super().create(validated_data)

        
        
class RefeicaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refeicao
        fields = '__all__'