# inventory/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Purchase, Sale, Stock

@receiver(post_save, sender=Purchase)
def update_stock_on_purchase(sender, instance, created, **kwargs):
    if created:  # Only run on creation, not updates
        stock, _ = Stock.objects.get_or_create(goods=instance.goods, defaults={'quantity': 0})
        stock.quantity += instance.quantity
        stock.save()

@receiver(post_save, sender=Sale)
def update_stock_on_sale(sender, instance, created, **kwargs):
    if created:  # Only run on creation, not updates
        stock = Stock.objects.get(goods=instance.goods)
        if stock.quantity >= instance.quantity:
            stock.quantity -= instance.quantity
            stock.save()
        else:
            # Optionally, raise an error or handle insufficient stock
            raise ValueError(f"Not enough stock for {instance.goods}. Available: {stock.quantity}, Requested: {instance.quantity}")