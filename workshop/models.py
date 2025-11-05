from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Customer(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    messenger = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'customers'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['phone']),
            models.Index(fields=['email']),
            models.Index(fields=['messenger']),
        ]

    def __str__(self):
        return self.name or "Без имени"


class Category(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        db_table = 'categories'
        indexes = [
            models.Index(fields=['title']),
        ]

    def __str__(self):
        return self.title


class Job(models.Model):
    TYPE_CHOICES = [
        ('FIX', 'Фикс'),
        ('VAR', 'Переменный'),
        ('LAB', 'Работа'),
        ('MAT', 'Материал'),
    ]

    type = models.CharField(max_length=4, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)
    price = models.IntegerField()

    class Meta:
        db_table = 'jobs'

    def __str__(self):
        return self.title


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True, blank=True)
    jobs = models.ManyToManyField("Job", blank=True, related_name="products")

    def __str__(self):
        return self.name



class Lead(models.Model):

    STATUS_CHOICES = [
        ('NEW', 'Новый'),
        ('STATUS', 'Статус'),
        ('CALLBACK', 'Дозвонись'),
        ('CLIENT', 'Клиент'),
        ('ASSIGN_MASTER', 'Оформить мастера'),
        ('ROP_ANALYSIS', 'РОП анализ'),
        ('NON_TARGET_ROP', 'Нецелевой РОП'),
        ('ROP_REFUSAL', 'Отказ РОП'),
        ('PICKUP', 'Забрать забор'),
        ('CLOSE_OR_FOLLOWUP', 'Дожми или доведи'),
        ('LOGISTICS_REFUSAL', 'Отказ логистики'),
    ]
    code = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=17, choices=STATUS_CHOICES)
    address = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']


class Part(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    value = models.PositiveIntegerField(blank=True, null=True, default=1)

    class Meta:
        db_table = 'parts'
        unique_together = ('lead', 'job')

    def __str__(self):
        return f"{self.lead} — {self.job} × {self.value}"
