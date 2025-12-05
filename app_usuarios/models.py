from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username} - {self.tipo}"


class Bicicleta(models.Model):
    codigo = models.IntegerField(unique=True)
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return f"Bicicleta {self.codigo}"


class Reserva(models.Model):
    aluno = models.ForeignKey(User, on_delete=models.CASCADE)
    bicicleta = models.ForeignKey('Bicicleta', on_delete=models.CASCADE, null=True, blank=True)  # <-- mudança
    status = models.CharField(max_length=20, default="pendente")
    data_hora_retirada = models.DateTimeField(null=True, blank=True)
    data_hora_devolucao = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Reserva {self.id}"


class Scan(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    seguranca = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10)
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Scan {self.tipo} - {self.reserva.id}"


# 🚨 NOVO MODEL PARA AS VAGAS
class Vaga(models.Model):
    numero = models.IntegerField(unique=True)
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return f"Vaga {self.numero}"
