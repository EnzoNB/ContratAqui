from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Comment, Category
from .forms import PostForm, EditForm, CommentForm


class HomeView(ListView):
    model = Post
    template_name = "home.html"
    ordering = ['-data_postagem']
    
    def get_context_data(self, *args, **kwargs):
        list_types = Category.objects.all()
        context = super(HomeView,self).get_context_data( *args, **kwargs)
        context["list_types"] = list_types
        return context

class ViewDetalhadaPost(DetailView):
    model = Post
    template_name = "article_details.html"

    def get_context_data(self, *args, **kwargs):
        list_types = Category.objects.all()
        context = super(ViewDetalhadaPost,self).get_context_data( *args, **kwargs)
        context["list_types"] = list_types
        return context

class ViewAdicionarPost(CreateView):
    model = Post
    form_class = PostForm
    template_name = "add_post.html"

    def get_context_data(self, *args, **kwargs):
        list_types = Category.objects.all()
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
        list_types = Category.objects.all()
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
        list_types = Category.objects.all()
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
        list_types = Category.objects.all()
        context = super(ViewAdicionarComentario,self).get_context_data( *args, **kwargs)
        context["list_types"] = list_types
        return context

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)
    
def CategoryView(request, types):
    Category_posts = Post.objects.filter(Category__type=types).order_by('-data_postagem')
    return render(request,"categories.html",{'types':types.title(), 'Category_posts':Category_posts })

def ViewTodasCategorias(request):
    categories_lista = Category.objects.all()
    return render(request,"categories_list.html",{'categories_lista':categories_lista })

    