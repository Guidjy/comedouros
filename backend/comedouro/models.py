from django.db import models
from datetime import date


class Lote(models.Model):
    nome = models.CharField(max_length=50, blank=True, null=True)
    n_animais = models.IntegerField(default=0)
    
    def __str__(self):
        return f'{self.nome} ({self.id})'
    

class Brinco(models.Model):
    tag_id = models.CharField(max_length=128, blank=True, null=True)
    numero = models.CharField(max_length=128)
    
    def __str__(self):
        if self.numero:
            return f'{self.numero}'
        return f'{self.tag_id}'
    

class Animal(models.Model):
    class Sexo(models.TextChoices):
        MACHO = 'macho'
        FEMEA = 'femea'
    
    sexo = models.CharField(max_length=50, choices=Sexo.choices, null=True, blank=True)
    meses = models.IntegerField(blank=True, null=True)
    raca = models.CharField(blank=True, null=True)
    categoria = models.CharField(blank=True, null=True)
    frequencia_livre = models.BooleanField(default=False)
    frequencia = models.IntegerField(blank=True, null=True)
    
    brinco = models.ForeignKey(Brinco, related_name='animais', null=True, on_delete=models.SET_NULL)
    lote = models.ForeignKey(Lote, related_name='animais', null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f'{self.brinco} do lote {self.lote}'
    
    def save(self, *args, **kwargs):
        # verifica se um animal está sendo criado ou atualizado
        is_new = self.pk is None
        super().save(*args, **kwargs)
        # se um novo animal estiver sendo criado, incrementa o número de animais no lote
        if is_new and self.lote:
            self.lote.n_animais += 1
            self.lote.save()

    def delete(self, *args, **kwargs):
        # decrementa o número de animais no lote quando um é deletado
        if self.lote:
            self.lote.n_animais -= 1
            self.lote.save()
        super().delete(*args, **kwargs)
        

class Refeicao(models.Model):
    # dados coletados no comedouro
    horario_entrada = models.TimeField()
    horario_saida = models.TimeField()
    consumo_kg = models.FloatField()
    peso_vivo_entrada_kg = models.FloatField()
    
    data = models.DateField(default=date.today)
    comportamento = models.TextField(max_length=2500, blank=True, null=True)
    
    animal = models.ForeignKey(Animal, related_name='refeições', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.animal} comeu {self.consumo_kg} - {self.data} as {self.horario_entrada}'
    
    