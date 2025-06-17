from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('men', 'Men'),
        ('women', 'Women'),
        ('electronics', 'Electronics'),
        ('computers', 'Computers'),
        ('houses', 'Houses'),
        ('automotives','Automotives')
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = CloudinaryField('image', folder='products', blank=True)  # Use CloudinaryField
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})
    
    def get_like_count(self):
        return self.likes.count()
    
    class Meta:
        ordering = ['-created_at']

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'product')

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Comment by {self.user} on {self.product}'