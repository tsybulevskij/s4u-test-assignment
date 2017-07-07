from django.db.models import Q
from rest_framework import generics

import account.serrializers
import transaction.serializers
from account.models import Account
from transaction.models import Transaction


class AccountAPIView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = account.serrializers.AccountSerializer

    def create(self, request, *args, **kwargs):
        response = super(AccountAPIView, self).create(request, *args, **kwargs)
        response.data['error'] = False
        return response


class AccountTransactions(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = transaction.serializers.TransactionSerializer

    def get_queryset(self):
        queryset = super(AccountTransactions, self).get_queryset()
        account_id = self.kwargs['id']
        return queryset.filter(Q(source_account_id=account_id) |
                               Q(dest_account_id=account_id))
