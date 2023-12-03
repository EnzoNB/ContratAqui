from django.shortcuts import get_object_or_404, render,redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Categoria,SubCategoria,Servico,Mensagem,SalaDeMensagens,PropostaServico, Perfil, Avaliacao,PropostaAceita
from .forms import ServicoForm,ServicoUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db import IntegrityError


class HomeView(ListView):
    template_name = "home.html"
    queryset = Categoria.objects.all()
    context_object_name = 'categorias'
    
    def get_context_data(self, *args, **kwargs):
        list_types = Categoria.objects.all()
        context = super(HomeView,self).get_context_data( *args, **kwargs)
        context["list_types"] = list_types
        return context

    
def SearchView(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        serviços = SubCategoria.objects.filter(nome__contains=searched )
        return render(request,"search.html",{"searched":searched,"serviços":serviços})
    else:
        return render(request,"search.html",{})
    

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
    form_class = ServicoUpdateForm
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

def conversas(request, servico_id, username, autor_username):
    servico = get_object_or_404(Servico, pk=servico_id)
    autor_username = servico.autor.username
    cliente = get_object_or_404(User, username=username)
    autor = get_object_or_404(User, username=autor_username)

    identificador_sala = slugify(f'{cliente.username}-{autor.username}-{servico_id}')
    sala_de_mensagens, created = SalaDeMensagens.objects.get_or_create(
        servico=servico,
        identificador_sala=identificador_sala
    )
    sala_de_mensagens.clientes.add(cliente, autor)

    if request.method == 'POST':
        texto_mensagem = request.POST.get('texto_mensagem')

        if texto_mensagem:
            if request.user == cliente:
                autor_da_mensagem = cliente
            else:
                autor_da_mensagem = autor

            Mensagem.objects.create(sala_de_mensagens=sala_de_mensagens, autor=autor_da_mensagem, texto=texto_mensagem)

            # Adicione aqui a lógica de notificação se necessário

        else:
            pass

        return redirect('conversas', servico_id=servico_id, username=username, autor_username=autor_username)
    proposta_criada = PropostaServico.objects.filter(
        servico=servico, autor=servico.autor, cliente=cliente
    ).exists()
    mensagens = Mensagem.objects.filter(sala_de_mensagens=sala_de_mensagens).order_by('data_envio')

    # Verifica se o usuário logado é o autor do serviço
    autor_da_proposta = get_object_or_404(User, username=autor_username)
    propostas = PropostaServico.objects.filter(servico=servico, autor=autor_da_proposta, cliente=cliente)

    return render(request, 'servico/servico_mensagens.html', {
        'servico': servico,
        'mensagens': mensagens,
        'cliente': cliente,
        'propostas': propostas,
        'proposta_criada': proposta_criada,
        'user': request.user  # Adicionei 'user' ao contexto
    })
def servico_lista_conversas(request, username):
    usuario = request.user
    salas_autor = SalaDeMensagens.objects.filter(servico__autor=usuario)
    salas_cliente = SalaDeMensagens.objects.filter(clientes=usuario).exclude(servico__autor=usuario)
    
    # Obtendo propostas aceitas do usuário logado, como autor e como cliente
    propostas_aceitas_autor = PropostaAceita.objects.filter(proposta__servico__autor=usuario, concluida=False)
    propostas_aceitas_cliente = PropostaAceita.objects.filter(proposta__cliente=usuario, concluida=False)
    
    # Verificando se existem propostas aceitas finalizadas, tanto como autor quanto como cliente
    propostas_aceitas_finalizadas_autor = PropostaAceita.objects.filter(proposta__servico__autor=usuario, concluida=True)
    propostas_aceitas_finalizadas_cliente = PropostaAceita.objects.filter(proposta__cliente=usuario, concluida=True)
    
    return render(request, 'servico/servico_lista_conversas.html', {
        'salas_autor': salas_autor,
        'salas_cliente': salas_cliente,
        'usuario': usuario,
        'propostas_aceitas_autor': propostas_aceitas_autor,
        'propostas_aceitas_cliente': propostas_aceitas_cliente,
        'propostas_aceitas_finalizadas_autor': propostas_aceitas_finalizadas_autor,
        'propostas_aceitas_finalizadas_cliente': propostas_aceitas_finalizadas_cliente,
    })


def criar_proposta(request, servico_id, username, autor_username):
    servico = get_object_or_404(Servico, pk=servico_id)
    cliente = get_object_or_404(User, username=username)
    autor = get_object_or_404(User, username=autor_username)

    if request.method == 'POST':
        valor_proposta = request.POST.get('valor_proposta')

        PropostaServico.objects.create(servico=servico, autor=autor, cliente=cliente, valor_proposta=valor_proposta)

        return redirect('listar_propostas', servico_id=servico_id)

    return render(request, 'servico/criar_proposta.html', {'servico': servico, 'cliente': cliente})

@login_required
def listar_propostas(request, servico_id):
    servico = get_object_or_404(Servico, pk=servico_id)
    
    proposta_aceita = PropostaAceita.objects.filter(proposta__servico=servico, concluida=True).first()
    
    if proposta_aceita:
        # Se houver uma proposta aceita e concluída para esse serviço, redirecione para a página de detalhes da proposta aceita
        return redirect('detalhe_proposta_aceita', proposta_aceita_id=proposta_aceita.id)
    
    # Se não houver proposta aceita concluída, continue listando as propostas normais
    if request.user == servico.autor:
        propostas = PropostaServico.objects.filter(servico=servico)
    else:
        propostas = PropostaServico.objects.filter(servico=servico, cliente=request.user)

    # Enviar para o template a informação sobre se há uma proposta aceita para este serviço
    proposta_aceita = PropostaAceita.objects.filter(proposta__servico=servico).exists()

    return render(request, 'servico/listar_propostas.html', {'propostas': propostas, 'servico': servico, 'proposta_aceita': proposta_aceita})

def detalhe_proposta(request, proposta_id,servico_id):
    proposta = get_object_or_404(PropostaServico, pk=proposta_id)
    is_cliente = proposta.cliente == request.user

    return render(request, 'servico/detalhe_proposta.html', {'proposta': proposta, 'is_cliente': is_cliente})


def aceitar_proposta(request, proposta_id):
    proposta = get_object_or_404(PropostaServico, pk=proposta_id)
    servico_id = proposta.servico.id
    cliente = proposta.cliente

    try:
        # Salvar a proposta como PropostaAceita
        proposta_aceita, created = PropostaAceita.objects.get_or_create(proposta=proposta)
        if created:
            proposta_aceita.save()
            # Remover outras propostas relacionadas a esse serviço e cliente, exceto a proposta aceita
            PropostaServico.objects.filter(servico=proposta.servico, cliente=cliente).exclude(pk=proposta_id).delete()
            return redirect('servico_lista_conversas', username=request.user.username)
        else:
            return redirect('detalhe_proposta_aceita', proposta_aceita_id=proposta_aceita.id)
    except IntegrityError:
        # Lógica para lidar com erros de integridade (opcional)
        pass
def recusar_proposta(request, proposta_id):
    proposta = get_object_or_404(PropostaServico, pk=proposta_id)

    # Lógica para deletar somente a proposta atual
    proposta.delete()

    # Redirecionar para a página de detalhes do serviço ou outro lugar desejado
    return redirect('servico-detail', pk=proposta.servico.id)

def criar_avaliacao(request, perfil_id):
    perfil = get_object_or_404(Perfil, pk=perfil_id)
    if request.method == 'POST':
        nota = request.POST.get('nota')
        Avaliacao.objects.create(perfil=perfil, usuario=request.user, nota=nota)
        atualizar_nota_media(perfil)
        return redirect('home')
    return render(request, 'criar_avaliacao.html', {'perfil': perfil})

def atualizar_nota_media(perfil):
    avaliacoes = Avaliacao.objects.filter(perfil=perfil)
    nota_media = sum(a.nota for a in avaliacoes) / avaliacoes.count()
    perfil.nota_media = nota_media
    perfil.numero_avaliacoes = avaliacoes.count()
    perfil.save()


def detalhe_proposta_aceita(request, proposta_aceita_id):
    proposta_aceita = get_object_or_404(PropostaAceita, pk=proposta_aceita_id)
    propostas_aceitas = PropostaAceita.objects.filter(proposta=proposta_aceita.proposta, concluida=True)
    
    is_cliente = request.user == proposta_aceita.proposta.cliente
    
    return render(request, 'servico/detalhe_proposta_aceita.html', {'proposta_aceita': proposta_aceita, 'propostas_aceitas': propostas_aceitas, 'is_cliente': is_cliente})

def finalizar_proposta_aceita(request, proposta_aceita_id):
    proposta_aceita = get_object_or_404(PropostaAceita, pk=proposta_aceita_id)

    if request.method == 'POST':
        proposta_aceita.concluida = True
        proposta_aceita.save()
        return redirect('criar_avaliacao', perfil_id=proposta_aceita.proposta.autor.perfil.id)

    return render(request, 'servico/finalizar_proposta.html', {'proposta_aceita': proposta_aceita})