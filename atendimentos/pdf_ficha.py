from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from datetime import date


# Cores do sistema
AZUL_ESCURO = colors.HexColor('#1a2a4a')
VERDE = colors.HexColor('#16a34a')
CINZA_CLARO = colors.HexColor('#f1f5f9')
CINZA_TEXTO = colors.HexColor('#64748b')
VERMELHO = colors.HexColor('#be123c')
BRANCO = colors.white


def gerar_ficha_pdf(atendimento):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
    )

    # Estilos
    estilo_titulo = ParagraphStyle('titulo', fontSize=18, fontName='Helvetica-Bold',
                                   textColor=AZUL_ESCURO, alignment=TA_CENTER, spaceAfter=4)
    estilo_sub = ParagraphStyle('sub', fontSize=10, fontName='Helvetica',
                                textColor=CINZA_TEXTO, alignment=TA_CENTER, spaceAfter=2)
    estilo_protocolo = ParagraphStyle('proto', fontSize=13, fontName='Helvetica-Bold',
                                      textColor=AZUL_ESCURO, alignment=TA_CENTER, spaceAfter=2)
    estilo_secao = ParagraphStyle('secao', fontSize=10, fontName='Helvetica-Bold',
                                  textColor=BRANCO, spaceAfter=6, spaceBefore=10)
    estilo_campo_label = ParagraphStyle('label', fontSize=8, fontName='Helvetica-Bold',
                                        textColor=CINZA_TEXTO, spaceAfter=1)
    estilo_campo_valor = ParagraphStyle('valor', fontSize=10, fontName='Helvetica',
                                        textColor=AZUL_ESCURO, spaceAfter=6)
    estilo_rodape = ParagraphStyle('rodape', fontSize=8, fontName='Helvetica',
                                   textColor=CINZA_TEXTO, alignment=TA_CENTER)

    story = []

    # Cabeçalho
    story.append(Paragraph('CONSELHO TUTELAR', estilo_titulo))
    story.append(Paragraph('Ficha de Atendimento', estilo_sub))
    story.append(HRFlowable(width='100%', thickness=3, color=VERDE, spaceAfter=8))

    # Protocolo e status
    status_map = {'aberto': 'ABERTO', 'em_andamento': 'EM ANDAMENTO', 'encerrado': 'ENCERRADO'}
    status_cor = {'aberto': colors.HexColor('#fbbf24'), 'em_andamento': colors.HexColor('#3b82f6'), 'encerrado': VERDE}

    dados_proto = [
        [
            Paragraph(f'<b>Protocolo:</b> {atendimento.numero_protocolo}', ParagraphStyle('p', fontSize=11, fontName='Helvetica-Bold', textColor=AZUL_ESCURO)),
            Paragraph(f'<b>Data:</b> {atendimento.data_hora.strftime("%d/%m/%Y às %H:%M")}', ParagraphStyle('p', fontSize=10, fontName='Helvetica', textColor=CINZA_TEXTO)),
            Paragraph(status_map.get(atendimento.status, atendimento.status),
                     ParagraphStyle('s', fontSize=10, fontName='Helvetica-Bold',
                                   textColor=status_cor.get(atendimento.status, AZUL_ESCURO),
                                   alignment=TA_CENTER)),
        ]
    ]
    tabela_proto = Table(dados_proto, colWidths=[6*cm, 7*cm, 4*cm])
    tabela_proto.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), CINZA_CLARO),
        ('ROUNDEDCORNERS', [5, 5, 5, 5]),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(tabela_proto)
    story.append(Spacer(1, 0.4*cm))

    def secao_header(texto):
        dados = [[Paragraph(f'  {texto}', estilo_secao)]]
        t = Table(dados, colWidths=[17*cm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), AZUL_ESCURO),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ]))
        return t

    def campo(label, valor):
        return [
            Paragraph(label.upper(), estilo_campo_label),
            Paragraph(str(valor) if valor else '—', estilo_campo_valor),
        ]

    # SEÇÃO: Criança / Adolescente
    story.append(secao_header('CRIANÇA / ADOLESCENTE'))
    story.append(Spacer(1, 0.2*cm))

    dados_crianca = [
        [
            Table([[Paragraph('NOME COMPLETO', estilo_campo_label)],
                   [Paragraph(atendimento.crianca.nome, estilo_campo_valor)]], colWidths=[11*cm]),
            Table([[Paragraph('DATA DE NASCIMENTO', estilo_campo_label)],
                   [Paragraph(atendimento.crianca.data_nascimento.strftime('%d/%m/%Y'), estilo_campo_valor)]], colWidths=[3*cm]),
            Table([[Paragraph('IDADE', estilo_campo_label)],
                   [Paragraph(f'{atendimento.crianca.idade} anos', estilo_campo_valor)]], colWidths=[3*cm]),
        ]
    ]
    t = Table(dados_crianca, colWidths=[11*cm, 3*cm, 3*cm])
    t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 8)]))
    story.append(t)

    escola = atendimento.crianca.escola or '—'
    story.append(Paragraph('ESCOLA', estilo_campo_label))
    story.append(Paragraph(escola, estilo_campo_valor))

    # SEÇÃO: Responsável
    story.append(secao_header('RESPONSÁVEL / QUEM TROUXE'))
    story.append(Spacer(1, 0.2*cm))

    dados_resp = [
        [
            Table([[Paragraph('NOME', estilo_campo_label)],
                   [Paragraph(atendimento.responsavel.nome, estilo_campo_valor)]], colWidths=[9*cm]),
            Table([[Paragraph('VÍNCULO', estilo_campo_label)],
                   [Paragraph(atendimento.responsavel.get_vinculo_display(), estilo_campo_valor)]], colWidths=[4*cm]),
            Table([[Paragraph('TELEFONE', estilo_campo_label)],
                   [Paragraph(atendimento.responsavel.telefone, estilo_campo_valor)]], colWidths=[4*cm]),
        ]
    ]
    t = Table(dados_resp, colWidths=[9*cm, 4*cm, 4*cm])
    t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 8)]))
    story.append(t)

    bairro = atendimento.responsavel.bairro or '—'
    story.append(Paragraph('BAIRRO / COMUNIDADE', estilo_campo_label))
    story.append(Paragraph(bairro, estilo_campo_valor))

    # SEÇÃO: Atendimento
    story.append(secao_header('ATENDIMENTO'))
    story.append(Spacer(1, 0.2*cm))

    dados_atend = [
        [
            Table([[Paragraph('TIPO DE DEMANDA', estilo_campo_label)],
                   [Paragraph(atendimento.get_tipo_demanda_display(), estilo_campo_valor)]], colWidths=[8.5*cm]),
            Table([[Paragraph('ENCAMINHAMENTO', estilo_campo_label)],
                   [Paragraph(atendimento.get_encaminhamento_display() if atendimento.encaminhamento else 'Nenhum', estilo_campo_valor)]], colWidths=[8.5*cm]),
        ]
    ]
    t = Table(dados_atend, colWidths=[8.5*cm, 8.5*cm])
    t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 8)]))
    story.append(t)

    story.append(Paragraph('DESCRIÇÃO DO ATENDIMENTO', estilo_campo_label))
    story.append(Paragraph(atendimento.descricao, estilo_campo_valor))

    # Assinatura
    story.append(Spacer(1, 1*cm))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#e2e8f0'), spaceAfter=6))

    dados_assin = [
        [
            Table([[Paragraph('_' * 45, ParagraphStyle('a', fontSize=10, textColor=CINZA_TEXTO, alignment=TA_CENTER))],
                   [Paragraph('Assinatura do Conselheiro', ParagraphStyle('a2', fontSize=8, textColor=CINZA_TEXTO, alignment=TA_CENTER))]],
                  colWidths=[8.5*cm]),
            Table([[Paragraph('_' * 45, ParagraphStyle('a', fontSize=10, textColor=CINZA_TEXTO, alignment=TA_CENTER))],
                   [Paragraph('Assinatura do Responsável', ParagraphStyle('a2', fontSize=8, textColor=CINZA_TEXTO, alignment=TA_CENTER))]],
                  colWidths=[8.5*cm]),
        ]
    ]
    t = Table(dados_assin, colWidths=[8.5*cm, 8.5*cm])
    t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(t)

    # Rodapé
    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width='100%', thickness=1, color=VERDE, spaceAfter=4))
    story.append(Paragraph(f'Documento gerado em {date.today().strftime("%d/%m/%Y")} — Sistema de Atendimento do Conselho Tutelar', estilo_rodape))

    doc.build(story)
    buffer.seek(0)
    return buffer
