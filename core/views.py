from django.shortcuts import render, redirect, get_object_or_404
from .models import Pedido, Estoque, FluxoGastos
from django.db.models import Q 
from datetime import date
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from weasyprint import HTML
from django.db.models import Sum
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils.timezone import now
from .models import Pedido, FluxoGastos
from django.db.models.functions import TruncMonth

@login_required
def listar_pedidos(request):
    pedidos = Pedido.objects.all()
    estoque_atual = Estoque.objects.aggregate(total=Sum('quantidade_disponivel'))['total'] or 0

    # Filtros (pesquisa e intervalo de datas)
    query = request.GET.get('q', '')
    if query:
        pedidos = pedidos.filter(
            Q(nome_cliente__icontains=query) |
            Q(tipo__icontains=query) |
            Q(telefone__icontains=query)
        )

    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    if data_inicio and data_fim:
        pedidos = pedidos.filter(data_pedido__range=[data_inicio, data_fim])

    # Pedidos atrasados
    pedidos_atrasados = pedidos.filter(data_entrega__lt=date.today())

    # Paginação
    paginator = Paginator(pedidos, 10)  # Mostra 10 pedidos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/listar_pedidos.html', {
        'page_obj': page_obj,
        'estoque_atual': estoque_atual, 
        'pedidos_atrasados': pedidos_atrasados,
        'query': query,
        'data_inicio': data_inicio,
        'data_fim': data_fim
    })

@login_required
def editar_fluxo(request, id):
    fluxo = get_object_or_404(FluxoGastos, id=id)

    if request.method == 'POST':
        fluxo.descricao = request.POST.get('descricao', fluxo.descricao)
        fluxo.tipo = request.POST.get('tipo', fluxo.tipo)
        fluxo.valor = float(request.POST.get('valor', fluxo.valor))
        fluxo.parcelado = request.POST.get('parcelado', 'off') == 'on'
        fluxo.parcelas = int(request.POST.get('parcelas', fluxo.parcelas))
        fluxo.save()
        messages.success(request, "Registro de fluxo de caixa atualizado com sucesso!")
        return redirect('listar_fluxo')

    return render(request, 'core/editar_fluxo.html', {'fluxo': fluxo})


@login_required
def excluir_fluxo(request, id):
    fluxo = get_object_or_404(FluxoGastos, id=id)
    fluxo.delete()
    messages.success(request, "Registro excluído com sucesso!")
    return redirect('listar_fluxo')


from django.shortcuts import render
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from .models import Pedido, FluxoGastos, Estoque

def dashboard(request):
    # Dados Resumo
    estoque_atual = Estoque.objects.aggregate(total=Sum('quantidade_disponivel'))['total'] or 0
    total_pedidos = Pedido.objects.count()
    pedidos_atrasados = Pedido.objects.filter(data_entrega__lt=date.today()).count()

    # Dados para Gráficos
    pedidos_por_mes = Pedido.objects.annotate(mes=TruncMonth('data_pedido')).values('mes').annotate(total=Count('id')).order_by('mes')
    meses = [item['mes'].strftime('%b %Y') for item in pedidos_por_mes if item['mes']]
    pedidos_totais = [item['total'] for item in pedidos_por_mes]

    fluxo = FluxoGastos.objects.values('tipo').annotate(total=Sum('valor'))
    entradas = sum(item['total'] for item in fluxo if item['tipo'] == 'entrada') or 0
    saidas = sum(item['total'] for item in fluxo if item['tipo'] == 'saida') or 0

    return render(request, 'core/dashboard.html', {
        'estoque_atual': estoque_atual,
        'total_pedidos': total_pedidos,
        'pedidos_atrasados': pedidos_atrasados,
        'meses': meses,
        'pedidos_totais': pedidos_totais,
        'entradas': entradas,
        'saidas': saidas,
    })

from django.http import HttpResponse
from openpyxl import Workbook

def exportar_pedidos_excel(request):
    # Cria o workbook e a planilha
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = 'Pedidos'

    # Cabeçalhos
    headers = [
        'Nome do Cliente', 'Telefone', 'Endereço', 'Tipo', 'Quantidade',
        'Largura (cm)', 'Espessura (cm)', 'Comprimento (cm)',
        'Valor Unitário', 'Valor Total', 'Data do Pedido',
        'Data de Entrega', 'Observação'
    ]
    sheet.append(headers)

    # Dados dos pedidos
    pedidos = Pedido.objects.all()
    for pedido in pedidos:
        sheet.append([
            pedido.nome_cliente,
            pedido.telefone,
            pedido.endereco,
            pedido.tipo,
            pedido.quantidade,
            pedido.largura,
            pedido.espessura,
            pedido.comprimento,
            pedido.valor_unitario,
            pedido.valor_total,
            pedido.data_pedido.strftime('%d/%m/%Y'),
            pedido.data_entrega.strftime('%d/%m/%Y'),
            pedido.observacao
        ])

    # Configura a resposta HTTP para o arquivo Excel
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=pedidos.xlsx'
    workbook.save(response)

    return response

@login_required
def calculo_financeiro(request):
    # Total de custos (somatório de todas as saídas no fluxo de caixa)
    total_custos = FluxoGastos.objects.filter(tipo='saida').aggregate(Sum('valor'))['valor__sum'] or 0

    # Total de receitas (somatório de todas as entradas no fluxo de caixa)
    total_receitas = FluxoGastos.objects.filter(tipo='entrada').aggregate(Sum('valor'))['valor__sum'] or 0

    # Total de vendas (lucro bruto)
    total_vendas = Pedido.objects.aggregate(Sum('valor_total'))['valor_total__sum'] or 0

    # Saldo geral (receitas - custos)
    saldo = total_receitas - total_custos

    # Lucro líquido (vendas - custos)
    lucro_liquido = total_vendas - total_custos

    return render(request, 'core/calculo_financeiro.html', {
        'total_custos': total_custos,
        'total_receitas': total_receitas,
        'total_vendas': total_vendas,
        'saldo': saldo,
        'lucro_liquido': lucro_liquido,
    })


@login_required
def editar_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id) 

    if request.method == 'POST':
        pedido.nome_cliente = request.POST.get('nome_cliente', pedido.nome_cliente).strip()
        pedido.telefone = request.POST.get('telefone', pedido.telefone).strip()
        pedido.endereco = request.POST.get('endereco', pedido.endereco).strip()
        pedido.tipo = request.POST.get('tipo', pedido.tipo).strip()
        pedido.quantidade = int(request.POST.get('quantidade', pedido.quantidade))
        pedido.valor_unitario = float(request.POST.get('valor_unitario', pedido.valor_unitario))
        pedido.observacao = request.POST.get('observacao', pedido.observacao).strip()
        pedido.data_pedido = request.POST.get('data_pedido', pedido.data_pedido)
        pedido.data_entrega = request.POST.get('data_entrega', pedido.data_entrega)

        pedido.save()
        return redirect('listar_pedidos') 

    return render(request, 'core/editar_pedido.html', {'pedido': pedido})

@login_required
def listar_fluxo(request):
    gastos = FluxoGastos.objects.all()
    fluxo = FluxoGastos.objects.all()
    parcelas_vencendo = fluxo.filter(parcelado=True, data__lte=date.today())
    return render(request, 'core/listar_fluxo.html', {'gastos': gastos, 'fluxo': fluxo,
        'parcelas_vencendo': parcelas_vencendo,})

@login_required
def registrar_fluxo(request):
    if request.method == 'POST':
        descricao = request.POST.get('descricao', "").strip()
        tipo = request.POST.get('tipo', "saida")
        valor = float(request.POST.get('valor', 0.0))
        parcelado = request.POST.get('parcelado', False) == "on"
        parcelas = int(request.POST.get('parcelas', 1))
        FluxoGastos.objects.create(
            descricao=descricao, tipo=tipo, valor=valor,
            parcelado=parcelado, parcelas=parcelas
        )
        return redirect('listar_fluxo')

    return render(request, 'core/registrar_fluxo.html')

@login_required
def excluir_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    pedido.delete()
    messages.success(request, f"Pedido de {pedido.nome_cliente} excluído com sucesso!")
    return redirect('listar_pedidos')


@login_required
def listar_estoque(request):
    estoque = Estoque.objects.first()
    alerta = None
    if estoque and estoque.quantidade_disponivel < estoque.limite_critico:
        alerta = f"Atenção: o estoque está abaixo do limite crítico ({estoque.limite_critico} unidades)."

    return render(request, 'core/listar_estoque.html', {'estoque': estoque, 'alerta': alerta})

@login_required
def relatorio_financeiro(request):
    entradas = FluxoGastos.objects.filter(tipo='entrada')
    saidas = FluxoGastos.objects.filter(tipo='saida')

    total_entradas = sum([entrada.valor for entrada in entradas])
    total_saidas = sum([saida.valor for saida in saidas])
    saldo = total_entradas - total_saidas

    return render(request, 'core/relatorio_financeiro.html', {
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'saldo': saldo,
    })


import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.http import HttpResponse
from .models import Pedido

@login_required
def relatorio_pedidos(request):
    # Dados para o gráfico
    pedidos = Pedido.objects.all()
    meses = [pedido.data_pedido.strftime('%B') for pedido in pedidos]
    valores = [pedido.valor_total for pedido in pedidos]

    # Gerar o gráfico
    plt.figure(figsize=(10, 6))
    plt.bar(meses, valores, color='blue')
    plt.title('Pedidos Mensais')
    plt.xlabel('Mês')
    plt.ylabel('Valor Total (R$)')
    plt.xticks(rotation=45)

    # Salvar o gráfico em memória
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Codificar a imagem em base64
    graph = base64.b64encode(image_png).decode('utf-8')

    return render(request, 'core/relatorio_pedidos.html', {'graph': graph})


@login_required
def atualizar_estoque(request):
    if request.method == 'POST':
        quantidade = int(request.POST.get('quantidade', 0))
        estoque = Estoque.objects.first()
        if not estoque:
            estoque = Estoque.objects.create(quantidade_disponivel=quantidade)
        else:
            estoque.quantidade_disponivel = quantidade
        estoque.save()
        return redirect('listar_estoque')

    return render(request, 'core/atualizar_estoque.html')

@login_required
def exportar_pedidos_pdf(request):
    # Recupera os pedidos do banco de dados
    pedidos = Pedido.objects.all()

    # Renderiza os pedidos em um template HTML
    html_string = render_to_string('core/pedidos_pdf.html', {'pedidos': pedidos})

    # Converte o HTML para PDF
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    # Retorna o PDF como resposta
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="pedidos.pdf"'

    return response

from django.utils.timezone import now
from django.db import transaction
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

@login_required
@transaction.atomic
def cadastrar_pedido(request):
    if request.method == 'POST':
        nome_cliente = request.POST.get('nome_cliente')
        telefone = request.POST.get('telefone')
        endereco = request.POST.get('endereco')
        tipo = request.POST.get('tipo')
        quantidade = int(request.POST.get('quantidade'))
        largura = float(request.POST.get('largura'))
        espessura = float(request.POST.get('espessura'))
        comprimento = float(request.POST.get('comprimento'))
        valor_unitario = float(request.POST.get('valor_unitario'))
        valor_total = quantidade * valor_unitario
        observacao = request.POST.get('observacao')
        data_pedido = request.POST.get('data_pedido')
        data_entrega = request.POST.get('data_entrega')

        # Atualiza o estoque
        estoque = Estoque.objects.first()
        if not estoque or estoque.quantidade_disponivel < quantidade:
            messages.error(request, "Estoque insuficiente para criar o pedido.")
            return redirect('listar_pedidos')

        # Subtrai a quantidade do estoque
        estoque.quantidade_disponivel -= quantidade
        estoque.save()

        # Cria o pedido
        Pedido.objects.create(
            nome_cliente=nome_cliente,
            telefone=telefone,
            endereco=endereco,
            tipo=tipo,
            quantidade=quantidade,
            largura=largura,
            espessura=espessura,
            comprimento=comprimento,
            valor_unitario=valor_unitario,
            valor_total=valor_total,
            observacao=observacao,
            data_pedido=data_pedido,
            data_entrega=data_entrega
        )

        messages.success(request, "Pedido criado com sucesso!")
        return redirect('listar_pedidos')

    # Calcula o estoque atual para exibição
    estoque_atual = Estoque.objects.aggregate(total=Sum('quantidade_disponivel'))['total'] or 0

    return render(request, 'core/cadastrar_pedido.html', {
        'estoque_atual': estoque_atual,  # Envia o estoque para o template
    })
