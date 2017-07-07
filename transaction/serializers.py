from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from account.models import Account
from transaction.exchange import Exchange
from transaction.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):

    transactionId = serializers.ReadOnlyField(source='pk')
    amount = serializers.FloatField(write_only=True)
    destAmount = serializers.FloatField(source='dest_amount', read_only=True)
    sourceAmount = serializers.FloatField(source='source_amount', read_only=True)
    exchangeRate = serializers.FloatField(source='exchange_rate', required=False)
    destAccount = serializers.SlugRelatedField(
        queryset=Account.objects.all(),
        slug_field='number',
        source='dest_account',
        read_only=False,
        required=False,
        allow_null=True
    )
    sourceAccount = serializers.SlugRelatedField(
        queryset=Account.objects.all(),
        slug_field='number',
        source='source_account',
        read_only=False,
        required=False,
        allow_null=True
    )

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Amount should be more then 0.')
        return value

    def validate(self, attrs):
        attrs = super(TransactionSerializer, self).validate(attrs)

        if not self._get_transaction_type(attrs):
            raise ValidationError({'non_field_error': 'Source account or Destination account must be filled.'})

        if attrs.get('source_account') == attrs.get('dest_account'):
            raise ValidationError({'non_field_error': 'Source account and Destination account should be different.'})

        set_amount_metods = {
            'transfer': self._set_transfer_amount,
            'deposit': self._set_deposit_amout,
            'withdraw': self._set_withdraw_amount,
        }
        set_amount_metods.get(self._get_transaction_type(attrs))(attrs)

        if attrs.get('source_account') and not attrs.get('source_account').is_enough_balance(attrs.get('source_amount')):
            raise ValidationError({'non_field_error': 'Not enough balance.'})

        return attrs

    def _get_transaction_type(self, attrs):
        if attrs.get('source_account') and attrs.get('dest_account'):
            return 'transfer'
        elif attrs.get('dest_account'):
            return 'deposit'
        elif attrs.get('source_account'):
            return 'withdraw'

    def _set_withdraw_amount(self, attrs):
        attrs['source_amount'] = attrs.pop('amount')

    def _set_deposit_amout(self, attrs):
        attrs['dest_amount'] = attrs.pop('amount')

    def _set_transfer_amount(self, attrs):
        rate = self.get_rate(attrs)
        attrs['source_amount'] = attrs.pop('amount')
        attrs['exchange_rate'] = rate
        attrs['dest_amount'] = self.convert(attrs.get('source_amount'), rate)

    def _get_rate(self, attrs):
        return Exchange.get_rate(attrs['source_account'].currency,
                                 attrs['dest_account'].currency)

    def _convert(self, amount, rate):
        return round(rate * amount, 2)

    class Meta:
        model = Transaction
        fields = (
            'sourceAccount',
            'destAccount',
            'amount',
            'sourceAmount',
            'destAmount',
            'exchangeRate',
            'transactionId'
        )
