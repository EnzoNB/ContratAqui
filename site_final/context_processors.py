# Em um novo arquivo chamado context_processors.py
from .models import Categoria

def categorias(request):
    cat=Categoria.objects.all()
    choices_dynamic = []
    for choice in cat:
        choices_dynamic.append(choice)
    return {'list_types': choices_dynamic}
