from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from datetime import date
from .models import Atendimento, Crianca, Responsavel
from .forms import AtendimentoForm
from .pdf_ficha import gerar_ficha_pdf


@login_required
def dashboard(request):
    hoje = date.today()
    criancas_aniversario = [c for c in Crianca.objects.all() if c.aniversario_esta_semana]
    responsaveis_aniversario = [r for r in Responsavel.objects.filter(data_nascimento__isnull=False) if r.aniversario_esta_semana]
    atendimentos_recentes = Atendimento.objects.select_related('crianca', 'responsavel').order_by('-data_hora')[:10]
    total_abertos = Atendimento.objects.filter(status='aberto').count()
    total_mes = Atendimento.objects.filter(data_hora__month=hoje.month, data_hora__year=hoje.year).count()
    total_andamento = Atendimento.objects.filter(status='em_andamento').count()
    context = {
        'criancas_aniversario': criancas_aniversario,
        'responsaveis_aniversario': responsaveis_aniversario,
        'atendimentos_recentes': atendimentos_recentes,
        'total_abertos': total_abertos,
        'total_mes': total_mes,
        'total_andamento': total_andamento,
        'hoje': hoje,
    }
    return render(request, 'atendimentos/dashboard.html', context)


@login_required
def novo_atendimento(request):
    if request.method == 'POST':
        form = AtendimentoForm(request.POST)
        if form.is_valid():
            atendimento = form.save()
            messages.success(request, f'Atendimento {atendimento.numero_protocolo} registrado com sucesso!')
            return redirect('dashboard')
    else:
        form = AtendimentoForm()
    return render(request, 'atendimentos/form_atendimento.html', {'form': form})


@login_required
def editar_atendimento(request, pk):
    atendimento = get_object_or_404(Atendimento, pk=pk)

    if request.method == 'POST':
        atendimento.crianca.nome = request.POST.get('crianca_nome', '').strip()
        atendimento.crianca.escola = request.POST.get('crianca_escola', '').strip()
        nasc_crianca = request.POST.get('crianca_data_nascimento')
        if nasc_crianca:
            atendimento.crianca.data_nascimento = nasc_crianca
        atendimento.crianca.save()

        atendimento.responsavel.nome = request.POST.get('responsavel_nome', '').strip()
        atendimento.responsavel.telefone = request.POST.get('responsavel_telefone', '').strip()
        atendimento.responsavel.vinculo = request.POST.get('responsavel_vinculo', '')
        atendimento.responsavel.bairro = request.POST.get('responsavel_bairro', '').strip()
        nasc_resp = request.POST.get('responsavel_data_nascimento')
        if nasc_resp:
            atendimento.responsavel.data_nascimento = nasc_resp
        atendimento.responsavel.save()

        atendimento.tipo_demanda = request.POST.get('tipo_demanda', '')
        atendimento.descricao = request.POST.get('descricao', '').strip()
        atendimento.encaminhamento = request.POST.get('encaminhamento', '')
        atendimento.status = request.POST.get('status', 'aberto')
        atendimento.save()

        messages.success(request, f'Atendimento {atendimento.numero_protocolo} atualizado com sucesso!')
        return redirect('detalhe_atendimento', pk=pk)

    return render(request, 'atendimentos/editar_atendimento.html', {'atendimento': atendimento})


@login_required
def detalhe_atendimento(request, pk):
    atendimento = get_object_or_404(Atendimento, pk=pk)
    historico = Atendimento.objects.filter(crianca=atendimento.crianca).exclude(pk=pk).order_by('-data_hora')
    return render(request, 'atendimentos/detalhe.html', {'atendimento': atendimento, 'historico': historico})


@login_required
def lista_atendimentos(request):
    atendimentos = Atendimento.objects.select_related('crianca', 'responsavel').all()
    busca = request.GET.get('q', '')
    if busca:
        atendimentos = (atendimentos.filter(crianca__nome__icontains=busca) |
                        atendimentos.filter(numero_protocolo__icontains=busca) |
                        atendimentos.filter(responsavel__nome__icontains=busca))
    status = request.GET.get('status', '')
    if status:
        atendimentos = atendimentos.filter(status=status)
    return render(request, 'atendimentos/lista.html', {'atendimentos': atendimentos, 'busca': busca, 'status_filtro': status})


@login_required
def ficha_pdf(request, pk):
    atendimento = get_object_or_404(Atendimento, pk=pk)
    buffer = gerar_ficha_pdf(atendimento)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="ficha_{atendimento.numero_protocolo}.pdf"'
    return response


@login_required
@require_POST
def atualizar_status(request, pk):
    atendimento = get_object_or_404(Atendimento, pk=pk)
    novo_status = request.POST.get('status', '')
    status_validos = [s[0] for s in Atendimento.STATUS_CHOICES]
    if novo_status in status_validos:
        atendimento.status = novo_status
        atendimento.save()
        return JsonResponse({
            'ok': True,
            'status': novo_status,
            'status_display': atendimento.get_status_display(),
        })
    return JsonResponse({'ok': False, 'erro': 'Status inválido'}, status=400)
