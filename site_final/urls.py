from django import views
from django.urls import path, include
from .views import HomeView, ServicoDetailView,CategoriaDetailView,CategoriaListView,SubCategoriaDetailView,SubCategoriaListView,ServicoCreateView,ServicoDeleteView,ServicoListView,ServicoUpdateView,SearchView,conversas
from . import views

urlpatterns = [
    path('',HomeView.as_view(),name="home"),
    path('categorias/', CategoriaListView.as_view(), name='categoria_list'),
    path('categorias/<slug:slug>/', CategoriaDetailView.as_view(), name='categoria_detail'),
    path('categorias/<slug:categoria_slug>/', SubCategoriaListView.as_view(), name='subcategoria_list'),
    path('categorias/<slug:categoria_slug>/<slug:subcategoria_slug>/', SubCategoriaDetailView.as_view(), name='subcategoria_detail'),
    path('criar/', ServicoCreateView.as_view(), name='servico-create'),
    path('lista/', ServicoListView.as_view(), name='servico-list'),
    path('<int:pk>/editar/', ServicoUpdateView.as_view(), name='servico-update'),
    path('<int:pk>/deletar/', ServicoDeleteView.as_view(), name='servico-delete'),
    path('servico/<int:pk>/', ServicoDetailView.as_view(), name='servico-detail'),
    path('ajax_select/', include('ajax_select.urls')),
    path('get_subcategorias/', views.get_subcategorias, name='get_subcategorias'),
    path('buscando/', SearchView, name = "search"),
    path('servico/<int:servico_id>/mensagens/<str:username>/<str:autor_username>/', views.conversas, name='conversas'),
    path('<str:username>/lista_conversas/', views.servico_lista_conversas, name='servico_lista_conversas'),
    path('servico/<int:servico_id>/proposta/criar/<str:username>/<str:autor_username>/', views.criar_proposta, name='criar_proposta'),
    path('servico/<int:servico_id>/proposta/listar/', views.listar_propostas, name='listar_propostas'),
    path('servico/<int:servico_id>/proposta/<int:proposta_id>/', views.detalhe_proposta, name='proposta_detail'),

]
