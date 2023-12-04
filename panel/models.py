from django.db import models
from django.forms import ValidationError
# from cart.shop_views import payment
from django.template.defaultfilters import slugify
from my_auth.countries import *
from flexyweb import settings
import datetime
import datetime
from django.utils import timezone
from django.urls import reverse
from pay.models import Payment
from PIL import Image
from django.contrib import messages


def order_num_gen():
    # last = Order.objects.latest("id")
    id = None
    # if last == None:
    #     id = 1
    # else:
        # id = last.id + 1
    id = "ADHGD"
    yr = int(datetime.date.today().strftime("%Y"))
    dt = int(datetime.date.today().strftime("%d"))
    mt = int(datetime.date.today().strftime("%m"))
    d = datetime.date(yr,mt,dt)
    current_date = d.strftime("%Y%m%d")

    order_nun = str(current_date) + str(id)
    return order_nun
    
# from datetime import timezone
payment_method = [
    # ("PayPal","PayPal"),
    ("PayFast","PayFast"),
    # ("PayPal","PayPal"),
    # ("Ozow","Ozow"),
    # ("Yoco","Yoco"),
]

STATUS = (

        ('New','New'),
        ('Started','Started'),
        ('Accepted','Accepted'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),
        ('Returned','Returned'),


    )
D_STATUS = (

        
        ('Delivered','Delivered'),
        ('Scheduled','Scheduled'),
        ('Cancelled','Cancelled'),
        ('Rescheduled','Rescheduled'),


    )
PREFFERED_METHOD = (
        ('Face To Face','Face To Face'),
        ('Online','Online'),
        ('Hybrid','Hybrid'),
    )
p_cs = [
    ("Free","Free"),
    ("Business","Business"),
    ("Beginner","Beginer"),
    ("Premium","Premium"),
]

STATUS_CHOICES = (
 ('draft', 'Draft'),
 ('published', 'Published'),
 )
# class PublishedManager(models.Manager):
#     def get_queryset(self):
#         return super(PublishedManager, self).get_queryset().filter(status='published')

#     def all(self):
#         return super(PublishedManager, self).get_queryset()

#     def include(self):
#         return super(PublishedManager, self).get_queryset().all()

# Create your models here.
class Order(models.Model):
    """Model definition for Order."""
    user                    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    payment                 = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    email                   = models.EmailField(max_length=200, blank=False)
    first_name              = models.CharField(max_length=200, blank=False)
    last_name               = models.CharField(max_length=200, blank=False)
    country                 = models.CharField(max_length=600,  default='South Africa')
    # country                 = models.CharField(max_length=400, choices=countries, default='ZA')
    type_of_class           = models.CharField(max_length=300, blank=True, null=True)
    phone                   = models.CharField(max_length=50, default="")
    order_total             = models.DecimalField(max_digits=10, decimal_places=2, default=3)
    order_total_other       = models.DecimalField(max_digits=10, decimal_places=2, default=3)
    device_name             = models.CharField(max_length=700, null=True, blank=True)
    currency                = models.CharField(max_length=40, default="ZAR")
    ip_adress               = models.CharField(max_length=40, default="0.0.0.1")
    payment_method          = models.CharField(max_length=300, choices=payment_method, default=1)
    learning_method         = models.CharField(max_length=300, choices=PREFFERED_METHOD, default=1)
    city                    = models.CharField(max_length=200, blank=True, null=True)
    street_name             = models.CharField(max_length=400, blank=True, null=True)
    zip_code                = models.CharField(max_length=200, blank=True, null=True)
    status                  = models.CharField(max_length=100, choices=STATUS, default="Started")
    delivery_status         = models.CharField(max_length=100, choices=D_STATUS, default="Scheduled")
    order_number            = models.CharField(max_length=300, blank=False, unique=False, default=order_num_gen)
    date_ordered			= models.DateTimeField(verbose_name='date orderd', auto_now_add=True)
    last_viewed	            = models.DateTimeField(verbose_name='last viewed', auto_now=True)
    is_ordered              = models.BooleanField(default=False)
    # TODO: Define fields here

    class Meta:
        """Meta definition for Order."""

        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        """Unicode representation of Order."""
        return self.first_name + " " + self.last_name
    
    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)
    
    def get_order_total(self):
        total = 0
        for p in self.order_items.all():
            total += p.get_sub_total
        return total
        

class Course(models.Model):
    """Model definition for Course."""
    name = models.CharField(max_length=200, blank=False, help_text='Enter your course title')
    motivation = models.CharField(max_length=500, blank=True, null=True, help_text='Motivation e.g Increase your skills in this course')
    trainer = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey("Category", blank=True, null=True, on_delete=models.SET_NULL, help_text='Choose the category for your course.')
    describe = models.CharField(max_length=800, blank=True, null=True, help_text='Describe this course in 200 words')
    similar_courses = models.ManyToManyField("self", blank=True, help_text='Enter all your courses to recommend')
    students_completed = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name="joined", blank=True)
    students_enrolled = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name="enrolled", blank=True)
    student_likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="likes",blank=True)
    price = models.DecimalField(max_digits=10, default=10, decimal_places=2)
    image = models.ImageField(default='default.jpg', upload_to='course/thumbnails', help_text='Make it a little bit bigger for cropping')
    slug = models.SlugField(max_length=250, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES, default='draft')
    
    # published = PublishedManager()


    # TODO: Define fields here
    def likes(self):
        return self.student_likes.count()

    def joins(self):
        return self.students_enrolled.count()
    
    @property
    def first_module(self):
        if self.modules.all():
            return self.modules.all()[0]
        return
    @property
    def enrollments(self):
        return self.students_enrolled.all()


    class Meta:
        """Meta definition for Course."""

        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ['-publish']
        indexes = [
                models.Index(fields=['-publish']),
            ]

    def get_absolute_url(self):
        return reverse('course', args=[self.publish.year,
            self.publish.month,
            self.publish.day,
            self.slug, self.pk])


    def __str__(self):
        """Unicode representation of Course."""
        return self.name
    
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name+"-"+str(self.publish))
        super().save()
        img = Image.open(self.image.path)
        w, h = img.size
       
        if w < 800 or h < 533:
            del img
            self.image = "default.jpg"
            # message = "Infomartion was submitted successfully"
            # messages.add_message(request, messages.INFO, message)
        else:
            img.thumbnail((800, 533))
            img.save(f"{self.image.path}")
        return super().save(*args, **kwargs)

    

# Create your models here.
class Product(models.Model):
    """Model definition for Product."""

    # TODO: Define fields here
    course = models.ForeignKey("Course", related_name='products', on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey('self', related_name='products', on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=250, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    hours = models.IntegerField( choices=[(i,i) for i in range(160)])
    per = models.CharField(max_length=250, default="hour")
    product_type = models.CharField(max_length=300, choices=p_cs)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES, default='draft')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_advanced = models.BooleanField(default=False)
    # published = PublishedManager()
    
    def __str__(self) -> str:
        return self.name

class ProductFeature(models.Model):
    """Model definition for Product."""

    # TODO: Define fields here
    product = models.ForeignKey(Product, related_name="main_features", on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=250, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.ManyToManyField(Product, related_name="features", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Feature'
        verbose_name_plural = 'Features'


class Category(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE, default=1)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=1, blank=True, null=True)
    course = models.ForeignKey(Course, related_name='order_items',blank=True, null=True,  on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    # variations = models.ManyToManyField(Variations, blank=True)
    quantity = models.IntegerField()
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(f"{self.product.name}")

    class Meta:
        db_table = 'order_product'
        managed = True
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
    

    @property
    def get_sub_total(self):
        if self.product:
            return (self.product.price) *  (self.quantity )
        return (self.course.price) *  1

    @property
    def get_hours(self):
        return (self.product.hours) if not None else 0