# Sistema de Atendimento — Conselho Tutelar

Desenvolvido com Python + Django.

## Como instalar e rodar

```bash
# 1. Instalar dependências
pip install django

# 2. Criar banco de dados
python manage.py migrate

# 3. Criar usuário administrador
python manage.py createsuperuser

# 4. Rodar o servidor
python manage.py runserver
```

Acesse em: http://localhost:8000

Painel admin: http://localhost:8000/admin

## Estrutura do sistema

- **Dashboard** — visão geral, alertas de aniversário e atendimentos recentes
- **Novo atendimento** — formulário simplificado (criança + responsável + descrição)
- **Lista de atendimentos** — busca por nome, protocolo ou responsável
- **Detalhe do atendimento** — ficha completa + histórico da criança

## Funcionalidades

- Número de protocolo automático (ex: CT-2026-00001)
- Data e hora do atendimento registradas automaticamente
- Idade calculada automaticamente pela data de nascimento
- **Alerta de aniversários** — destaca na dashboard quem faz aniversário nos próximos 7 dias
- Histórico de atendimentos por criança
- Busca rápida por nome, protocolo ou responsável
- Filtro por status (aberto, em andamento, encerrado)

## Próximos passos sugeridos

- [ ] Login e controle de acesso por perfil de usuário
- [ ] Geração de ficha em PDF
- [ ] Campo CPF na criança e no responsável
- [ ] Relatórios por tipo de demanda e período
