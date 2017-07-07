from rest_framework import generics

from transaction.models import Transaction
from transaction.serializers import TransactionSerializer


class TransactionAPIView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        response = super(TransactionAPIView, self).create(request, *args, **kwargs)
        response.data['error'] = False
        return response
