from .models import Categorys

def add_variable_to_context(request):
    return {
        
        "category":Categorys.objects.all(),
    }