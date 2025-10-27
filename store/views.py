import io
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Cliente, Product


# ==============================
# 🏠 Dashboard (página inicial)
# ==============================
def dashboard(request):
    return render(request, 'dashboard.html')


# ==============================
# 🏬 Loja (lista de produtos)
# ==============================
def store(request):
    products = Product.objects.all()
    return render(request, 'store.html', {'products': products})


# ==============================
# 📦 Detalhes de produto
# ==============================
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})


# ==============================
# 🛒 Carrinho
# ==============================
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {
            'name': product.name,
            'price': float(product.price),
            'quantity': 1
        }

    request.session['cart'] = cart
    messages.success(request, f"{product.name} adicionado ao carrinho!")
    return redirect('cart')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('cart')


def clear_cart(request):
    request.session['cart'] = {}
    request.session.modified = True
    return redirect('cart')


def cart(request):
    cart = request.session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render(request, 'cart.html', {'cart': cart, 'total': total})


# ==============================
# 💳 Checkout
# ==============================
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Seu carrinho está vazio.")
        return redirect('store')

    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render(request, 'checkout.html', {'cart': cart, 'total': total})


# ==============================
# 💰 Escolher método de pagamento
# ==============================
# ==============================
# 💰 Escolher método de pagamento
# ==============================
def place_order(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Seu carrinho está vazio.")
        return redirect('store')

    total = sum(item['price'] * item['quantity'] for item in cart.values())
    context = {'cart': cart, 'total': total}

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        # ========================
        # 🔹 PIX
        # ========================
        if payment_method == 'pix':
            context.update({
                'show_pix': True,
                'pix_key': "92617581187",
                'pix_qr': '/static/images/pix_qrcode.png',  # caminho corrigido
            })
            return render(request, 'order_complete.html', context)

        # ========================
        # 🔹 Pagamento confirmado via PIX
        # ========================
        elif payment_method == 'pix_paid':
            return redirect('generate_receipt_pdf')

        # ========================
        # 🔹 Cartão
        # ========================
        elif payment_method == 'cartao':
            context.update({'show_card': True})
            return render(request, 'order_complete.html', context)

        # ========================
        # 🔹 PayPal
        # ========================
        elif payment_method == 'paypal':
            # Em vez de ir direto ao dashboard, abre a tela PayPal simulada
            context.update({'show_paypal': True})
            return render(request, 'order_complete.html', context)

        elif payment_method == 'paypal_paid':
            return redirect('paypal_return')

        else:
            messages.error(request, "Método de pagamento inválido.")
            return redirect('checkout')

    return render(request, 'order_complete.html', context)


# ==============================
# ✅ Concluir pedido
# ==============================
def order_complete(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Seu carrinho está vazio.")
        return redirect('store')

    total = sum(item['price'] * item['quantity'] for item in cart.values())

    if request.method == 'POST':
        messages.success(request, "Pedido finalizado com sucesso! Obrigado pela compra.")
        request.session['cart'] = {}
        return redirect('dashboard')

    return render(request, 'order_complete.html', {'cart': cart, 'total': total})


# ==============================
# 🅿️ PayPal simulado
# ==============================
def paypal_return(request):
    messages.success(request, "Pagamento via PayPal confirmado (simulação). Obrigado!")
    request.session['cart'] = {}
    return redirect('dashboard')


# ==============================
# 📄 PDF do recibo
# ==============================
def generate_receipt_pdf(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Seu carrinho está vazio.")
        return redirect('store')

    total = sum(item['price'] * item['quantity'] for item in cart.values())
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, "Recibo de Compra - Loja Roneii")
    p.setFont("Helvetica", 12)
    y = height - 90

    for idx, (prod_id, item) in enumerate(cart.items(), start=1):
        p.drawString(50, y, f"{idx}. {item['name']} x{item['quantity']} - R$ {item['price'] * item['quantity']:.2f}")
        y -= 18

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y - 10, f"Total: R$ {total:.2f}")
    p.showPage()
    p.save()
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="recibo.pdf"'
    return response


# ==============================
# 🔹 Páginas extras do dashboard
# ==============================
def produtos(request):
    return render(request, 'produtos.html')

def clientes(request):
    return render(request, 'clientes.html')

def pedidos(request):
    return render(request, 'pedidos.html')
