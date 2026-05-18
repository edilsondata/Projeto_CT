from django.contrib import admin
from .models import Crianca, Responsavel, Atendimento

@admin.register(Crianca)
class CriancaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'data_nascimento', 'escola']
    search_fields = ['nome']

@admin.register(Responsavel)
class ResponsavelAdmin(admin.ModelAdmin):
    list_display = ['nome', 'telefone', 'vinculo', 'bairro']
    search_fields = ['nome']

@admin.register(Atendimento)
class AtendimentoAdmin(admin.ModelAdmin):
    list_display = ['numero_protocolo', 'crianca', 'tipo_demanda', 'status', 'data_hora']
    list_filter = ['status', 'tipo_demanda']
    search_fields = ['numero_protocolo', 'crianca__nome', 'responsavel__nome']
