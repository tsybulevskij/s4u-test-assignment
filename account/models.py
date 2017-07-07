import random

from django.conf import settings
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

# Create your models here.
from account.config import CURRENCIES


def get_number():
    number = random.randint(10000000, 99999999)
    while Account.objects.filter(number=number).exists():
        number = random.randint(10000000, 99999999)
    return number


class Account(models.Model):
    number = models.CharField(
        max_length=settings.ACCOUNT_NUMBER_LENGTH,
        default=get_number,
        blank=True,
        unique=True,
        validators=[MinLengthValidator(settings.ACCOUNT_NUMBER_LENGTH)]
    )
    currency = models.CharField(max_length=3, choices=CURRENCIES)
    balance = models.FloatField(default=0, blank=True,
                                validators=[MinValueValidator(0)])

    def __str__(self):
        return '{} {} {}'.format(self.number, self.currency, self.balance)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Account, self).save(*args, **kwargs)

    def is_enough_balance(self, amount):
        return self.balance >= amount if amount else True

    def withdraw(self, amount):
        self.balance -= amount
        self.save()

    def deposit(self, amount):
        self.balance += amount
        self.save()
