from django.db import models
from django.utils import timezone

class Pedido(models.Model):
    nome_cliente = models.CharField(max_length=100, default="")
    telefone = models.CharField(max_length=15, default="")
    endereco = models.TextField(default="")
    tipo = models.CharField(max_length=50, default="")
    quantidade = models.IntegerField(default=1)
    largura = models.FloatField(default=0.0)
    espessura = models.FloatField(default=0.0)
    comprimento = models.FloatField(default=0.0)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    observacao = models.TextField(blank=True, null=True)
    data_pedido = models.DateField(default=timezone.now)
    data_entrega = models.DateField(default=timezone.now)
    class Meta:
        ordering = ['-id']

    def calcular_valor_total(self):
        self.valor_total = self.quantidade * self.valor_unitario
        return self.valor_total

    def save(self, *args, **kwargs):
        self.calcular_valor_total()
        super().save(*args, **kwargs)

        from django.db import models
from django.utils import timezone

# Modelo de Estoque
class Estoque(models.Model):
    quantidade_disponivel = models.IntegerField(default=0)  # Total de madeiras no estoque
    limite_critico = models.IntegerField(default=50)  # Limite mínimo para alerta
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Estoque: {self.quantidade_disponivel} unidades"


    def __str__(self):
        return f"Estoque: {self.quantidade_disponivel} unidades"


class FluxoGastos(models.Model):
    descricao = models.CharField(max_length=255)  # Descrição da entrada/saída
    tipo = models.CharField(max_length=50, choices=[('entrada', 'Entrada'), ('saida', 'Saída')])
    valor = models.DecimalField(max_digits=10, decimal_places=2)  # Valor da transação
    data = models.DateField(default=timezone.now)  # Data da transação
    parcelado = models.BooleanField(default=False)  # Indica se é parcelado
    parcelas = models.IntegerField(default=1)  # Número de parcelas, se for parcelado

    def __str__(self):
        return f"{self.tipo.capitalize()}: {self.descricao} - R$ {self.valor}"


    def __str__(self):
        return f"Pedido {self.id} - {self.nome_cliente}"
