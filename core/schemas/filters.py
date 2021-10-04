from django.db.models.query_utils import Q
import django_filters
from django.db.models.query import QuerySet
from core import models


class PersonFilter(django_filters.FilterSet):

    class Meta:
        model = models.Person
        fields = {
            "id": ["exact"],
            "first_name": ["exact", "icontains"]
        }


class CreditCardFilter(django_filters.FilterSet):
    class Meta:
        model = models.CreditCard
        fields = {
            "id": ["exact"],
            "person__id": ["exact"]
        }


class InvoiceFilter(django_filters.FilterSet):
    class Meta:
        model = models.Invoice
        fields = {
            "id": ["exact"],
            "credit_card__id": ["exact"]
        }


class PurchaseFilter(django_filters.FilterSet):
    class Meta:
        model = models.Invoice
        fields = {
            "id": ["exact"],
            "credit_card__id": ["exact"]
        }
