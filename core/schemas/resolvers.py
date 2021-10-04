from core import models
class ClassName:
    pass
    
    
    
    
def resolve_invoice(root, info, id):
    return models.Invoice.objects.get(pk=id)
