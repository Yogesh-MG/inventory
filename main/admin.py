from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Purchase, Sale, Stock, Seller, Buyer, Goods
from django.http import HttpResponse
import csv
# Register your models here.


def export_to_csv(modeladmin, request, queryset):
    """
    Custom admin action to export selected records to a CSV file.
    """
    # Get model fields dynamically
    field_names = [field.name for field in modeladmin.model._meta.fields]
    # Create the HTTP response for the CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={modeladmin.model._meta.model_name}_export.csv'
    # Write the CSV
    writer = csv.writer(response)
    writer.writerow(field_names)  # Write header row
    for obj in queryset:
        row = [getattr(obj, field) for field in field_names]
        writer.writerow(row)
    return response
export_to_csv.short_description = "Export selected items to CSV"

class customPurchaseAdmin(admin.ModelAdmin):
    actions = [export_to_csv]
    list_display = ('seller', 'goods', 'quantity', 'purchase_price', 'date')

admin.site.register(Purchase, customPurchaseAdmin)
admin.site.register(Sale)
admin.site.register(Stock)
admin.site.register(Seller)
admin.site.register(Buyer)
admin.site.register(Goods)