from datetime import datetime
from graphene import relay
from graphene_django import DjangoObjectType
import graphene
from core import models
from . import filters


class PersonAddressNode(DjangoObjectType):
    class Meta:
        model = models.PersonAddress
        interfaces = (relay.Node,)


class PersonObjectType(DjangoObjectType):
    name = graphene.String()

    def resolve_name(self, info):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        model = models.Person
        filterset_class = filters.PersonFilter
        exclude = ('password', 'first_name', 'last_name')


class CreditCardObjectType(DjangoObjectType):
    class Meta:
        model = models.CreditCard
        filterset_class = filters.CreditCardFilter


class InvoiceEntryObjectType(DjangoObjectType):
    class Meta:
        model = models.InvoiceEntry


class InvoiceObjectType(DjangoObjectType):
    invoice_entries = graphene.List(of_type=InvoiceEntryObjectType)
    closed = graphene.Boolean()

    def resolve_closed(self, info):
        current_date = datetime.now()
        return current_date.date() >= self.closing_date

    def resolve_invoice_entries(self, info):
        return self.entries.all()

    class Meta:
        model = models.Invoice
        filterset_class = filters.InvoiceFilter


class PurchaseObjectType(DjangoObjectType):
    class Meta:
        model = models.Purchase
        filterset_class = filters.PurchaseFilter
