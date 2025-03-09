from django.db import models

# Create your models here.
class Seller(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class Buyer(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class Goods(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name
    

class Purchase(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        self.total_amount = self.quantity * self.purchase_price
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.goods.name} - {self.quantity} - {self.total_amount}'
    
class Sale(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)  
    quantity = models.PositiveIntegerField()
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        self.total_amount = self.quantity * self.sale_price
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.goods.name} - {self.quantity} - {self.total_amount}'
    
    
class Stock(models.Model):
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    def __str__(self):
        return f'{self.goods.name} - {self.quantity}'
    