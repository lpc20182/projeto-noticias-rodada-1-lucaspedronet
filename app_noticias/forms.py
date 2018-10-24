from django import forms


class ContatoForm(forms.Form):
    nome = forms.CharField(max_length=128, min_length=12)
    email = forms.EmailField(required=False)
    mensagem = forms.CharField(widget=forms.Textarea)

    def clean(self):
        dados = super().clean()
        # não aceita e-mail do gmail
        email = dados.get('email', None)
        mensagem = dados.get('mensagem')
        if '@gmail.com' in email:
            self.add_error('email', 'Provedor de e-mail não suportado (gmail.com)')
        # testa palavras não permitidas na mensagem
        palavras = ['problema', 'defeito', 'erro']
        for palavra in palavras:
            if palavra in mensagem.lower():
                self.add_error('mensagem', 'Mensagem contém palavra não permitida')
        return dados

class DenunciaNoticiaForm(forms.Form):
    state = forms.CharField(min_length=2, max_length=50)
    city = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea, min_length=10, max_length=255)

    def isValid(self):
        dados = super().clean()
        state = dados.get('state', None)
        city = dados.get('city')
        description = dados.get('description')
        if description < 0:
            self.add_error('description', 'Descrição da denúcia deve conter no mínimo 10 carectere!')
        ufs = ['TO', 'DF', 'GO', 'RJ', 'SP']
        for uf in ufs:
            if uf in state.lower():
                self.add_error('state', 'Estado não aceito!')
        return dados