from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, TemplateView, DetailView, FormView

# Create your views here.
from app_noticias.forms import ContatoForm, DenunciaNoticiaForm
from .models import *


class HomePageView(ListView):
    model = Noticia
    context_object_name = 'noticias'
    template_name = 'app_noticias/home.html'

    def get_queryset(self):
        return Noticia.objects.exclude(data_de_publicacao=None).order_by('-data_de_publicacao')[:5]


class NoticiasResumoView(TemplateView):
    template_name = 'app_noticias/resumo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = Noticia.objects.count()
        context['state'] =  DenunciaNoticia.objects.count()
        context['city'] =  DenunciaNoticia.objects.count()

        return context   


class NoticiaDetalhesView(DetailView):
    model = Noticia
    template_name = 'app_noticias/detalhes.html'


class TagDetalhesView(DetailView):
    model = Tag
    template_name = 'app_noticias/noticias_da_tag.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['noticias'] = Noticia.objects.filter(tags__in=[self.object])
        return context


class ContatoView(FormView):
    template_name = 'app_noticias/contato.html'
    form_class = ContatoForm

    def form_valid(self, form):
        dados = form.clean()
        mensagem = MensagemDeContato(
            nome=dados['nome'], email=dados['email'], mensagem=dados['mensagem'])
        mensagem.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('contato_sucesso')


class ContatoSucessoView(TemplateView):
    template_name = 'app_noticias/contato_sucesso.html'


def noticias_da_tag(request, tag_slug):
    try:
        tag = Tag.objects.get(slug=tag_slug)
        noticias = Noticia.objects.filter(tags__in=[tag])
    except Tag.DoesNotExist:
        raise Http404('Tag não encontrada')
    return render(request, 'app_noticias/noticias_da_tag.html', {'tag': tag, 'noticias': noticias})


def noticia_detalhes(request, id):
    try:
        n = Noticia.objects.get(pk=id)
        return render(request, 'app_noticias/detalhes.html', {'noticia': n})
    except Noticia.DoesNotExist:
        return Http404('Notícia não encontrada')


def autor_detalhes(request, id):
    try:
        pessoa = Pessoa.objects.get(pk=id)
        noticias = Noticia.objects.filter(autor=pessoa)
        return render(request, 'app_noticias/autor.html', {
            'autor': pessoa,
            'noticias': noticias
        })
    except Pessoa.DoesNotExist:
        return Http404('Este autor não foi encontrado')


def categoria_detalhes(request, slug):
    try:
        categoria = Categoria.objects.get(slug=slug)
        noticias = Noticia.objects.filter(categoria=categoria)
        porcentagem = noticias.count()/Noticia.objects.count()*100
        return render(request, 'app_noticias/categoria.html', {
            'categoria': categoria,
            'noticias': noticias,
            'porcentagem': porcentagem
        })
    except Categoria.DoesNotExist:
        return Http404('Categoria não encontrada')

#VIEW DO FORMULÁRIO DE DENÚNCIA DE NPTÍCIAS!
class DenunciaNoticiaView(FormView):
    template_name = 'app_noticias/denuncias.html' #estamos passando o nome do template para variavel template_name.
    form_class = DenunciaNoticiaForm # classe DenunciaNoticiaForm do arquivo forms.py

    def form_valid(self, form):
        dados = form.clean()
    # INSTANCIANDO UM OBJETO DA CLASSE DenunciaNoticia
        denuncia = DenunciaNoticia(state=dados['state'], city=dados['city'], description=dados['description']) 
    # PERSISTINDO OS OBJETOS (DADOS) NO SQLITE.
        denuncia.save()
    #PASSANDO COMO RETORNO A RECUPERAÇÃO DOS DADOS JÁ VALIDADOS OBTIDOS PELO FORMULÁRIO.
        return super().form_valid(form)

    
    def get_success_url(self):# MÉTODO DE SUCESSO RETORNA UMA URL DE SUCESSO SE VALIDAÇÃO DE FORMULARIO ESTIVER TUDO OK.
        return reverse ('denuncia_sucesso')

class DenunciaNoticiaSucessoView(TemplateView):
    template_name = 'app_noticias/denuncia_sucesso.html'

# RESUMO DAS DENÚNCIAS DE NOTÍCIAS

# QUANTIDADE DE DENÚCIAS POR ESTADO e CIDADE
# def quantidade_denuncias_por_estado_cidade(request, uf, cidade):
#     denuncias = DenunciaNoticia.objects.all()
#     teste = DenunciaNoticiaForm.isValid()
#     estado = teste.filter(state=uf).count()
#     cidade = teste.filter(city=cidade).count()
#     return render(request, 'app_noticias/resumo.html', {
#         'estado': estado,
#         'cidade': cidade,
#         'teste': teste,
#     })

# def quantidade_denuncias_por_cidade(request, cidade):
#     denuncias = DenunciaNoticia.objects.all()
#     UF = denuncias.filter(state=uf).count()
#     return render(request, 'app_noticias/resumo.html', {
#         'estado': denuncias,
#     })