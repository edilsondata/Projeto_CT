from django import forms
from .models import Atendimento, Crianca, Responsavel


class CriancaForm(forms.ModelForm):
    class Meta:
        model = Crianca
        fields = ['nome', 'data_nascimento', 'escola']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }


class ResponsavelForm(forms.ModelForm):
    class Meta:
        model = Responsavel
        fields = ['nome', 'telefone', 'vinculo', 'bairro', 'data_nascimento']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }


class AtendimentoForm(forms.Form):
    # Dados da criança
    crianca_nome = forms.CharField(label='Nome completo', max_length=200)
    crianca_data_nascimento = forms.DateField(
        label='Data de nascimento',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    crianca_escola = forms.CharField(label='Escola', max_length=200, required=False)

    # Dados do responsável
    responsavel_nome = forms.CharField(label='Nome do responsável', max_length=200)
    responsavel_telefone = forms.CharField(label='Telefone / WhatsApp', max_length=20)
    responsavel_vinculo = forms.ChoiceField(label='Vínculo', choices=Responsavel.VINCULO_CHOICES)
    responsavel_bairro = forms.CharField(label='Bairro / Comunidade', max_length=100, required=False)
    responsavel_data_nascimento = forms.DateField(
        label='Data de nascimento do responsável',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    # Dados do atendimento
    tipo_demanda = forms.ChoiceField(label='Tipo de demanda', choices=Atendimento.TIPO_CHOICES)
    descricao = forms.CharField(label='Descrição do atendimento', widget=forms.Textarea(attrs={'rows': 4}))
    encaminhamento = forms.ChoiceField(
        label='Encaminhamento realizado',
        choices=Atendimento.ENCAMINHAMENTO_CHOICES,
        required=False
    )

    def save(self):
        data = self.cleaned_data

        crianca = Crianca.objects.create(
            nome=data['crianca_nome'],
            data_nascimento=data['crianca_data_nascimento'],
            escola=data.get('crianca_escola', ''),
        )

        responsavel = Responsavel.objects.create(
            nome=data['responsavel_nome'],
            telefone=data['responsavel_telefone'],
            vinculo=data['responsavel_vinculo'],
            bairro=data.get('responsavel_bairro', ''),
            data_nascimento=data.get('responsavel_data_nascimento'),
        )

        atendimento = Atendimento.objects.create(
            crianca=crianca,
            responsavel=responsavel,
            tipo_demanda=data['tipo_demanda'],
            descricao=data['descricao'],
            encaminhamento=data.get('encaminhamento', ''),
        )

        return atendimento
