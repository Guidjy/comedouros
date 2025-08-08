from django.db import models


class Lote(models.Model):
    nome = models.CharField(max_length=50, blank=True, null=True)
    n_animais = models.IntegerField(default=0)
    
    def __str__(self):
        return f'{self.id} - {self.nome}'
    

class Raca(models.Model):
    nome = models.CharField(max_length=50)
    
    def __str__(self):
        return f'{self.nome}'
    

class Animal(models.Model):
    class Sexo(models.TextChoices):
        MACHO = 'macho'
        FEMEA = 'femea'
        
    class Categoria(models.TextChoices):
        CORDEIRO = 'cordeiro(a)'
        BORREGO = 'borrego(a)'
        OVELHA = 'ovelha'
        CARNEIRO = 'carneiro'
        CAPAO = 'capão'
    
    brinco = models.IntegerField()
    animal_id_c = models.CharField(max_length=50)
    sexo = models.CharField(max_length=50, choices=Sexo.choices)
    meses = models.IntegerField()
    categoria = models.CharField(max_length=50, choices=Categoria.choices)
    peso_vivo_atual_kg = models.FloatField()
    frequencia_livre = models.BooleanField(default=False)
    frequencia = models.IntegerField(blank=True, null=True)
    
    lote = models.ForeignKey(Lote, related_name='animais', null=True, on_delete=models.SET_NULL)
    raca = models.ForeignKey(Raca, related_name='animais', null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f'{self.brinco} do lote {self.lote}'
    

class Refeicao(models.Model):
    data = models.DateField()
    horario = models.TimeField()
    duracao_min = models.FloatField()
    comportamento = models.TextField(max_length=2500, blank=True, null=True)
    consumo_kg = models.FloatField()
    peso_vivo_entrada_kg = models.FloatField()
    peso_vivo_final_kg = models.FloatField()
    gdm_entrada = models.FloatField()
    gdm_final = models.FloatField()
    
    animal = models.ForeignKey(Animal, related_name='refeições', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.animal} comeu {self.consumo_kg} - {self.data} as {self.horario}'
    
    