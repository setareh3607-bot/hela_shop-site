from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='عنوان دسته بندی')
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True, blank=True, verbose_name='شناسه آدرس')
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='children',
        verbose_name='دسته بندی والد'
    )
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین به روزرسانی')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        ordering = ('title',)
        
    def __str__(self):
        return self.title
    
    def __repr__(self):
        return f"<Category: id={self.pk}, slug='{self.slug}'>"


class Customer(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='نام')
    last_name = models.CharField(max_length=50, verbose_name='نام خانوادگی')
    phone = models.CharField(max_length=13, unique=True, verbose_name='شماره موبایل')
    email = models.EmailField(max_length=100, unique=True, verbose_name='ایمیل')
    address = models.TextField(default="", blank=True, verbose_name='آدرس')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین به روزرسانی')

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربرها'
        ordering = ('first_name', 'last_name',)
        indexes = (
            models.Index(fields=['first_name']),
            models.Index(fields=['last_name']),
        )
        
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def __repr__(self):
        return f"<Customer: id={self.pk}, phone='{self.phone}'>"
    
    
class Brand(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='نام برند')
    slug = models.SlugField(max_length=150, unique=True, allow_unicode=True, blank=True, verbose_name='شناسه آدرس')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین به روزرسانی')
    
    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برندها'
        ordering = ('name',)
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"<Brand: id={self.pk}, slug='{self.slug}'>"
    
    
class Product(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='نام محصول'
    )
    brief_explanation = models.CharField(
        max_length=250,
        default="",
        blank=True,
        verbose_name='توضیح مختصر'
    )
    description = models.TextField(
        default="",
        blank=True,
        verbose_name='توضیحات'
    )
    price = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='قیمت'
    )
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name='موجودی'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='products',
        blank=True,
        null=True,
        verbose_name='دسته بندی'
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        related_name='products',
        blank=True,
        null=True,
        verbose_name='برند'
    )
    image = models.ImageField(
        upload_to='product/',
        blank=True,
        null=True,
        verbose_name='تصویر محصول'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاریخ آخرین به روزرسانی'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='آیا کالا برای فروش فعال است'
    )
    discount_price = models.PositiveIntegerField(
        default=0,
        verbose_name='مبلغ تخفیف'
    )
    rating = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[MaxValueValidator(5)],
        verbose_name='امتیاز محصول از ۰ تا ۵'
    )
    
    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ('name',)
        indexes = (models.Index(fields=['name']),)
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"<Product: id={self.pk}, name='{self.name}'>"
    
    
class Coupon(models.Model):
    PERCENTAGE = 'percentage'
    FIXED = 'fixed'
    DISCOUNT_TYPE_CHOICES = (
        (PERCENTAGE, 'درصدی'),
        (FIXED, 'مبلغ ثابت'),
    )
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='کد'
    )
    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='مقدار تخفیف'
    )
    discount_type = models.CharField(
        max_length=20,
        choices=DISCOUNT_TYPE_CHOICES,
        default=PERCENTAGE,
        verbose_name='نوع تخفیف'
    )
    min_purchase_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='حداقل مبلغ خرید'
    )
    max_uses = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='حداکثر تعداد استفاده'
    )
    used_count = models.PositiveIntegerField(
        default=0,
        verbose_name='تعداد استفاده شده'
    )
    valid_from = models.DateTimeField(verbose_name='تاریخ شروع اعتبار')
    valid_until = models.DateTimeField(verbose_name='تاریخ پایان اعتبار')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'کوپن'
        verbose_name_plural = 'کوپن ها'
        ordering = ('-created_at',)
        indexes = (models.Index(fields=['valid_until']),)
        
    def __str__(self):
        return self.code
    
    def __repr__(self):
        return f"<Coupon: code={self.code}, type={self.discount_type}>"
        
        
class Cart(models.Model):
    customer = models.ForeignKey(
        'Customer',
        on_delete=models.SET_NULL,
        related_name='carts',
        null=True,
        blank=True,
        verbose_name='مشتری'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به روز رسانی')
    is_paid = models.BooleanField(default=False, verbose_name='پرداخت شده')
    paid_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='تاریخ پرداخت'
    )
    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.SET_NULL,
        related_name='carts',
        null=True,
        blank=True,
        verbose_name='کوپن'
    )
    
    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد خرید ها'
        ordering = ('customer', '-created_at',)
    
    def __str__(self):
        return f'سبد خرید مشتری: {self.customer or "مهمان"}'
    
    def __repr__(self):
        return f'<Cart: id={self.id}, customer_id={self.customer_id}, is_paid={self.is_paid}>'


class CartItem(models.Model):
    cart = models.ForeignKey(
        'Cart',
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='سبد خریداری',
    )
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name='محصول'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name='تعداد'
    )
    unit_price = models.PositiveIntegerField(
        verbose_name='قیمت واحد'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )
    
    class Meta:
        verbose_name = 'آیتم سبد خرید'
        verbose_name_plural = 'آیتم های سبد خرید'
        ordering = ('-created_at',)
        unique_together = (('cart', 'product'),)
        
    @property
    def total_price(self):
        return self.quantity * self.unit_price
    
    def __str__(self):
        return f'{self.quantity} * {self.product}'
    
    def __repr__(self):
        return (
            f'<CartItem: id={self.id}, '
            f'cart_id={self.cart_id}, '
            f'product_id={self.product_id}, '
            f'qty={self.quantity}>'
        )


class Order(models.Model):
    PENDING = 'pending'
    PROCESSING = 'processing'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'
    STATUS_CHOICES = (
        (PENDING, 'در انتظار'),
        (PROCESSING, 'در حال پردازش'),
        (SHIPPED, 'ارسال شده'),
        (DELIVERED, 'تحویل داده شد'),
        (CANCELLED, 'لغو شده')
    )
    customer = models.ForeignKey(
        "Customer",
        related_name='orders',
        verbose_name="مشتری",
        on_delete=models.PROTECT
    )
    address = models.TextField(
        verbose_name="آدرس تحویل",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=20,
        default=PENDING,
        verbose_name='وضعیت'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاریخ آخرین به روزرسانی'
    )
    
    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش ها"
        ordering = ('-created_at',)
        indexes = (models.Index(fields=['created_at']),)
        
    def __str__(self):
        return f'سفارش {self.pk} - {self.customer}'
    
    def __repr__(self):
        return f"<Order: id={self.pk}, customer_id={self.customer_id}, status='{self.status}'>"

    
class OrderItem(models.Model):
    order = models.ForeignKey(
        "Order",
        related_name='items',
        verbose_name="سفارش",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        "Product",
        related_name='order_items',
        verbose_name="محصول",
        on_delete=models.PROTECT,
    )
    price = models.PositiveIntegerField(
        verbose_name='قیمت'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name='تعداد'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )
    
    class Meta:
        verbose_name = 'آیتم سفارش'
        verbose_name_plural = 'آیتم های سفارش'
        ordering = ('-created_at',)
        
    @property
    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f'{self.quantity} * {self.product}'

    def __repr__(self):
        return (
            f'<OrderItem: id={self.pk}, '
            f'order_id={self.order_id}, '
            f'product_id={self.product_id}>'
        )


class User(AbstractUser):
    phone = models.CharField(
        max_length=13,
        unique=True,
        verbose_name='تلفن'
    )
    