from django.views.generic import ListView
from django.db.models import Sum
from .models import Transaction
from .filters import TransactionFilter

class TransactionListView(ListView):
    model = Transaction
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = TransactionFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        
        # Глобальне бюджетування
        all_transactions = Transaction.objects.all()
        global_income = all_transactions.filter(transaction_type='debit').aggregate(Sum('amount'))['amount__sum'] or 0
        global_expense = all_transactions.filter(transaction_type='credit').aggregate(Sum('amount'))['amount__sum'] or 0
        context['global_income'] = global_income
        context['global_expense'] = global_expense
        context['global_balance'] = global_income - global_expense
        
        return context
