from graphene import ObjectType
import graphene
from graphene_federation import build_schema
from graphene_django_pagination import DjangoPaginationConnectionField
from core.schemas import queries, mutations, resolvers


class Query(ObjectType):
    """Definição da Query usada no Schema."""
    list_person = DjangoPaginationConnectionField(queries.PersonObjectType)
    list_credit_card = DjangoPaginationConnectionField(queries.CreditCardObjectType)
    list_invoice = DjangoPaginationConnectionField(queries.InvoiceObjectType)
    list_purchase = DjangoPaginationConnectionField(queries.PurchaseObjectType)
    invoice_detail = graphene.Field(
        queries.InvoiceObjectType, id=graphene.String(), resolver=resolvers.resolve_invoice)


class Mutation(ObjectType):
    person = mutations.PersonMutation.Field()
    credit_card = mutations.CreditCardMutation.Field()
    purchase = mutations.PurchaseMutation.Field()


schema = build_schema(mutation=Mutation, query=Query)
