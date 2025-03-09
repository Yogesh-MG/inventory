# inventory/views.py
from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views import View
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Purchase, Sale, Stock, Seller, Buyer, Goods
from .forms import PurchaseForm, SaleForm

# Helper function to check if user is Owner
def is_owner(user):
    return user.is_authenticated and user.groups.filter(name='Owner').exists()

# Helper function to check if user is Employee
def is_employee(user):
    return user.is_authenticated and user.groups.filter(name='Employee').exists()

def is_owner_or_employee(user):  # New helper for owner or employee access
    return user.is_authenticated and (user.groups.filter(name='Owner').exists() or user.groups.filter(name='Employee').exists())


# New Index View
def index(request):
    if request.user.is_authenticated:
        if is_owner(request.user):
            return redirect('stock_list')
        elif is_employee(request.user):
            return redirect('add_sale')
    return render(request, 'index.html')

# Existing views with access control
@login_required
@user_passes_test(is_owner, login_url='/login/')
def add_purchase(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stock_list')
    else:
        form = PurchaseForm()
    return render(request, 'add_purchase.html', {'form': form})

@login_required
def add_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            form.save()  # Only saves if validation passes
            return redirect('stock_list')
        # If invalid (e.g., stock error), render form with errors
    else:
        form = SaleForm()
    return render(request, 'add_sale.html', {'form': form})

@login_required
@user_passes_test(is_owner, login_url='/login/')
def stock_list(request):
    goods = Goods.objects.all()
    for good in goods:
        Stock.objects.get_or_create(goods=good, defaults={'quantity': 0})
    stocks = Stock.objects.all()
    return render(request, 'stock_list.html', {'stocks': stocks})

@login_required
@user_passes_test(is_owner, login_url='/login/')
def bill_summary(request):
    purchases = Purchase.objects.all()
    sales = Sale.objects.all()
    total_purchase = sum(p.total_amount for p in purchases)
    total_sale = sum(s.total_amount for s in sales)
    profit = total_sale - total_purchase
    return render(request, 'bill_summary.html', {
        'purchases': purchases,
        'sales': sales,
        'total_purchase': total_purchase,
        'total_sale': total_sale,
        'profit': profit
    })

# Update Views with access control
class SellerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Seller
    fields = ['name', 'contact', 'email']
    template_name = 'update_seller.html'
    success_url = reverse_lazy('stock_list')
    def test_func(self):
        return is_owner(self.request.user)

class GoodsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Goods
    fields = ['name', 'description']
    template_name = 'update_goods.html'
    success_url = reverse_lazy('stock_list')
    def test_func(self):
        return is_owner(self.request.user)

class BuyerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Buyer
    fields = ['name', 'contact', 'email']
    template_name = 'update_buyer.html'
    success_url = reverse_lazy('stock_list')
    def test_func(self):
        return is_owner(self.request.user)

# Create Views with access control
class SellerCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Seller
    fields = ['name', 'contact', 'email']
    template_name = 'add_seller.html'
    success_url = reverse_lazy('stock_list')
    def test_func(self):
        return is_owner(self.request.user)

class GoodsCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Goods
    fields = ['name', 'description']
    template_name = 'add_goods.html'
    success_url = reverse_lazy('stock_list')
    def test_func(self):
        return is_owner(self.request.user)

class BuyerCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Buyer
    fields = ['name', 'contact', 'email']
    template_name = 'add_buyer.html'
    success_url = reverse_lazy('stock_list')
    def test_func(self):
        return is_owner_or_employee(self.request.user)

# Login/Logout Views
class CustomLoginView(LoginView):
    template_name = 'login.html'
    # Removed redirect_authenticated_user
    def get_success_url(self):
        if is_owner(self.request.user):
            return reverse_lazy('stock_list')
        elif is_employee(self.request.user):
            return reverse_lazy('add_sale')
        return reverse_lazy('index') 
class CustomLogoutView(View):
    def get(self, request):
        logout(request)  # Log the user out
        return redirect('index')
