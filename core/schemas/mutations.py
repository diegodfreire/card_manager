from graphene_django.rest_framework.mutation import SerializerMutation
from core import serializers


class PersonMutation(SerializerMutation):
    class Meta:
        serializer_class = serializers.PersonSerializer
        lookup_field = "id"



class CreditCardMutation(SerializerMutation):
    class Meta:
        serializer_class = serializers.CreditCardSerializer
        lookup_field = "id"



class PurchaseMutation(SerializerMutation):
    class Meta:
        serializer_class = serializers.PurchaseSerializer
        model_operations = ['create']


