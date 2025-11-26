from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    TIPOS = [
        ('aluno', 'Aluno'),
        ('seguranca', 'Segurança'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    matricula = models.CharField(max_length=20, blank=True, null=True)
    curso = models.CharField(max_length=100, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.tipo})"


class Bicicleta(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return f"Bike {self.codigo} - {'Livre' if self.disponivel else 'Ocupada'}"


class Reserva(models.Model):
    aluno = models.ForeignKey(User, on_delete=models.CASCADE)
    bicicleta = models.ForeignKey(Bicicleta, on_delete=models.CASCADE)
    data_hora_reserva = models.DateTimeField(auto_now_add=True)
    data_hora_retirada = models.DateTimeField(blank=True, null=True)
    data_hora_devolucao = models.DateTimeField(blank=True, null=True)

    STATUS = [
        ('pendente', 'Pendente'),
        ('retirada', 'Retirada'),
        ('devolvida', 'Devolvida'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='pendente')

    def __str__(self):
        return f"Reserva #{self.id} - {self.aluno.username}"


class Scan(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    seguranca = models.ForeignKey(User, on_delete=models.CASCADE)
    data_hora = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=20, choices=[
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ])

    def __str__(self):
        return f"Scan {self.tipo} - {self.reserva.id}"
