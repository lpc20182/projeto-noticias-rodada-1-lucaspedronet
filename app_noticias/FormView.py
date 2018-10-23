class ContatoView(FormView):
    template_name = 'app_noticias/contato.html'
    form_class = ContatoForm

    def form_valid(self, form):
        dados = form.clean()
        mensagem = MensagemDeContato(cidade=dados['cidade'], estado=dados['estado'], descricao=dados['descricao'])
        mensagem.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse ('contato_sucesso')
    

class ContatoSucessoView(TemplateView):
    template_name = 'app_noticias/contato_sucesso.html'


#VIEW DO FORMULÁRIO DE DENÚNCIA DE NPTÍCIAS!

class DenunciaNoticiaView(FormView):# A CLASSE DenunciaNoticia HERDA DE FormView TEMPLATE DE FORMULÁRIO. 
    template_name = 'app_noticias/denuncias.html' #estamos passando o nome do template para variavel template_name.
    form_class = DenunciaNoticiaForm # classe DenunciaNoticiaForm do arquivo forms.py

    def form_valid(self, form): # VALIDANDO OS DADOS DO FORMULÁRIO
        dados = form.clean()
        denuncia = DenunciaNoticia(state=dados['state'], city=dados['city'], description=dados['description'])
        denuncia.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse ('denuncias_sucesso')

class DenunciaNoticiaSucessoView(TemplateView):
    template_name = 'app_noticias/denuncias_sucesso.html'