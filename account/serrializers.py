from rest_framework import serializers

from account.models import Account


class AccountSerializer(serializers.ModelSerializer):
    accountNumber = serializers.ReadOnlyField(source='number')

    class Meta:
        model = Account
        fields = ('id', 'accountNumber', 'currency', 'balance')
        read_only_fields = ('id', 'accountNumber', 'balance')
