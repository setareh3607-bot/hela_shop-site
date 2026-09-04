from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='عنوان دسته یندی')
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True, blank=True, verbose_name='شناسه آدرس')
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name='children', verbose_name='دسته بندی والد') 
    
    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        
    def __str__(self):
        return self.title

class Customer(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='نام')
    last_name = models.CharField(max_length=50, verbose_name='نام خانوادگی')
    phone = models.CharField(max_length=13, unique=True, verbose_name='شماره موبایل')
    email = models.EmailField(max_length=100, unique=True, verbose_name='ایمیل')
    address = models.TextField(blank=True, null=True, verbose_name='آدرس')
    
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربرها'
        
    def __str__(self):
        return f'{self.first_name} {self.last_name}'