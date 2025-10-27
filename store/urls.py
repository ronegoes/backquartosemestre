from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Loja
    path('loja/', views.store, name='store'),
    path('produto/<int:id>/', views.product_detail, name='product_detail'),

    # Carrinho
    path('carrinho/', views.cart, name='cart'),
    path('adicionar/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remover/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('limpar-carrinho/', views.clear_cart, name='clear_cart'),

    # Pagamentos e pedidos
    path('checkout/', views.checkout, name='checkout'),
    path('pedido/', views.place_order, name='place_order'),
    path('pedido/concluido/', views.order_complete, name='order_complete'),
    path('pedido/pdf/', views.generate_receipt_pdf, name='generate_receipt_pdf'),
    path('paypal/retorno/', views.paypal_return, name='paypal_return'),

    # Dashboard extras
    path('produtos/', views.produtos, name='produtos'),
    path('clientes/', views.clientes, name='clientes'),
    path('pedidos/', views.pedidos, name='pedidos'),
]
