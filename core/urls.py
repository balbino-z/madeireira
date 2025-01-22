from django.urls import path
from . import views

urlpatterns = [
    # Rotas para pedidos
    path('', views.dashboard, name='dashboard'),  # Dashboard
    path('pedidos/', views.listar_pedidos, name='listar_pedidos'),  # Listar pedidos
    path('cadastrar/', views.cadastrar_pedido, name='cadastrar_pedido'),  # Cadastrar pedido
    path('editar/<int:id>/', views.editar_pedido, name='editar_pedido'),  # Editar pedido
    path('excluir/<int:id>/', views.excluir_pedido, name='excluir_pedido'),  # Excluir pedido

    path('exportar-pedidos-excel/', views.exportar_pedidos_excel, name='exportar_pedidos_excel'),

    # Rotas para estoque
    path('estoque/', views.listar_estoque, name='listar_estoque'),  # Visualizar estoque
    path('estoque/atualizar/', views.atualizar_estoque, name='atualizar_estoque'),  # Atualizar estoque

    # Rotas para fluxo de caixa
    path('fluxo/', views.listar_fluxo, name='listar_fluxo'),  # Listar fluxo de caixa
    path('fluxo/registrar/', views.registrar_fluxo, name='registrar_fluxo'),  # Registrar entrada/saída
    path('exportar-pedidos/', views.exportar_pedidos_pdf, name='exportar_pedidos_pdf'),  # Exportar para PDF
    path('calculo-financeiro/', views.calculo_financeiro, name='calculo_financeiro'),  # Rota para cálculo financeiro
    path('fluxo/editar/<int:id>/', views.editar_fluxo, name='editar_fluxo'),
    path('fluxo/excluir/<int:id>/', views.excluir_fluxo, name='excluir_fluxo'),
]
