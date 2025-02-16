from django.db import models

class Product(models.Model):
    image = models.ImageField(upload_to='store/images/')
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.CharField(max_length=50)
    free_delivery = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

    from django.db import models

class WomenProduct(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()

    class Meta:
        db_table = 'women_products'  # Match table name in MySQL

class MenProduct(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()

    class Meta:
        db_table = 'men_products'

class NewProduct(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()

    class Meta:
        db_table = 'new_products'

class KidsProduct(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()

    class Meta:
        db_table = 'kids_products'

class UtensilsProduct(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()

    class Meta:
        db_table = 'utensils_products'
