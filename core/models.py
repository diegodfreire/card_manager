import uuid
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.db.models.deletion import CASCADE


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class PersonAddress(BaseModel):
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    number = models.CharField(max_length=10)


class Person(AbstractUser, BaseModel):
    address = models.OneToOneField(
        PersonAddress,
        on_delete=models.CASCADE,
        related_name="person",
        null=True,
        blank=True
    )


class CreditCard(BaseModel):
    name = models.CharField(max_length=255)
    limit = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    due_day = models.PositiveIntegerField()
    closing_day = models.PositiveIntegerField()
    person = models.ForeignKey(
        Person,
        on_delete=CASCADE,
        related_name='credit_cards'
    )


class Invoice(BaseModel):
    due_date = models.DateField()
    closing_date = models.DateField()
    total_value = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    credit_card = models.ForeignKey(
        CreditCard,
        on_delete=models.CASCADE,
        related_name='invoices'
    )


class Purchase(BaseModel):
    value = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=datetime.now)
    installments = models.PositiveIntegerField(default=1)
    credit_card = models.ForeignKey(
        CreditCard,
        on_delete=CASCADE,
        related_name='purchases'
    )


class InvoiceEntry(BaseModel):
    value = models.DecimalField(max_digits=10, decimal_places=2)
    installment_number = models.PositiveIntegerField()
    purchase = models.ForeignKey(
        Purchase,
        on_delete=CASCADE,
        related_name='invoice_entries'
    )
    invoice = models.ForeignKey(
        Invoice,
        on_delete=CASCADE,
        related_name='entries'
    )
