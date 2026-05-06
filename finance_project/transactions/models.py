from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Назва категорії")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

class Transaction(models.Model):
    TYPE_CHOICES = (
        ('debit', 'Дебет (Надходження)'),
        ('credit', 'Кредит (Витрати)'),
    )
    
    description = models.CharField(max_length=255, verbose_name="Опис")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Сума")
    transaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name="Тип")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='transactions', verbose_name="Категорія")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    def __str__(self):
        return f"{self.description} - {self.amount} ({self.get_transaction_type_display()})"

    class Meta:
        verbose_name = "Транзакція"
        verbose_name_plural = "Транзакції"
        ordering = ['-created_at']
