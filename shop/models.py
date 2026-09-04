from django.db import models

# Create your models here.
class category(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='عنوان دسته یندی')
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True, blank=True, verbose_name='شناسه آدرس')
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name='children', verbose_name='دسته بندی والد') 
    
    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        
    def __str__(self):
        return self.title