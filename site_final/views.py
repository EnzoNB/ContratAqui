from django.shortcuts import get_object_or_404, render,redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Comment, Category,Categoria,SubCategoria,Servico
from .forms import PostForm, EditForm, CommentForm,ServicoForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse




class HomeView(ListView):
    template_name = "home.html"
    queryset = Categoria.objects.all()
    context_object_name = 'categorias'
    
    def get_context_data(self, *args, **kwargs):
        list_types = Categoria.objects.all()
        context = super(HomeView,self).get_context_data( *args, **kwargs)
        context["list_types"] = list_types
        return context

class ViewDetalhadaPost(DetailView):
    model = Post
    template_name = "article_details.html"

    def get_context_data(self, *args, **kwargs):
        list_types = Categoria.objects.all()
        context = super(ViewDetalhadaPost,self).get_context_data( *args, **kwargs)
        context["list_types"] = list_types
        return context

class ViewAdicionarPost(CreateView):
    model = Post
    form_class = PostForm
    template_name = "add_post.html"

    def get_context_data(self, *args, **kwargs):
        list_types = Categoria.objects.all()
        context = super(ViewAdicionarPost,self).get_context_data( *args, **kwargs)
        context["list_types"] = list_types
        return context
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        form.save_m2m()  
        return super().form_valid(form)

class ViewAtualizarPost(UpdateView):
    model = Post
    form_class = EditForm
    template_name = "update_post.html"

    def get_context_data(self, *args, **kwargs):
        list_types = Categoria.objects.all()
        context = super(ViewAtualizarPost,self).get_context_data( *args, **kwargs)
        context["list_types"] = list_types
        return context
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        form.save_m2m()  # save many-to-many data
        return super().form_valid(form)

class ViewApagarPost(DeleteView):
    model = Post
    template_name = "delete_post.html"
    

    def get_context_data(self, *args, **kwargs):
        list_types = Categoria.objects.all()
        context = super(ViewApagarPost,self).get_context_data( *args, **kwargs)
        context["list_types"] = list_types
        return context
    
    success_url = reverse_lazy('home')

class ViewAdicionarComentario(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "add_comment.html"
    ordering = ['-comment_date']
    success_url = reverse_lazy('home')

    def get_context_data(self, *args, **kwargs):
        list_types = Categoria.objects.all()
        context = super(ViewAdicionarComentario,self).get_context_data( *args, **kwargs)
        context["list_types"] = list_types
        return context

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)
    
def SearchView(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        serviços = SubCategoria.objects.filter(nome__contains=searched )
        return render(request,"search.html",{"searched":searched,"serviços":serviços})
    else:
        return render(request,"search.html",{})
    
def CategoryView(request, types):
    Category_posts = Post.objects.filter(Category__type=types).order_by('-data_postagem')
    return render(request,"categories.html",{'types':types.title(), 'Category_posts':Category_posts })

def ViewTodasCategorias(request):
    categories_lista = Category.objects.all()
    return render(request,"categories_list.html",{'categories_lista':categories_lista })

################################################################################################

class CategoriaListView(ListView):
    model = Categoria
    template_name = 'categoria_list.html'

    def get_context_data(self, *args, **kwargs):
        list_types = Categoria.objects.all()
        context = super(CategoriaListView,self).get_context_data( *args, **kwargs)
        context["list_types"] = list_types
        return context


class CategoriaDetailView(DetailView):
    model = Categoria
    template_name = 'categoria_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, *args, **kwargs):
        list_types = Categoria.objects.all()
        context = super(CategoriaDetailView,self).get_context_data( *args, **kwargs)
        context["list_types"] = list_types
        return context


class SubCategoriaListView(ListView):
    model = SubCategoria
    template_name = 'subcategoria_list.html'

    def get_context_data(self, *args, **kwargs):
        list_types = Categoria.objects.all()
        context = super(SubCategoriaListView,self).get_context_data( *args, **kwargs)
        context["list_types"] = list_types
        return context


class SubCategoriaDetailView(DetailView):
    model = SubCategoria
    template_name = 'subcategoria_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'subcategoria_slug'

    def get_context_data(self, **kwargs):
        context = super(SubCategoriaDetailView,self).get_context_data(**kwargs)
        categoria_slug = self.kwargs.get('categoria_slug')
        subcategoria_slug = self.kwargs.get('subcategoria_slug')

        categoria = get_object_or_404(Categoria, slug=categoria_slug)
        subcategoria = get_object_or_404(SubCategoria, slug=subcategoria_slug, categoria_pai=categoria)

        servicos = Servico.objects.filter(subcategoria=subcategoria)
        context['subcategoria'] = subcategoria
        context['servicos'] = servicos
        
        return context  

class ServicoCreateView(LoginRequiredMixin, CreateView):
    model = Servico
    form_class = ServicoForm
    template_name = 'servico/servico_form.html'
    success_url = '/'

    def get_context_data(self, *args, **kwargs):
        list_types = Categoria.objects.all()
        context = super(ServicoCreateView,self).get_context_data( *args, **kwargs)
        context["list_types"] = list_types
        return context

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

class ServicoListView(ListView):
    model = Servico
    template_name = 'servico/servico_list.html'
    context_object_name = 'servicos'

    def get_context_data(self, *args, **kwargs):
        list_types = Categoria.objects.all()
        context = super(ServicoListView,self).get_context_data( *args, **kwargs)
        context["list_types"] = list_types
        return context

class ServicoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Servico
    fields = ['nome', 'descricao']
    template_name = 'servico/servico_editar.html'

    def get_context_data(self, *args, **kwargs):
        list_types = Categoria.objects.all()
        context = super(ServicoUpdateView,self).get_context_data( *args, **kwargs)
        context["list_types"] = list_types
        return context

    def test_func(self):
        servico = self.get_object()
        return self.request.user == servico.autor
    def get_success_url(self):
        return reverse_lazy('servico-detail', kwargs={'pk': self.object.pk})

class ServicoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Servico
    success_url = reverse_lazy('home')  
    template_name = 'servico/servico_delete.html'

    def test_func(self):
        servico = self.get_object()
        return self.request.user == servico.autor

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return redirect(success_url)
    
    def get_context_data(self, *args, **kwargs):
        list_types = Categoria.objects.all()
        context = super(ServicoDeleteView,self).get_context_data( *args, **kwargs)
        context["list_types"] = list_types
        return context
    
class ServicoDetailView(DetailView):
    model = Servico
    template_name = 'servico/servico_detail.html'
    context_object_name = 'servico'

    def get_context_data(self, *args, **kwargs):
        list_types = Categoria.objects.all()
        context = super(ServicoDetailView,self).get_context_data( *args, **kwargs)
        context["list_types"] = list_types
        return context

def get_subcategorias(request):
    categoria_id = request.GET.get('categoria_id')
    if categoria_id:
        try:
            subcategorias = SubCategoria.objects.filter(categoria_pai_id=categoria_id).order_by('nome')
            options = '<option value="">---------</option>'
            for subcategoria in subcategorias:
                options += f'<option value="{subcategoria.pk}">{subcategoria.nome}</option>'
            return JsonResponse({'options': options})
        except SubCategoria.DoesNotExist:
            pass
    return JsonResponse({'options': ''})