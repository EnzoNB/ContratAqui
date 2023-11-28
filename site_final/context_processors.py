# Em um novo arquivo chamado context_processors.py
from .models import Categoria

def categorias(request):
    categorias = Categoria.objects.all()
    print(categorias)  # Adicione esta linha
    return {'list_types': categorias}
