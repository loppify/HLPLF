import django_filters
from django import forms
from .models import Transaction, Category

class TransactionFilter(django_filters.FilterSet):
    description = django_filters.CharFilter(
        lookup_expr='icontains', 
        label="Пошук (опис)"
    )
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(), 
        label="Категорія"
    )
    transaction_type = django_filters.ChoiceFilter(
        choices=Transaction.TYPE_CHOICES, 
        label="Тип"
    )
    
    order_by = django_filters.OrderingFilter(
        fields=(
            ('amount', 'amount'),
            ('created_at', 'created_at'),
        ),
        field_labels={
            'amount': 'Сума',
            'created_at': 'Дата',
        },
        label="Сортування"
    )

    class Meta:
        model = Transaction
        fields = ['description', 'category', 'transaction_type']

    def __init__(self, *args, **kwargs):
        super(TransactionFilter, self).__init__(*args, **kwargs)
        self.form.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Пошук...'})
        self.form.fields['category'].widget.attrs.update({'class': 'form-select'})
        self.form.fields['transaction_type'].widget.attrs.update({'class': 'form-select'})
        self.form.fields['order_by'].widget.attrs.update({'class': 'form-select'})
