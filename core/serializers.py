from datetime import datetime, date, timedelta
from django.db.models import fields
from rest_framework import serializers
from django.db import transaction
from core import models


class PersonAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PersonAddress
        fields = ("country", "state", "city", "district", "street", "number")


class PersonSerializer(serializers.ModelSerializer):
    address = PersonAddressSerializer(many=False)

    class Meta:
        model = models.Person
        fields = ('id', 'username', 'first_name',
                  'last_name', 'email', 'address')

    @transaction.atomic
    def persist(self, validated_data: dict, instance: models.Person = None):
        address = validated_data.pop("address", None)
        if instance:
            models.Person.objects.filter(
                pk=instance.id).update(**validated_data)
            instance = models.Person.objects.get(pk=instance.id)
        else:
            instance = models.Person.objects.create_user(**validated_data)
        if address:
            data_address = PersonAddressSerializer(address).data
            address, _ = models.PersonAddress.objects.update_or_create(
                person=instance, defaults=data_address)
            instance.address = address
        instance.save()
        return instance

    def create(self, validated_data):
        return self.persist(validated_data)

    def update(self, instance, validated_data):
        return self.persist(instance=instance, validated_data=validated_data)


class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CreditCard
        fields = "__all__"


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Purchase
        fields = ('value', 'installments', 'credit_card', 'date')

    def save(self, **kwargs):
        instance: models.Purchase = super().save(**kwargs)
        credit_card: models.CreditCard = instance.credit_card
        now = datetime.now()
        year = now.year
        installment_value = instance.value / instance.installments
        for num_installment in range(instance.installments):
            next_month = now.month + num_installment
            year = year+1 if next_month > 12 else year
            month = (now.month + num_installment) % 12 or 12
            closing_date = date(
                year=year,
                month=month,
                day=credit_card.closing_day
            )
            invoice, _ = models.Invoice.objects.get_or_create(
                credit_card=credit_card,
                closing_date=closing_date,
                defaults={
                    "due_date": date(
                        year=year,
                        month=month,
                        day=credit_card.due_day
                    )
                }
            )
            invoice.total_value += installment_value
            invoice.save()
            models.InvoiceEntry.objects.create(**{
                "value": installment_value,
                "installment_number": (num_installment+1),
                "purchase": instance,
                "invoice": invoice
            })
        return instance
