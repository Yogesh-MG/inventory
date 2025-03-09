# forms.py
from django import forms
from .models import Purchase, Sale, Stock

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['seller', 'goods', 'quantity', 'purchase_price']

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['buyer', 'goods', 'quantity', 'sale_price']

    def clean(self):
        cleaned_data = super().clean()
        goods = cleaned_data.get('goods')
        quantity = cleaned_data.get('quantity')
        if goods and quantity:
            try:
                stock = Stock.objects.get(goods=goods)
                if stock.quantity < quantity:
                    raise forms.ValidationError(
                        f"Not enough stock for {goods}. Available: {stock.quantity}, Requested: {quantity}"
                    )
            except Stock.DoesNotExist:
                raise forms.ValidationError(f"No stock record exists for {goods}.")
        return cleaned_data
