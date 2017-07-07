from django.core.validators import MinValueValidator
from django.db import models, transaction

# Create your models here.
from account.models import Account


class Transaction(models.Model):
    transaction_dt = models.DateTimeField(auto_now_add=True)

    source_account = models.ForeignKey(Account, null=True, blank=True,
                                       related_name='withdrawal_transactions')
    dest_account = models.ForeignKey(Account, null=True, blank=True,
                                     related_name='deposit_transaction')
    source_amount = models.FloatField(null=True, blank=True,
                                      validators=[MinValueValidator(0)])
    dest_amount = models.FloatField(null=True, blank=True,
                                    validators=[MinValueValidator(0)])

    exchange_rate = models.FloatField(null=True, blank=True,
                                      validators=[MinValueValidator(0)])

    def __str__(self):
        return '{} -> {} {}'.format(self.source_account, self.dest_account,
                                    self.source_amount or self.dest_amount)

    def save(self, *args, **kwargs):
        self.full_clean()

        if self.pk is None:
            action = self._get_action()
            with transaction.atomic():
                action()
                super(Transaction, self).save(*args, **kwargs)

    @property
    def transaction_type(self):
        if self.source_account and self.dest_account:
            return 'transfer'
        elif self.dest_account:
            return 'deposit'
        elif self.source_account:
            return 'withdraw'

    def _get_action(self):
        return {
            'transfer': self._transfer,
            'deposit': self._deposit,
            'withdraw': self._withdraw,
        }[self.transaction_type]

    def _transfer(self):
        self.source_account.withdraw(self.source_amount)
        self.dest_account.deposit(self.dest_amount)

    def _deposit(self):
        self.dest_account.deposit(self.dest_amount)

    def _withdraw(self):
        self.source_account.withdraw(self.source_amount)